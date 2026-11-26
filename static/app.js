const state = { token: localStorage.getItem("token"), me: null };

async function api(path, { method = "GET", body } = {}) {
  const headers = { "Content-Type": "application/json" };
  if (state.token) headers.Authorization = `Bearer ${state.token}`;
  const res = await fetch(path, { method, headers, body: body ? JSON.stringify(body) : undefined });
  if (res.status === 204) return null;
  const data = await res.json().catch(() => null);
  if (!res.ok) {
    const d = data?.detail;
    throw new Error(Array.isArray(d) ? d.map((e) => `${e.loc.at(-1)}: ${e.msg}`).join("; ") : d || res.statusText);
  }
  return data;
}

function toast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg; t.hidden = false;
  clearTimeout(toast._t); toast._t = setTimeout(() => (t.hidden = true), 3000);
}

const esc = (s) => String(s ?? "").replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const formData = (form) => Object.fromEntries([...new FormData(form)].filter(([, v]) => v !== ""));

async function loadMe() {
  if (!state.token) { state.me = null; return; }
  try { state.me = await api("/api/auth/me"); }
  catch { state.token = null; localStorage.removeItem("token"); state.me = null; }
}

function renderUser() {
  const box = document.getElementById("user-box");
  document.getElementById("auth").hidden = !!state.me;
  document.getElementById("new-book").hidden = !state.me;
  if (!state.me) { box.innerHTML = ""; return; }
  box.innerHTML = `<span>${esc(state.me.first_name)} ${esc(state.me.last_name)} (@${esc(state.me.username)})</span>
    <button class="secondary" id="logout">Выйти</button>`;
  document.getElementById("logout").onclick = () => { state.token = null; localStorage.removeItem("token"); refresh(); };
}

async function renderBooks() {
  const q = document.getElementById("search").value.trim();
  const books = await api(`/api/books${q ? `?q=${encodeURIComponent(q)}` : ""}`);
  const el = document.getElementById("books");
  el.innerHTML = books.length ? "" : `<p class="muted">Книг пока нет</p>`;
  for (const b of books) {
    const mine = state.me && state.me.id === b.author.id;
    const div = document.createElement("div");
    div.className = "item";
    div.innerHTML = `<h3>${esc(b.title)}</h3>
      <span class="muted">${esc(b.author.first_name)} ${esc(b.author.last_name)}</span>
      <p>${esc(b.description)}</p>
      <a href="${esc(b.file_url)}" target="_blank" rel="noopener">Открыть файл</a>
      <span class="muted">Рейтинг: ${b.rating ?? "—"} (${b.ratings_count})</span>
      ${state.me && !mine ? `<div class="stars">${[1, 2, 3, 4, 5].map((n) => `<button data-rate="${n}">★</button>`).join("")}</div>` : ""}
      ${mine ? `<button class="secondary" data-del>Удалить</button>` : ""}`;
    div.querySelectorAll("[data-rate]").forEach((btn) => (btn.onclick = () =>
      api(`/api/books/${b.id}/rate`, { method: "POST", body: { rating: +btn.dataset.rate } })
        .then(() => { toast("Спасибо за оценку!"); refresh(); }).catch((e) => toast(e.message))));
    const del = div.querySelector("[data-del]");
    if (del) del.onclick = () => confirm("Удалить книгу?") &&
      api(`/api/books/${b.id}`, { method: "DELETE" }).then(refresh).catch((e) => toast(e.message));
    el.appendChild(div);
  }
}

async function renderAuthors() {
  const authors = await api("/api/authors");
  document.getElementById("authors").innerHTML = authors.length
    ? authors.map((a) => `<div class="item">
        ${a.image_url ? `<img class="avatar" src="${esc(a.image_url)}" alt="">` : ""}
        <h3>${esc(a.first_name)} ${esc(a.last_name)}</h3>
        <span class="muted">@${esc(a.username)} · книг: ${a.books_count} · рейтинг: ${a.rating}</span>
      </div>`).join("")
    : `<p class="muted">Авторов пока нет</p>`;
}

async function refresh() {
  await loadMe();
  renderUser();
  await Promise.all([renderBooks(), renderAuthors()]).catch((e) => toast(e.message));
}

document.querySelectorAll(".tabs button").forEach((btn) => (btn.onclick = () => {
  document.querySelectorAll(".tabs button").forEach((b) => b.classList.toggle("active", b === btn));
  document.getElementById("login-form").hidden = btn.dataset.tab !== "login";
  document.getElementById("register-form").hidden = btn.dataset.tab !== "register";
}));

async function login(username, password) {
  const { access_token } = await api("/api/auth/login", { method: "POST", body: { username, password } });
  state.token = access_token;
  localStorage.setItem("token", access_token);
}

document.getElementById("login-form").onsubmit = async (e) => {
  e.preventDefault();
  const { username, password } = formData(e.target);
  try { await login(username, password); e.target.reset(); refresh(); } catch (err) { toast(err.message); }
};

document.getElementById("register-form").onsubmit = async (e) => {
  e.preventDefault();
  const data = formData(e.target);
  try {
    await api("/api/auth/register", { method: "POST", body: data });
    await login(data.username, data.password);
    e.target.reset(); toast("Добро пожаловать!"); refresh();
  } catch (err) { toast(err.message); }
};

document.getElementById("book-form").onsubmit = async (e) => {
  e.preventDefault();
  try {
    await api("/api/books", { method: "POST", body: formData(e.target) });
    e.target.reset(); toast("Книга добавлена"); refresh();
  } catch (err) { toast(err.message); }
};

let searchTimer;
document.getElementById("search").oninput = () => { clearTimeout(searchTimer); searchTimer = setTimeout(renderBooks, 250); };

refresh();

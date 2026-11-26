import os
import secrets

# Ключ берётся из окружения; если не задан — генерируется на время жизни процесса
# (токены станут невалидными после рестарта, для прода обязательно задайте JWT_SECRET_KEY).
JWT_SECRET: str = os.getenv("JWT_SECRET_KEY") or secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

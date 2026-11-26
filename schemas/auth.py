from pydantic import BaseModel, Field

USERNAME_PATTERN = r"^[A-Za-z0-9_.-]+$"


class LoginRequest(BaseModel):
    username: str = Field(min_length=3, max_length=32, pattern=USERNAME_PATTERN)
    password: str = Field(min_length=6, max_length=128)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

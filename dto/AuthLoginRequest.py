from pydantic import BaseModel


class AuthLoginRequest(BaseModel):
    # TODO: validation
    username: str
    password: str
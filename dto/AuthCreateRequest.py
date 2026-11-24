from pydantic import BaseModel


class AuthCreateRequest(BaseModel):
        ID: int
        first_name: str
        last_name: str
        image_url: str
        password: str
        username: str
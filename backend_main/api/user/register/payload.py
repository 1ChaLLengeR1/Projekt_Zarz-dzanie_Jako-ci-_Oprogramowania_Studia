from pydantic import BaseModel, EmailStr


class RegisterPayload(BaseModel):
    username: str
    email: EmailStr
    password: str

from pydantic import BaseModel, EmailStr


class LoginPayload(BaseModel):
    email: EmailStr
    password: str

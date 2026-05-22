from pydantic import BaseModel, EmailStr


class UpdateUserPayload(BaseModel):
    username: str
    email: EmailStr
    password: str

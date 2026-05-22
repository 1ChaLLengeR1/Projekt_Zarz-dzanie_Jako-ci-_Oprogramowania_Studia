from datetime import datetime

from pydantic import BaseModel


class UserCollectionItemResponse(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool
    created_at: datetime


class UserCollectionResponse(BaseModel):
    users: list[UserCollectionItemResponse]
    total: int

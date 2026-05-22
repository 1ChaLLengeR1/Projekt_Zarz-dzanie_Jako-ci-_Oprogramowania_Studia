from datetime import datetime

from pydantic import BaseModel


class UpdatedUserResponse(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool
    created_at: datetime

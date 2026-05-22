from dataclasses import dataclass
from datetime import datetime


@dataclass
class GetUsersItemResponse:
    id: str
    username: str
    email: str
    is_active: bool
    created_at: datetime

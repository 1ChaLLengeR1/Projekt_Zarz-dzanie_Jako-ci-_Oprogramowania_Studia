from pydantic import BaseModel


class DeletedUserResponse(BaseModel):
    deleted: str

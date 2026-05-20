from typing import Generic, Literal, TypeVar

from pydantic import BaseModel

DATA = TypeVar("DATA")
ADDITIONALS = TypeVar("ADDITIONALS")


class ApiErrorData(BaseModel):
    message: str
    type_module: str
    type_error: str
    key_type_error: str


class ApiErrorResponse(BaseModel, Generic[ADDITIONALS]):
    status: Literal["ERROR"] = "ERROR"
    status_code: int
    data: ApiErrorData
    additional: ADDITIONALS | None = None


class ApiSuccessResponse(BaseModel, Generic[DATA, ADDITIONALS]):
    status: Literal["SUCCESS"] = "SUCCESS"
    status_code: int = 200
    data: DATA
    additional: ADDITIONALS | None = None

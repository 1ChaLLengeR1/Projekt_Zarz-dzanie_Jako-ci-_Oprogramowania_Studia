from typing import Generic, Literal, TypeVar

from fastapi.responses import JSONResponse
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


def error_response(error: dict, type_module: str) -> JSONResponse:
    return JSONResponse(
        content=ApiErrorResponse(
            status_code=error.get("status_code", 400),
            data=ApiErrorData(
                message=error.get("message", "Unknown error"),
                type_module=error.get("type_module", type_module),
                type_error=error.get("type_error", "error"),
                key_type_error=error.get("type_error", "error"),
            ),
        ).model_dump(mode="json"),
    )

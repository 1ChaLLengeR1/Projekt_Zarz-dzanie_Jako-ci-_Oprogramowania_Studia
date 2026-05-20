from fastapi import APIRouter

from api.response import ApiErrorData, ApiErrorResponse, ApiSuccessResponse
from api.urls import USER_LOGIN
from api.user.payload import LoginPayload
from api.user.response import UserResponse
from core.handlers.user.user import handler_login_user

router = APIRouter()


@router.post(USER_LOGIN, tags=["User"])
def api_login_user(payload: LoginPayload):
    try:
        user, error, is_valid = handler_login_user(payload.email, payload.password)

        if not is_valid:
            return ApiErrorResponse(
                status_code=error.get("status_code", 400),
                data=ApiErrorData(
                    message=error.get("message", "Unknown error"),
                    type_module=error.get("type_module", "api_login_user"),
                    type_error=error.get("type_error", "error"),
                    key_type_error=error.get("type_error", "error"),
                ),
            )

        return ApiSuccessResponse[UserResponse, None](
            status_code=200,
            data=UserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
            ),
        )

    except Exception as e:
        return ApiErrorResponse(
            status_code=500,
            data=ApiErrorData(
                message=str(e),
                type_module="api_login_user",
                type_error="Exception",
                key_type_error="Exception",
            ),
        )

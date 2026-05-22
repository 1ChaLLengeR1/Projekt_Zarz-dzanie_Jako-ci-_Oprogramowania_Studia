from fastapi import APIRouter

from api.response import ApiErrorResponse, ApiSuccessResponse, error_response
from api.urls import USER_LOGIN
from api.user.login.payload import LoginPayload
from api.user.login.response import UserResponse
from core.handlers.user.login.login import handler_login_user

router = APIRouter()


@router.post(
    USER_LOGIN,
    tags=["User"],
    summary="Login user",
    description="Authenticate a user with email and password. Returns user data on success.",
    response_model=ApiSuccessResponse[UserResponse, None],
    responses={
        401: {"model": ApiErrorResponse, "description": "Invalid credentials"},
        404: {"model": ApiErrorResponse, "description": "User not found"},
        500: {"model": ApiErrorResponse, "description": "Internal server error"},
    },
)
def api_login_user(payload: LoginPayload):
    try:
        user, error, is_valid = handler_login_user(payload.email, payload.password)

        if not is_valid:
            return error_response(error, "api_login_user")

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
        return error_response({"message": str(e), "type_error": "Exception", "status_code": 500}, "api_login_user")
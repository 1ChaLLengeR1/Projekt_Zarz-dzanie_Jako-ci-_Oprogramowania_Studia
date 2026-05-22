from fastapi import APIRouter

from api.response import ApiErrorResponse, ApiSuccessResponse, error_response
from api.urls import USER_REGISTER
from api.user.register.payload import RegisterPayload
from api.user.register.response import RegisterUserResponse
from core.handlers.user.register.register import handler_register_user

router = APIRouter()


@router.post(
    USER_REGISTER,
    tags=["User"],
    summary="Register user",
    description="Create a new user account. Password is hashed with Argon2 before storage.",
    response_model=ApiSuccessResponse[RegisterUserResponse, None],
    responses={
        409: {"model": ApiErrorResponse, "description": "Username or email already exists"},
        500: {"model": ApiErrorResponse, "description": "Internal server error"},
    },
)
def api_register_user(payload: RegisterPayload):
    try:
        user, error, is_valid = handler_register_user(
            payload.username, payload.email, payload.password
        )

        if not is_valid:
            return error_response(error, "api_register_user")

        return ApiSuccessResponse[RegisterUserResponse, None](
            status_code=200,
            data=RegisterUserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
            ),
        )

    except Exception as e:
        return error_response({"message": str(e), "type_error": "Exception", "status_code": 500}, "api_register_user")
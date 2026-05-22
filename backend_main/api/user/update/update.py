from fastapi import APIRouter

from api.response import ApiErrorResponse, ApiSuccessResponse, error_response
from api.urls import USER_BY_ID
from api.user.update.payload import UpdateUserPayload
from api.user.update.response import UpdatedUserResponse
from core.handlers.user.update.update import handler_update_user

router = APIRouter()


@router.put(
    USER_BY_ID,
    tags=["User"],
    summary="Update user",
    description="Replace all user fields (username, email, password). Password is re-hashed with Argon2.",
    response_model=ApiSuccessResponse[UpdatedUserResponse, None],
    responses={
        404: {"model": ApiErrorResponse, "description": "User not found"},
        409: {"model": ApiErrorResponse, "description": "Username or email already taken"},
        500: {"model": ApiErrorResponse, "description": "Internal server error"},
    },
)
def api_update_user(user_id: str, payload: UpdateUserPayload):
    try:
        user, error, is_valid = handler_update_user(
            user_id, payload.username, payload.email, payload.password
        )

        if not is_valid:
            return error_response(error, "api_update_user")

        return ApiSuccessResponse[UpdatedUserResponse, None](
            status_code=200,
            data=UpdatedUserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
            ),
        )

    except Exception as e:
        return error_response({"message": str(e), "type_error": "Exception", "status_code": 500}, "api_update_user")

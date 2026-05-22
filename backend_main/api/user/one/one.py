from fastapi import APIRouter

from api.response import ApiErrorResponse, ApiSuccessResponse, error_response
from api.urls import USER_BY_ID
from api.user.one.response import OneUserResponse
from core.handlers.user.one.one import handler_get_user

router = APIRouter()


@router.get(
    USER_BY_ID,
    tags=["User"],
    summary="Get user by ID",
    description="Retrieve a single user by their unique identifier.",
    response_model=ApiSuccessResponse[OneUserResponse, None],
    responses={
        404: {"model": ApiErrorResponse, "description": "User not found"},
        500: {"model": ApiErrorResponse, "description": "Internal server error"},
    },
)
def api_get_user(user_id: str):
    try:
        user, error, is_valid = handler_get_user(user_id)

        if not is_valid:
            return error_response(error, "api_get_user")

        return ApiSuccessResponse[OneUserResponse, None](
            status_code=200,
            data=OneUserResponse(
                id=user.id,
                username=user.username,
                email=user.email,
                is_active=user.is_active,
                created_at=user.created_at,
            ),
        )

    except Exception as e:
        return error_response({"message": str(e), "type_error": "Exception", "status_code": 500}, "api_get_user")
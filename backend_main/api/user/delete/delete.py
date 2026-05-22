from fastapi import APIRouter

from api.response import ApiErrorResponse, ApiSuccessResponse, error_response
from api.urls import USER_BY_ID
from api.user.delete.response import DeletedUserResponse
from core.handlers.user.delete.delete import handler_delete_user

router = APIRouter()


@router.delete(
    USER_BY_ID,
    tags=["User"],
    summary="Delete user",
    description="Permanently remove a user from the database.",
    response_model=ApiSuccessResponse[DeletedUserResponse, None],
    responses={
        404: {"model": ApiErrorResponse, "description": "User not found"},
        500: {"model": ApiErrorResponse, "description": "Internal server error"},
    },
)
def api_delete_user(user_id: str):
    try:
        result, error, is_valid = handler_delete_user(user_id)

        if not is_valid:
            return error_response(error, "api_delete_user")

        return ApiSuccessResponse[DeletedUserResponse, None](
            status_code=200,
            data=DeletedUserResponse(deleted=result.deleted),
        )

    except Exception as e:
        return error_response({"message": str(e), "type_error": "Exception", "status_code": 500}, "api_delete_user")

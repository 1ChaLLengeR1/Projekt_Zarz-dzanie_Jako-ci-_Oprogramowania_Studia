from fastapi import APIRouter

from api.response import ApiErrorResponse, ApiSuccessResponse, error_response
from api.urls import USER_COLLECTION
from api.user.collection.response import UserCollectionItemResponse, UserCollectionResponse
from core.handlers.user.collection.collection import handler_get_users

router = APIRouter()


@router.get(
    USER_COLLECTION,
    tags=["User"],
    summary="Get all users",
    description="Retrieve a list of all registered users.",
    response_model=ApiSuccessResponse[UserCollectionResponse, None],
    responses={
        500: {"model": ApiErrorResponse, "description": "Internal server error"},
    },
)
def api_get_users():
    try:
        users, error, is_valid = handler_get_users()

        if not is_valid:
            return error_response(error, "api_get_users")

        items = [
            UserCollectionItemResponse(
                id=u.id,
                username=u.username,
                email=u.email,
                is_active=u.is_active,
                created_at=u.created_at,
            )
            for u in users
        ]

        return ApiSuccessResponse[UserCollectionResponse, None](
            status_code=200,
            data=UserCollectionResponse(users=items, total=len(items)),
        )

    except Exception as e:
        return error_response({"message": str(e), "type_error": "Exception", "status_code": 500}, "api_get_users")

from core.repository.psql.user.one.one import get_user_by_id_psql
from core.repository.psql.user.one.response import GetUserResponse


def handler_get_user(
    user_id: str,
) -> tuple[GetUserResponse | None, dict | None, bool]:
    try:
        user_data, error, is_valid = get_user_by_id_psql(user_id)
        if not is_valid:
            return None, error, False

        response = GetUserResponse(
            id=user_data["id"],
            username=user_data["username"],
            email=user_data["email"],
            is_active=user_data["is_active"],
            created_at=user_data["created_at"],
        )
        return response, None, True

    except Exception as e:
        return None, {
            "message": str(e),
            "type_module": "handler_get_user",
            "type_error": "Exception",
            "status_code": 500,
        }, False

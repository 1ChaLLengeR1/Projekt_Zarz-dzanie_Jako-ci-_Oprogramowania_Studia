from core.repository.psql.user.collection.collection import get_users_psql
from core.repository.psql.user.collection.response import GetUsersItemResponse


def handler_get_users() -> tuple[list[GetUsersItemResponse] | None, dict | None, bool]:
    try:
        users_data, error, is_valid = get_users_psql()
        if not is_valid:
            return None, error, False

        response = [
            GetUsersItemResponse(
                id=u["id"],
                username=u["username"],
                email=u["email"],
                is_active=u["is_active"],
                created_at=u["created_at"],
            )
            for u in users_data
        ]
        return response, None, True

    except Exception as e:
        return None, {
            "message": str(e),
            "type_module": "handler_get_users",
            "type_error": "Exception",
            "status_code": 500,
        }, False

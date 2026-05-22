from core.repository.psql.user.delete.delete import delete_user_psql
from core.repository.psql.user.delete.response import DeleteUserResponse


def handler_delete_user(
    user_id: str,
) -> tuple[DeleteUserResponse | None, dict | None, bool]:
    try:
        result_data, error, is_valid = delete_user_psql(user_id)
        if not is_valid:
            return None, error, False

        response = DeleteUserResponse(deleted=result_data["deleted"])
        return response, None, True

    except Exception as e:
        return None, {
            "message": str(e),
            "type_module": "handler_delete_user",
            "type_error": "Exception",
            "status_code": 500,
        }, False

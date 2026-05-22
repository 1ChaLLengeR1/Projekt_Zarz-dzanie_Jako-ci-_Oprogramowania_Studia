from core.repository.psql.user.update.update import update_user_psql
from core.repository.psql.user.update.response import UpdateUserResponse
from core.utils.password import hash_password


def handler_update_user(
    user_id: str,
    username: str,
    email: str,
    password: str,
) -> tuple[UpdateUserResponse | None, dict | None, bool]:
    try:
        hashed = hash_password(password)
        user_data, error, is_valid = update_user_psql(user_id, username, email, hashed)
        if not is_valid:
            return None, error, False

        response = UpdateUserResponse(
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
            "type_module": "handler_update_user",
            "type_error": "Exception",
            "status_code": 500,
        }, False

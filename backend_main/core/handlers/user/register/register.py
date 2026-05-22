from core.repository.psql.user.register.register import create_user_psql
from core.repository.psql.user.register.response import CreateUserResponse
from core.utils.password import hash_password


def handler_register_user(
    username: str,
    email: str,
    password: str,
) -> tuple[CreateUserResponse | None, dict | None, bool]:
    try:
        hashed = hash_password(password)
        user_data, error, is_valid = create_user_psql(username, email, hashed)
        if not is_valid:
            return None, error, False

        response = CreateUserResponse(
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
            "type_module": "handler_register_user",
            "type_error": "Exception",
            "status_code": 500,
        }, False

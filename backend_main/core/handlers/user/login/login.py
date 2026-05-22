from core.repository.psql.user.login.login import get_user_by_email_psql
from core.repository.psql.user.login.response import LoginUserResponse
from core.utils.password import verify_password


def handler_login_user(
    email: str,
    password: str,
) -> tuple[LoginUserResponse | None, dict | None, bool]:
    try:
        user_data, error, is_valid = get_user_by_email_psql(email)
        if not is_valid:
            return None, error, False

        if not verify_password(password, user_data["password"]):
            return None, {
                "message": "Invalid credentials",
                "type_module": "handler_login_user",
                "type_error": "Unauthorized",
                "status_code": 401,
            }, False

        response = LoginUserResponse(
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
            "type_module": "handler_login_user",
            "type_error": "Exception",
            "status_code": 500,
        }, False

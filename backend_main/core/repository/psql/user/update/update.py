from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.psql.database import managed_session
from database.psql.models.user import User


def update_user_psql(
    user_id: str,
    username: str,
    email: str,
    hashed_password: str,
    db_session: Session | None = None,
) -> tuple[dict | None, dict | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            user = db.query(User).filter(User.id == user_id).first()

            if not user:
                return None, {
                    "message": "User not found",
                    "type_module": "update_user_psql",
                    "type_error": "NotFound",
                    "status_code": 404,
                }, False

            conflict = db.query(User).filter(
                User.id != user_id,
                (User.email == email) | (User.username == username),
            ).first()
            if conflict:
                field = "email" if conflict.email == email else "username"
                return None, {
                    "message": f"User with this {field} already exists",
                    "type_module": "update_user_psql",
                    "type_error": "Conflict",
                    "status_code": 409,
                }, False

            user.username = username
            user.email = email
            user.password = hashed_password
            db.commit()
            db.refresh(user)

            return {
                "id": str(user.id),
                "username": user.username,
                "email": user.email,
                "is_active": user.is_active,
                "created_at": user.created_at,
            }, None, True

    except SQLAlchemyError as e:
        return None, {
            "message": str(e),
            "type_module": "update_user_psql",
            "type_error": "SQLAlchemyError",
            "status_code": 500,
        }, False

    except Exception as e:
        return None, {
            "message": str(e),
            "type_module": "update_user_psql",
            "type_error": "Exception",
            "status_code": 500,
        }, False

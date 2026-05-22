from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.psql.database import managed_session
from database.psql.models.user import User


def get_users_psql(
    db_session: Session | None = None,
) -> tuple[list[dict] | None, dict | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            users = db.query(User).all()

            return [
                {
                    "id": str(u.id),
                    "username": u.username,
                    "email": u.email,
                    "is_active": u.is_active,
                    "created_at": u.created_at,
                }
                for u in users
            ], None, True

    except SQLAlchemyError as e:
        return None, {
            "message": str(e),
            "type_module": "get_users_psql",
            "type_error": "SQLAlchemyError",
            "status_code": 500,
        }, False

    except Exception as e:
        return None, {
            "message": str(e),
            "type_module": "get_users_psql",
            "type_error": "Exception",
            "status_code": 500,
        }, False

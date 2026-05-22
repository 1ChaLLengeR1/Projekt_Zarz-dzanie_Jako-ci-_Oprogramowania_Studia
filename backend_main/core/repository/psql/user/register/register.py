import uuid

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from database.psql.database import managed_session
from database.psql.models.user import User


def create_user_psql(
    username: str,
    email: str,
    hashed_password: str,
    db_session: Session | None = None,
) -> tuple[dict | None, dict | None, bool]:
    try:
        with managed_session(db_session) as (db, _):
            existing = db.query(User).filter(
                (User.email == email) | (User.username == username)
            ).first()

            if existing:
                field = "email" if existing.email == email else "username"
                return None, {
                    "message": f"User with this {field} already exists",
                    "type_module": "create_user_psql",
                    "type_error": "Conflict",
                    "status_code": 409,
                }, False

            user = User(
                id=str(uuid.uuid4()),
                username=username,
                email=email,
                password=hashed_password,
            )
            db.add(user)
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
            "type_module": "create_user_psql",
            "type_error": "SQLAlchemyError",
            "status_code": 500,
        }, False

    except Exception as e:
        return None, {
            "message": str(e),
            "type_module": "create_user_psql",
            "type_error": "Exception",
            "status_code": 500,
        }, False

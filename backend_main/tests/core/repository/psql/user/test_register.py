from core.repository.psql.user.register.register import create_user_psql


def test_create_success(db_session):
    result, error, is_valid = create_user_psql(
        username="newuser",
        email="new@example.com",
        hashed_password="hashed_pw",
        db_session=db_session,
    )

    assert is_valid is True
    assert error is None
    assert result["username"] == "newuser"
    assert result["is_active"] is True
    assert result["id"] is not None


def test_create_duplicate_email(test_user, db_session):
    result, error, is_valid = create_user_psql(
        username="other", email=test_user["email"], hashed_password="pw", db_session=db_session
    )

    assert is_valid is False
    assert error["status_code"] == 409


def test_create_duplicate_username(test_user, db_session):
    result, error, is_valid = create_user_psql(
        username=test_user["username"], email="other@example.com", hashed_password="pw", db_session=db_session
    )

    assert is_valid is False
    assert error["status_code"] == 409

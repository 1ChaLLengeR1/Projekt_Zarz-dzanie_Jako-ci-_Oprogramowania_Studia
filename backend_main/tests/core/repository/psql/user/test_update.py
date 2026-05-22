from core.repository.psql.user.update.update import update_user_psql


def test_update_success(test_user, db_session):
    result, error, is_valid = update_user_psql(
        user_id=test_user["id"],
        username="updated_name",
        email="updated@example.com",
        hashed_password="new_hashed_pw",
        db_session=db_session,
    )

    assert is_valid is True
    assert error is None
    assert result["username"] == "updated_name"
    assert result["email"] == "updated@example.com"
    assert result["id"] == test_user["id"]


def test_update_not_found(db_session):
    result, error, is_valid = update_user_psql(
        user_id="nonexistent-id-000",
        username="x",
        email="x@example.com",
        hashed_password="pw",
        db_session=db_session,
    )

    assert is_valid is False
    assert error["status_code"] == 404

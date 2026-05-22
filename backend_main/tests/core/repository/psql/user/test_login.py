from core.repository.psql.user.login.login import get_user_by_email_psql


def test_get_by_email_found(test_user, db_session):
    result, error, is_valid = get_user_by_email_psql(test_user["email"], db_session=db_session)

    assert is_valid is True
    assert error is None
    assert result["email"] == test_user["email"]
    assert "password" in result


def test_get_by_email_not_found(db_session):
    result, error, is_valid = get_user_by_email_psql("ghost@example.com", db_session=db_session)

    assert is_valid is False
    assert error["status_code"] == 404
    assert error["type_error"] == "NotFound"

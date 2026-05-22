from core.repository.psql.user.one.one import get_user_by_id_psql


def test_get_by_id_found(test_user, db_session):
    result, error, is_valid = get_user_by_id_psql(test_user["id"], db_session=db_session)

    assert is_valid is True
    assert error is None
    assert result["id"] == test_user["id"]
    assert result["email"] == test_user["email"]


def test_get_by_id_not_found(db_session):
    result, error, is_valid = get_user_by_id_psql("nonexistent-id-000", db_session=db_session)

    assert is_valid is False
    assert error["status_code"] == 404
    assert error["type_error"] == "NotFound"

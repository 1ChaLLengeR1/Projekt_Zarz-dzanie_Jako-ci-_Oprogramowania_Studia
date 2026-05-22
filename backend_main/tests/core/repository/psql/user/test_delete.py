from core.repository.psql.user.delete.delete import delete_user_psql


def test_delete_success(test_user, db_session):
    result, error, is_valid = delete_user_psql(test_user["id"], db_session=db_session)

    assert is_valid is True
    assert error is None
    assert result["deleted"] == test_user["id"]


def test_delete_not_found(db_session):
    result, error, is_valid = delete_user_psql("nonexistent-id-000", db_session=db_session)

    assert is_valid is False
    assert error["status_code"] == 404
    assert error["type_error"] == "NotFound"

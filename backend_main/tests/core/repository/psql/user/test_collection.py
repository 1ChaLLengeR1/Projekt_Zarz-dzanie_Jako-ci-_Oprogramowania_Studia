from core.repository.psql.user.collection.collection import get_users_psql
from core.repository.psql.user.register.register import create_user_psql


def test_get_users_empty(db_session):
    result, error, is_valid = get_users_psql(db_session=db_session)

    assert is_valid is True
    assert error is None
    assert result == []


def test_get_users_returns_all(db_session):
    create_user_psql("user1", "a@example.com", "pw", db_session=db_session)
    create_user_psql("user2", "b@example.com", "pw", db_session=db_session)

    result, error, is_valid = get_users_psql(db_session=db_session)

    assert is_valid is True
    assert len(result) == 2

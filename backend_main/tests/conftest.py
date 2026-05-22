import os

# Must be set before any project imports — database.psql.database reads them at module level
os.environ.setdefault("DB_HOST", "localhost")
os.environ.setdefault("DB_PORT", "5432")
os.environ.setdefault("DB_USER", "testuser")
os.environ.setdefault("DB_PASSWORD", "testpass")
os.environ.setdefault("DB_DBNAME", "testdb")
os.environ.setdefault("ARGON2_PEPPER", "test_pepper_only")

import pytest
from sqlalchemy import create_engine, delete
from sqlalchemy.orm import sessionmaker

from database.psql.database import Base
from database.psql.models.user import User
import database.psql.models.user  # noqa: F401 — registers model in Base.metadata

TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="session")
def engine():
    _engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
    )
    Base.metadata.create_all(_engine)
    yield _engine
    _engine.dispose()


@pytest.fixture
def db_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()
    yield session
    session.execute(delete(User))
    session.commit()
    session.close()


@pytest.fixture
def test_user(db_session):
    from core.repository.psql.user.register.register import create_user_psql

    user_data, _, _ = create_user_psql(
        username="testuser",
        email="testuser@example.com",
        hashed_password="fake_hashed_pw",
        db_session=db_session,
    )
    return user_data

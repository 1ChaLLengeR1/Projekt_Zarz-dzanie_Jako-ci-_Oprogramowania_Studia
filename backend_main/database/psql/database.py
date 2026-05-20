from collections.abc import Generator
from contextlib import contextmanager

from sqlalchemy import URL, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from core.utils.env import get_env_variable

host = get_env_variable("DB_HOST")
port = get_env_variable("DB_PORT")
user = get_env_variable("DB_USER")
password = get_env_variable("DB_PASSWORD")
dbName = get_env_variable("DB_DBNAME")

if not all([host, port, user, password, dbName]):
    raise RuntimeError("One or more database environment variables are missing.")

DATABASE_URL = URL.create(
    drivername="postgresql",
    username=user,
    password=password,
    host=host,
    port=port,
    database=dbName,
)

engine = create_engine(
    DATABASE_URL,
    pool_size=20,  # Increased from 10 to handle concurrent test requests
    max_overflow=10,  # Increased from 5 to prevent connection exhaustion
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,  # Verify connection health before use
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db() -> Generator[Session]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def managed_session(
        db_session: Session | None = None,
) -> Generator[tuple[Session, bool]]:
    if db_session is not None:
        yield db_session, True
    else:
        db = SessionLocal()
        try:
            yield db, False
        except Exception:
            db.rollback()
            raise
        finally:
            db.close()

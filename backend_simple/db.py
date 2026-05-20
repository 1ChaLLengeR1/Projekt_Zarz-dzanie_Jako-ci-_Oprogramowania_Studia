import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')

host = os.environ.get("DB_HOST")
port = os.environ.get("DB_PORT")
user = os.environ.get("DB_USER")
password = os.environ.get("DB_PASSWORD")
dbName = os.environ.get("DB_DBNAME")

if not all([host, port, user, password, dbName]):
    raise ValueError("One or more database environment variables are missing.")

data_base_url = f"postgresql://{quote_plus(user)}:{quote_plus(password)}@{host}:{port}/{dbName}"
engine = create_engine(data_base_url)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

import os

# Load env variables before any imports that trigger database.py
from config.app_config import ENV_MODE, ENV_PATH

_env_file = ENV_PATH / f"{ENV_MODE}.env"
if _env_file.exists():
    with open(_env_file, encoding="utf-8") as _f:
        for _line in _f:
            _line = _line.strip()
            if _line and not _line.startswith("#"):
                _key, _, _value = _line.partition("=")
                os.environ.setdefault(_key.strip(), _value.strip().strip('"').strip("'"))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.router import api_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH"],
    allow_headers=["*"],
)

app.include_router(api_router)
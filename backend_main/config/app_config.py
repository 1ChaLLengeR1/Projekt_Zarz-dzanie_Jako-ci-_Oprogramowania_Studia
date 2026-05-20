from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent

ENV_PATH = BASE_DIR / "env"

# local, stg, prod — controlled by ENV_MODE environment variable
ENV_MODE = "local"

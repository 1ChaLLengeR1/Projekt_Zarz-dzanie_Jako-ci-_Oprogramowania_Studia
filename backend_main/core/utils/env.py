import os


def get_env_variable(name_env: str, default: str | None = None) -> str:
    value = os.getenv(name_env)

    if value is not None:
        return value.strip().strip('"').strip("'").strip()

    if default is not None:
        return default

    raise RuntimeError(f"Missing required environment variable: {name_env}")

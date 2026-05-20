FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PROJECT_ROOT=/app

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml ./

COPY . /app/

RUN uv pip install --system -e ".[test]"

RUN find /app -type f -name "*.sh" -exec sed -i 's/\r$//' {} \; && \
    find /app -type f -name "*.sh" -exec chmod +x {} \; && \
    find /app -type f -name "*.env" -exec sed -i 's/\r$//' {} \; 2>/dev/null || true
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PROJECT_ROOT=/app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libjpeg-dev \
    zlib1g-dev \
    libpq-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml ./

COPY . /app/

RUN uv pip install --system -e ".[test]"

RUN find /app -type f -name "*.sh" -exec sed -i 's/\r$//' {} \; 2>/dev/null || true && \
    find /app -type f -name "*.sh" -exec chmod +x {} \; 2>/dev/null || true

CMD ["pytest", "-v", "-s"]
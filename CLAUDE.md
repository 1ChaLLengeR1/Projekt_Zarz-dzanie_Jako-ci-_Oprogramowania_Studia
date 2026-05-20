# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **educational Software Quality Management project** demonstrating two contrasting implementation approaches to the same requirements (User CRUD + Authorization):

- **`backend_simple`** — "Quick & Dirty" legacy approach showcasing antipatterns and technical debt
- **`backend_main`** — "Production-Ready" modern approach showcasing best practices

The goal is to illustrate the impact of software quality decisions on the SDLC. Both backends are intentionally different by design — do not normalize them toward each other.

## Running the Project

Both backends are orchestrated via Docker Compose:

```bash
docker-compose up
```

API documentation (Swagger UI) for `backend_main` is available at `/docs` once running.

## backend_main — Modern Architecture

Stack: FastAPI, Pydantic, SQLAlchemy, Alembic, Poetry, Argon2

```bash
# Install dependencies (from backend_main/)
poetry install

# Run database migrations
alembic upgrade head

# Start the server
uvicorn src.main:app --reload

# Run tests
pytest

# Static analysis
ruff check .
mypy .
bandit -r src/
```

### Architecture (DDD / Hexagonal)

```
backend_main/src/
├── api/            # HTTP layer: FastAPI routers, request/response schemas
├── domain/         # Pure business logic, entities, domain models (no I/O)
├── services/       # Application services / Use Cases (orchestrate domain)
└── infrastructure/ # DB session, SQLAlchemy models, Alembic, repositories
```

Data flows inward: `api → services → domain`, with `infrastructure` injected via dependency inversion. Domain layer has no dependencies on infrastructure or HTTP concerns.

## backend_simple — Legacy Antipatterns

Stack: Flask or FastAPI (minimal), plain `requirements.txt`, single-file monolith

All logic lives in `main.py` — no layer separation, no migrations, plaintext passwords, root Docker user. This is intentional for demonstration purposes.

## Key Quality Contrasts to Preserve

| Concern | backend_simple | backend_main |
|---|---|---|
| Architecture | Monolithic `main.py` | Layered DDD |
| Validation | Manual `if/else` or none | Pydantic models |
| Error handling | Unhandled 500s | Global exception handler |
| DB management | Hardcoded schema | Alembic versioned migrations |
| Passwords | Plaintext | Argon2 hashing |
| Logging | `print()` | Structured JSON |
| Docker | Single-stage, root user | Multi-stage, non-root |
| Dependencies | Unpinned `requirements.txt` | `poetry.lock` |
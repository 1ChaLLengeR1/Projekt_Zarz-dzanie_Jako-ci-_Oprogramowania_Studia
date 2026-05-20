install:
	uv sync --all-extras

clean:
	rm -rf .venv uv.lock .uv __pycache__ .pytest_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete


# ============================================================================
# Alembic
# ============================================================================

migrate:
	uv run alembic upgrade head

migrate_down:
	uv run alembic downgrade -1

migrate_base:
	uv run alembic downgrade base


# ============================================================================
# Dev server
# ============================================================================

run:
	uv run uvicorn main:app --reload


# ============================================================================
# Docker Compose (local)
# ============================================================================

COMPOSE_FILE = infra/dockerfiles/compose/local-docker-compose.yml

up:
	docker-compose -f $(COMPOSE_FILE) up -d

up_build:
	docker-compose -f $(COMPOSE_FILE) up -d --build

down:
	docker-compose -f $(COMPOSE_FILE) down -v

logs:
	docker-compose -f $(COMPOSE_FILE) logs -f


# ============================================================================
# Code Quality
# ============================================================================

lint:
	@echo "Linting code..."
	@uv run ruff check .

format:
	@echo "Formatting code..."
	@uv run ruff format .

fix:
	@echo "Auto-fixing all issues..."
	@uv run ruff check --fix .
	@uv run ruff format .
	@echo "Done!"

check:
	@echo "Running all checks..."
	@uv run ruff check .
	@uv run ruff format --check .
	@echo "All checks passed!"


# ============================================================================
# Tests
# ============================================================================

test:
	uv run pytest -s -v

test_full:
	uv run pytest -s -v -m ""
# backend_main — Production-Ready API

Implementacja referencyjna REST API dla zarządzania użytkownikami i autoryzacji, zbudowana zgodnie z zasadami **Clean Code**, **Domain-Driven Design** i inżynierii produkcyjnej. Stanowi kontrast jakościowy do `backend_simple`.

---

## Cel

Pokazanie, jak wygląda kod gotowy na środowisko produkcyjne: warstwowa architektura, pełna konteneryzacja, bezpieczne hashowanie haseł, wersjonowane migracje bazy danych i potok CI/CD z bramkami jakości.

---

## Uruchomienie

### Lokalnie (bez Dockera)

```bash
# Instalacja zależności
make install

# env/local.env → DB_HOST="localhost"

# Migracje bazy danych
./infra/scripts/database/migration_up.sh local

# Serwer deweloperski
make run
# http://127.0.0.1:8000/docs
```

### Docker (app + PostgreSQL w kontenerze)

```bash
make up_build   # Zbuduj i uruchom
make logs       # Podgląd logów
make down       # Zatrzymaj i usuń volumeny
```

Swagger UI: `http://127.0.0.1:8000/docs`

---

## Endpointy

| Metoda | Ścieżka | Opis |
| :--- | :--- | :--- |
| `POST` | `/api/v1/user/login` | Logowanie użytkownika |

---

## Zmienne środowiskowe (`env/local.env`)

| Zmienna | Opis |
| :--- | :--- |
| `DB_HOST` | `localhost` lokalnie / `postgresql` w Dockerze |
| `DB_PORT` | Port PostgreSQL (domyślnie `5432`) |
| `DB_USER` | Użytkownik bazy danych |
| `DB_PASSWORD` | Hasło do bazy danych |
| `DB_DBNAME` | Nazwa bazy danych |
| `ARGON2_PEPPER` | Sekretny pepper do hashowania haseł Argon2 |
| `POSTGRES_USER` | Użytkownik inicjalizujący kontener PostgreSQL |
| `POSTGRES_PASSWORD` | Hasło inicjalizujące kontener PostgreSQL |
| `POSTGRES_DB` | Baza danych inicjalizowana w kontenerze PostgreSQL |

---

## Struktura projektu

```
backend_main/
│
├── main.py                          # Punkt wejścia FastAPI — CORS, router, ładowanie env
├── pyproject.toml                   # Zależności (uv), metadane projektu
├── alembic.ini                      # Konfiguracja Alembic
├── Makefile                         # Skróty CLI
│
├── api/                             # Warstwa HTTP
│   ├── response.py                  # Generyczne schematy (ApiSuccessResponse, ApiErrorResponse)
│   ├── router.py                    # Główny APIRouter aggregujący routery modułów
│   ├── urls.py                      # Stałe URL endpointów
│   └── user/
│       ├── login.py                 # POST /api/v1/user/login
│       ├── payload.py               # Schema wejściowa (LoginPayload: email + password)
│       └── response.py              # Schema wyjściowa (UserResponse bez pola password)
│
├── core/                            # Logika aplikacyjna
│   ├── handlers/
│   │   └── user/
│   │       └── user.py              # Handler — orchestruje repo + weryfikację hasła
│   ├── repository/
│   │   └── psql/
│   │       └── user/
│   │           └── login/
│   │               ├── login.py     # Zapytanie do bazy — pobierz usera po email
│   │               └── response.py  # Dataclass LoginUserResponse (bez password)
│   └── utils/
│       ├── env.py                   # get_env_variable() — bezpieczne czytanie env
│       └── password.py              # verify_password() — Argon2 + pepper
│
├── database/
│   └── psql/
│       ├── database.py              # Engine SQLAlchemy, SessionLocal, managed_session()
│       ├── models/
│       │   └── user.py              # Model ORM User
│       ├── migrations/
│       │   ├── env.py               # Środowisko Alembic
│       │   ├── script.py.mako       # Szablon migracji
│       │   └── versions/
│       │       └── 0001_init.py     # Tworzenie tabeli users
│       └── sql/
│           ├── database_up.sql      # Rozszerzenia PostgreSQL (uuid-ossp)
│           ├── database_down.sql    # DROP TABLE users CASCADE
│           └── user.sql             # Seed domyślnego admina
│
├── config/
│   └── app_config.py                # ENV_MODE, ścieżki bazowe
│
├── env/
│   ├── local.env                    # Środowisko lokalne
│   └── stg.env                      # Środowisko staging
│
├── infra/
│   ├── dockerfiles/
│   │   ├── compose/
│   │   │   └── local-docker-compose.yml   # Docker Compose: app + PostgreSQL
│   │   └── dockerfile/
│   │       ├── local.dockerfile     # Dev: python-slim + uv + postgresql-client
│   │       ├── prod.dockerfile      # Prod: gunicorn
│   │       ├── migration.dockerfile # Migracje w CI
│   │       └── test.dockerfile      # Testy w CI
│   └── scripts/
│       ├── load_env.sh              # Ładuje i waliduje .env
│       ├── run_mode.sh              # Przełącza ENV_MODE
│       └── database/
│           ├── migration_up.sh      # extensions → alembic → seed
│           ├── migration_down.sh    # DROP TABLE
│           ├── copy_user.sh         # INSERT admina z user.sql
│           └── docker_entrypoint.sh # Entrypoint kontenera: migracje → uvicorn
│
└── .github/
    └── workflows/
        ├── ci.yml                   # Lint + testy przy push/PR
        ├── cd.yml                   # Build obrazu + deploy
        ├── main.yml                 # Główny workflow
        └── test.yml                 # Testy z DB w kontenerze
```

---

## Architektura

```
HTTP Request
     ↓
[api/user/login.py]           ← warstwa HTTP (FastAPI, Pydantic schemas)
     ↓
[core/handlers/user.py]       ← warstwa aplikacyjna (orchestracja)
     ↓
[core/repository/psql/...]    ← warstwa danych (SQLAlchemy queries)
     ↓
[database/psql/database.py]   ← infrastruktura (engine, session, ORM)
```

Każda funkcja w warstwie danych i aplikacyjnej zwraca `tuple[data | None, error | None, bool]` — spójny kontrakt dla całej aplikacji bez rzucania wyjątków przez warstwy.

---

## Bezpieczeństwo

| Aspekt | Rozwiązanie |
| :--- | :--- |
| Hashowanie haseł | **Argon2id** — zwycięzca Password Hashing Competition 2015 |
| Pepper | Sekret spoza bazy, w zmiennych środowiskowych |
| Walidacja wejścia | **Pydantic EmailStr** — format email weryfikowany automatycznie |
| Odpowiedź API | Pole `password` nigdy nie trafia do odpowiedzi |
| CORS | Ograniczony origin (`localhost:3000`), metody (`GET, POST, PUT, PATCH`) |

---

## Zarządzanie bazą danych

```bash
make migrate        # alembic upgrade head
make migrate_down   # alembic downgrade -1
make migrate_base   # alembic downgrade base

./infra/scripts/database/migration_up.sh local    # Pełna inicjalizacja
./infra/scripts/database/migration_down.sh local  # Rollback
```

---

## Jakość kodu

```bash
make lint     # Ruff check
make format   # Ruff format
make fix      # Auto-fix
make check    # Wszystkie sprawdzenia (bez modyfikacji)
```

---

## Komendy Makefile

| Komenda | Opis |
| :--- | :--- |
| `make install` | Instalacja zależności |
| `make run` | Serwer deweloperski |
| `make up_build` | Docker Compose z buildem |
| `make up` | Docker Compose w tle |
| `make down` | Stop + usuń volumeny |
| `make logs` | Logi kontenerów |
| `make migrate` | Alembic upgrade head |
| `make migrate_down` | Alembic downgrade -1 |
| `make migrate_base` | Alembic downgrade base |
| `make lint` | Ruff check |
| `make format` | Ruff format |
| `make fix` | Auto-fix |
| `make check` | Wszystkie sprawdzenia |
| `make test` | Testy jednostkowe |
| `make test_full` | Pełny zestaw testów |
| `make clean` | Usuń .venv, cache, pyc |

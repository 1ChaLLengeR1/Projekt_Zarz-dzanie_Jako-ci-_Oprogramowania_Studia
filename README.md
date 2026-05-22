# Software Quality Management: A Comparative Study
### Case Study: Legacy "Quick & Dirty" vs. Modern "Production-Ready" Architecture

## 1. Cel projektu
Projekt został stworzony w celu zademonstrowania różnic w jakości oprogramowania oraz ich wpływu na cykl życia produktu (SDLC). Przedstawia on dwa podejścia do realizacji tego samego zestawu wymagań biznesowych (CRUD użytkowników + Autoryzacja):

1.  **`backend_simple`**: Skupiony na szybkości dostarczenia (Time-to-Market) kosztem długu technicznego.
2.  **`backend_main`**: Skupiony na wysokiej jakości, skalowalności i łatwości utrzymania (Maintainability).

---

## 2. Porównanie jakościowe (Quality Matrix)

| Cecha | `backend_simple` (Legacy) | `backend_main` (Modern) |
| :--- | :--- | :--- |
| **Architektura** | Monolit spaghetti (wszystko w jednym) | **Domain-Driven Design (DDD)** / Hexagonal |
| **Walidacja danych** | Brak lub ręczne `if/else` | **Pydantic (BaseModel)** — silne typowanie |
| **Obsługa błędów** | Standardowe 500-tki (crash-prone) | `ApiErrorResponse` z `type_module`, `type_error`, kodem HTTP |
| **Dokumentacja API** | Brak response model, brak opisów | `response_model` + `responses` na każdym endpoincie, Swagger UI |
| **Testy automatyczne** | Brak — kod jest silnie sprzężony | Testy jednostkowe warstwy repo (SQLite in-memory, pytest) |
| **Zarządzanie DB** | Brak (hardcoded schema) | **Alembic** (wersjonowane migracje) |
| **Bezpieczeństwo** | Brak (plaintext passwords, root user) | **Argon2id** + pepper, non-root Docker user |
| **Observability** | `print()` w konsoli | **Structured Logging** (JSON format) |
| **DevOps** | Single-stage Dockerfile | **Multi-stage Build**, `.dockerignore`, Healthchecks |

---

## 3. Szczegóły implementacji

### 🔴 backend_simple (Antywzorce)
Ten moduł reprezentuje podejście "byle działało". Główne problemy z punktu widzenia jakości:
* **Brak separacji warstw:** Logika bazy danych jest wymieszana z logiką HTTP.
* **Dług techniczny:** Użycie `requirements.txt` bez przypiętych wersji sprawia, że buildy są niepowtarzalne.
* **Brak testowalności:** Kod jest silnie sprzężony (tightly coupled), co uniemożliwia testy jednostkowe.
* **Brak dokumentacji API:** Endpointy nie mają response model — Swagger pokazuje puste odpowiedzi.
* **Zagrożenie bezpieczeństwa:** Brak walidacji wejścia, hasła w plaintekście, brak Graceful Shutdown.

### 🟢 backend_main (Best Practices)
Moduł implementujący zasady **Clean Code** oraz nowoczesne standardy inżynierii:
* **Architektura warstwowa:**
    * `api/` — kontrolery FastAPI, schematy żądań i odpowiedzi (Pydantic)
    * `core/` — handlery biznesowe i repozytoria psql (czysta logika, bez HTTP)
    * `database/` — modele SQLAlchemy, migracje Alembic, sesja
* **Dokumentacja API:** Każdy endpoint ma `response_model`, `summary`, `description` oraz `responses` z kodami błędów — Swagger UI pod `/docs` jest kompletny.
* **Testy automatyczne:** Warstwa repozytorium pokryta testami jednostkowymi (pytest + SQLite in-memory). Każda operacja psql ma dedykowany plik testowy w `tests/core/repository/psql/user/`.
* **Statyczna analiza kodu:** Przygotowane pod narzędzia takie jak **Ruff**, **Mypy** oraz **Bandit**.
* **Automatyzacja procesów:** Skrypty migracyjne, `Makefile` z 15+ targetami, konteneryzacja zoptymalizowana pod środowiska produkcyjne.

---

## 4. Perspektywa DevOps & CI/CD
W podejściu jakościowym (`backend_main`) proces wdrożeniowy jest integralną częścią oprogramowania:

1.  **Lintery & Formattery:** Kod przechodzi przez bramki jakości (Quality Gates).
2.  **Container Security:** Obraz Dockerowy budowany jest w oparciu o obrazy typu `slim` z minimalnym footprintem bezpieczeństwa.
3.  **Dependency Management:** Wykorzystanie `uv.lock` gwarantuje deterministyczne budowanie artefaktów.

---

## 5. Struktura katalogów
```text
.
├── backend_simple/                 # Prezentacja długu technicznego
│   ├── main.py                     # Wszystko w jednym pliku (routing, logika, DB)
│   ├── db.py                       # Sesja bazy danych
│   ├── models.py                   # Modele ORM
│   ├── urls.py                     # Endpointy bez response model
│   ├── requirements.txt            # Luźne wersje zależności
│   └── Dockerfile                  # Nieoptymalny obraz (Root)
│
├── backend_main/                   # Standard produkcyjny
│   ├── api/
│   │   ├── user/
│   │   │   ├── login/              # POST /api/v1/user/login
│   │   │   ├── register/           # POST /api/v1/user/register
│   │   │   ├── one/                # GET  /api/v1/user/{user_id}
│   │   │   ├── collection/         # GET  /api/v1/user/collection
│   │   │   ├── update/             # PUT  /api/v1/user/{user_id}
│   │   │   └── delete/             # DELETE /api/v1/user/{user_id}
│   │   ├── response.py             # ApiSuccessResponse, ApiErrorResponse, error_response()
│   │   ├── router.py               # Agregacja routerów
│   │   └── urls.py                 # Stałe URL
│   ├── core/
│   │   ├── handlers/user/          # Logika biznesowa (login, register, one, ...)
│   │   ├── repository/psql/user/   # Dostęp do bazy (login, register, one, ...)
│   │   └── utils/                  # password.py (Argon2), env.py
│   ├── database/psql/              # Modele SQLAlchemy, migracje Alembic, sesja
│   ├── tests/
│   │   ├── conftest.py             # Fixtures: engine (SQLite), db_session, test_user
│   │   └── core/repository/psql/user/
│   │       ├── test_login.py
│   │       ├── test_register.py
│   │       ├── test_one.py
│   │       ├── test_collection.py
│   │       ├── test_update.py
│   │       └── test_delete.py
│   ├── pyproject.toml              # Zarządzanie zależnościami (uv)
│   ├── Makefile                    # Standaryzacja komend
│   └── Dockerfile                  # Multi-stage build (Quality-focused)
│
└── docker-compose.yml              # Infrastruktura do uruchomienia obu systemów
```

---

## 6. Szczegółowe porównanie jakości implementacji

### 6.1 Architektura i struktura kodu

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Organizacja plików | Płaski katalog, wszystko w `main.py` | Warstwowa: `api/` → `core/` → `database/` |
| Separacja odpowiedzialności | Brak — HTTP, logika i baza w jednym miejscu | Pełna — każda warstwa zna tylko swoją rolę |
| Wzorzec architektoniczny | Monolit (Spaghetti Architecture) | Layered Architecture z elementami DDD |
| Testowalność | Niemożliwa — silne sprzężenie (tight coupling) | Możliwa — każda warstwa testowalna izolowanie |
| Kontrakt danych między warstwami | Brak — surowe obiekty ORM | `tuple[data, error, bool]` — spójny dla całej aplikacji |

### 6.2 Bezpieczeństwo

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Przechowywanie haseł | **Plaintext** w bazie danych | **Argon2id** + pepper z env |
| Hashowanie | Brak | Argon2id (winner Password Hashing Competition 2015) |
| Ekspozycja danych | `GET /users/all` zwraca hasła w plaintekście | Pole `password` nigdy nie wychodzi z serwera |
| Walidacja wejścia | Pydantic bez walidatorów formatu | `EmailStr`, typy silne, walidacja na poziomie schematu |
| CORS | `allow_origins=["*"]` — każda domena | Tylko `localhost:3000`, tylko wymagane metody HTTP |
| Autoryzacja | Brak — każdy endpoint publiczny | Endpoint logowania jako fundament pod JWT |

### 6.3 Obsługa błędów

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Strategia | Brak — domyślne HTTP 500 | `tuple[data, error, bool]` — błędy jako wartości |
| Kody HTTP | Zawsze 500 przy wyjątku | Semantyczne: 404, 401, 409, 500 |
| Odpowiedź błędu | Stack trace lub pusta odpowiedź | Ustrukturyzowany `ApiErrorResponse` z `type_module`, `type_error` |
| Logowanie błędów | `print()` | Strukturalne logowanie (gotowe pod JSON logger) |

### 6.4 Dokumentacja API

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Response model | Brak — Swagger pokazuje puste odpowiedzi | `response_model=ApiSuccessResponse[...]` na każdym endpoincie |
| Opisy endpointów | Brak `summary` i `description` | Każdy endpoint z `summary`, `description`, tagiem |
| Kody błędów w Swagger | Niewidoczne | `responses={404: ..., 409: ..., 500: ...}` — pełna specyfikacja |
| Funkcja pomocnicza błędów | Brak — duplikacja kodu | Wspólna `error_response()` w `api/response.py` |
| Swagger UI | Dostępny, ale niekompletny | Kompletny pod `/docs` — opis każdego przypadku |

### 6.5 Testy automatyczne

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Pokrycie testami | **0%** — brak jakichkolwiek testów | Warstwa repo pokryta testami jednostkowymi |
| Izolacja testów | N/A | SQLite in-memory — testy bez uruchomionego PostgreSQL |
| Fixtures | N/A | `engine` (session), `db_session` (function), `test_user` |
| Liczba testów | 0 | 13 testów — po 2–3 na każdą operację psql |
| Uruchomienie | N/A | `make test` lub `uv run pytest -s -v` |
| Konfiguracja | N/A | `pyproject.toml` `[tool.pytest.ini_options]` + `conftest.py` |

### 6.6 Baza danych i migracje

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Inicjalizacja schematu | `Base.metadata.create_all()` przy starcie — nieodwracalne | **Alembic** — wersjonowane, odwracalne migracje |
| Historia zmian | Brak — schemat "magicznie" pojawia się | Każda zmiana jako plik migracji w `versions/` |
| Rollback | Niemożliwy | `alembic downgrade -1` / `downgrade base` |
| Sesja bazy danych | `session = SessionLocal()` globalnie — wyciek pamięci | `managed_session()` — context manager z rollback |
| Connection pool | Brak konfiguracji | `pool_size=20`, `max_overflow=10`, `pool_pre_ping=True` |

### 6.7 Konteneryzacja i DevOps

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Dockerfile | Single-stage, uruchomienie jako **root** | Multi-stage build, non-root user |
| `.dockerignore` | Brak — wszystkie pliki trafiają do obrazu | Obecny — minimalizuje rozmiar i wyciek sekretów |
| Health check | Brak | `pg_isready` — baza startuje zanim aplikacja |
| Docker Compose | App + PostgreSQL bez health check | App + PostgreSQL z `condition: service_healthy` |
| Zmienne środowiskowe | Plik `.env` bez separacji środowisk | `env/local.env`, `env/stg.env` — separacja środowisk |

### 6.8 Zarządzanie zależnościami

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Format | `requirements.txt` bez wersji lock | `pyproject.toml` + `uv.lock` |
| Powtarzalność budowania | Brak — `pip install` pobierze najnowsze wersje | Deterministyczny — `uv sync --frozen` |
| Narzędzie | `pip` | `uv` — 10–100x szybszy od pip |
| Grupy zależności | Brak | `dependencies`, `dev`, `prod` — minimalne środowisko produkcyjne |

### 6.9 CI/CD i automatyzacja

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Pipeline | 1 workflow: build → SSH deploy | Osobne: `ci.yml` (lint+test), `cd.yml` (deploy) |
| Bramki jakości | Brak | Lint (Ruff), testy, sprawdzenie typów |
| Testy w CI | Brak | `test.yml` z bazą PostgreSQL w kontenerze |
| Deploy | `docker-compose up` bez weryfikacji | Health check po deploymencie |
| Makefile | Brak | 15+ targets — standaryzacja komend dla całego zespołu |

---

## 7. Wnioski jakościowe

### Koszt długu technicznego (`backend_simple`)

`backend_simple` reprezentuje podejście **"działa na moim komputerze"**. Każdy skrót podjęty na etapie developmentu generuje koszt na późniejszych etapach SDLC:

- **Plaintext hasła** → naruszenie danych = katastrofa wizerunkowa i prawna (RODO)
- **Brak migracji** → każda zmiana schematu wymaga ręcznego `DROP TABLE` na produkcji
- **Globalna sesja DB** → wyciek pamięci ujawnia się dopiero pod obciążeniem
- **Brak testów** → refaktoryzacja niemożliwa bez ryzyka regresji
- **Brak response model** → Swagger jest bezużyteczny — konsumenci API nie wiedzą, czego się spodziewać
- **Root w Dockerze** → podatność na container escape — przejęcie całego hosta

### Wartość inwestycji w jakość (`backend_main`)

`backend_main` wymaga więcej czasu na start, ale każda decyzja architektoniczna **procentuje**:

- **Warstwowa architektura** → nowy developer rozumie strukturę w 15 minut, nie 3 godziny
- **Alembic** → zmiana schematu bazy = jeden plik migracji, rollback jedną komendą
- **Argon2id** → bezpieczeństwo haseł zgodne ze standardami OWASP 2024
- **Pydantic + response_model** → błędy walidacji wykrywane przed dotarciem do bazy; Swagger generuje kompletną dokumentację automatycznie
- **Testy jednostkowe (SQLite in-memory)** → refaktoryzacja bez strachu, regresje wykrywane natychmiast, CI nie wymaga uruchomionej bazy
- **Makefile + skrypty** → onboarding nowego developera = `make install && make run`

### Podsumowanie metryczne

| Metryka | backend_simple | backend_main |
| :--- | :--- | :--- |
| Liczba plików Python | ~6 | ~50+ |
| Warstwy architektury | 1 (monolit) | 3 (api, core, database) |
| Testy automatyczne | **0** | **13 testów** (6 plików, każda operacja psql) |
| Pokrycie warstwy repo | 0% | ~100% (happy path + error path) |
| Dokumentacja endpointów w Swagger | Niekompletna | Kompletna (response_model + kody błędów) |
| Krytyczne podatności bezpieczeństwa | 5+ | 0 |
| Czas onboardingu nowego developera | Wysoki (brak dokumentacji procesu) | Niski (`make install && make run`) |
| Możliwość rollback schematu DB | Nie | Tak (`alembic downgrade`) |
| Deterministyczność budowania | Nie | Tak (`uv.lock`) |

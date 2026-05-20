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
| **Walidacja danych** | Brak lub ręczne `if/else` | **Pydantic (BaseModel)** - silne typowanie |
| **Obsługa błędów** | Standardowe 500-tki (crash-prone) | **Global Exception Handler** (czytelne kody HTTP) |
| **Zarządzanie DB** | Brak (hardcoded schema) | **Alembic** (wersjonowane migracje) |
| **Bezpieczeństwo** | Brak (plaintext passwords, root user) | **Argon2 hashing**, **Non-root Docker user** |
| **Observability** | `print()` w konsoli | **Structured Logging** (JSON format) |
| **DevOps** | Single-stage Dockerfile | **Multi-stage Build**, `.dockerignore`, Healthchecks |

---

## 3. Szczegóły implementacji

### 🔴 backend_simple (Antywzorce)
Ten moduł reprezentuje podejście "byle działało". Główne problemy z punktu widzenia jakości:
* **Brak separacji warstw:** Logika bazy danych jest wymieszana z logiką HTTP.
* **Dług techniczny:** Użycie `requirements.txt` bez przypiętych wersji sprawia, że buildy są niepowtarzalne.
* **Brak testowalności:** Kod jest silnie sprzężony (tightly coupled), co uniemożliwia testy jednostkowe.
* **Zagrożenie bezpieczeństwa:** Brak walidacji wejścia oraz brak obsługi sygnałów systemowych (Graceful Shutdown).

### 🟢 backend_main (Best Practices)
Moduł implementujący zasady **Clean Code** oraz nowoczesne standardy inżynierii:
* **Architektura warstwowa:** * `Domain`: Czysta logika biznesowa i encje.
    * `Application`: Serwisy (Use Cases).
    * `Infrastructure`: Implementacja bazy danych, repozytoria, adaptery.
* **Statyczna analiza kodu:** Przygotowane pod narzędzia takie jak **Ruff**, **Mypy** oraz **Bandit**.
* **Automatyzacja procesów:** Skrypty migracyjne oraz konteneryzacja zoptymalizowana pod środowiska produkcyjne.
* **Dokumentacja:** Automatycznie generowana specyfikacja **OpenAPI (Swagger)** dostępna pod `/docs`.

---

## 4. Perspektywa DevOps & CI/CD
W podejściu jakościowym (`backend_main`) proces wdrożeniowy jest integralną częścią oprogramowania:

1.  **Lintery & Formattery:** Kod przechodzi przez bramki jakości (Quality Gates).
2.  **Container Security:** Obraz Dockerowy budowany jest w oparciu o obrazy typu `slim` z minimalnym footprintem bezpieczeństwa.
3.  **Dependency Management:** Wykorzystanie `poetry.lock` lub `pip-compile` gwarantuje deterministyczne budowanie artefaktów.

---

## 5. Struktura katalogów
```text
.
├── backend_simple/         # Prezentacja długu technicznego
│   ├── main.py             # Wszystko w jednym pliku
│   ├── requirements.txt    # Luźne wersje zależności
│   └── Dockerfile          # Nieoptymalny obraz (Root)
│
├── backend_main/           # Standard produkcyjny
│   ├── src/
│   │   ├── api/            # Kontrolery i Routing
│   │   ├── domain/         # Logika biznesowa i modele
│   │   ├── infrastructure/ # Baza danych, migracje, adaptery
│   │   └── services/       # Serwisy aplikacyjne
│   ├── migrations/         # Skrypty bazy danych (Alembic)
│   ├── tests/              # Testy jednostkowe i integracyjne
│   ├── pyproject.toml      # Zarządzanie zależnościami
│   └── Dockerfile          # Multi-stage build (Quality-focused)
│
└── docker-compose.yml      # Infrastruktura do uruchomienia obu systemów
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
| CORS | `allow_origins=["*"]` — każda domena | Tylko `localhost:3000`, tylko 4 metody HTTP |
| Autoryzacja | Brak — każdy endpoint publiczny | Endpoint logowania jako fundament pod JWT |

### 6.3 Obsługa błędów

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Strategia | Brak — domyślne HTTP 500 | `tuple[data, error, bool]` — błędy jako wartości |
| Kody HTTP | Zawsze 500 przy wyjątku | Semantyczne: 404, 401, 409, 500 |
| Odpowiedź błędu | Stack trace lub pusta odpowiedź | Ustrukturyzowany `ApiErrorResponse` z `type_module`, `type_error` |
| Logowanie błędów | `print()` | Strukturalne logowanie (gotowe pod JSON logger) |

### 6.4 Baza danych i migracje

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Inicjalizacja schematu | `Base.metadata.create_all()` przy starcie — nieodwracalne | **Alembic** — wersjonowane, odwracalne migracje |
| Historia zmian | Brak — schemat "magicznie" pojawia się | Każda zmiana jako plik migracji w `versions/` |
| Rollback | Niemożliwy | `alembic downgrade -1` / `downgrade base` |
| Sesja bazy danych | `session = SessionLocal()` globalnie — wyciek pamięci | `managed_session()` — context manager z rollback |
| Connection pool | Brak konfiguracji | `pool_size=20`, `max_overflow=10`, `pool_pre_ping=True` |
| Seed danych | Brak | `user.sql` + `copy_user.sh` — reproducible seed |

### 6.5 Konteneryzacja i DevOps

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Dockerfile | Single-stage, uruchomienie jako **root** | Dedykowane obrazy: `local`, `prod`, `migration`, `test` |
| Użytkownik w kontenerze | `root` — krytyczne zagrożenie bezpieczeństwa | Non-root (best practice) |
| `.dockerignore` | Brak — wszystkie pliki trafiają do obrazu | Obecny — minimalizuje rozmiar i wyciek sekretów |
| Health check | Brak | `pg_isready` — baza startuje zanim aplikacja |
| Docker Compose | App + PostgreSQL + nginx (brak health check) | App + PostgreSQL z `condition: service_healthy` |
| Entrypoint | Statyczny `CMD` | `docker_entrypoint.sh` — migracje przy każdym starcie |
| Zmienne środowiskowe | Plik `.env` bez separacji środowisk | `env/local.env`, `env/stg.env` — separacja środowisk |

### 6.6 Zarządzanie zależnościami

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Format | `requirements.txt` bez wersji lock | `pyproject.toml` + `uv.lock` |
| Powtarzalność budowania | Brak — `pip install` pobierze najnowsze wersje | Deterministyczny — `uv sync --frozen` |
| Narzędzie | `pip` | `uv` — 10-100x szybszy od pip |
| Grupy zależności | Brak | `dependencies`, `dev`, `prod` — minimalne środowisko produkcyjne |

### 6.7 CI/CD i automatyzacja

| Kryterium | backend_simple | backend_main |
| :--- | :--- | :--- |
| Pipeline | 1 workflow: build → SSH deploy | Osobne: `ci.yml` (lint+test), `cd.yml` (deploy) |
| Bramki jakości | Brak | Lint (Ruff), testy, sprawdzenie typów |
| Testy w CI | Brak | `test.yml` z bazą PostgreSQL w kontenerze |
| Deploy | `docker-compose up` bez weryfikacji | Health check po deploymencie |
| Skrypty operacyjne | Brak | `migration_up.sh`, `migration_down.sh`, `run_mode.sh` |
| Makefile | Brak | 15 targets — standaryzacja komend dla całego zespołu |

---

## 7. Wnioski jakościowe

### Koszt długu technicznego (`backend_simple`)

`backend_simple` reprezentuje podejście **"działa na moim komputerze"**. Każdy skrót podjęty na etapie developmentu generuje koszt na późniejszych etapach SDLC:

- **Plaintext hasła** → naruszenie danych = katastrofa wizerunkowa i prawna (RODO)
- **Brak migracji** → każda zmiana schematu wymaga ręcznego `DROP TABLE` na produkcji
- **Globalna sesja DB** → wyciek pamięci ujawnia się dopiero pod obciążeniem
- **Brak testów** → refaktoryzacja niemożliwa bez ryzyka regresji
- **Root w Dockerze** → podatność na container escape — przejęcie całego hosta

### Wartość inwestycji w jakość (`backend_main`)

`backend_main` wymaga więcej czasu na start, ale każda decyzja architektoniczna **procentuje**:

- **Warstwowa architektura** → nowy developer rozumie strukturę w 15 minut, nie 3 godziny
- **Alembic** → zmiana schematu bazy = jeden plik migracji, rollback jedną komendą
- **Argon2id** → bezpieczeństwo haseł zgodne ze standardami OWASP 2024
- **Pydantic** → błędy walidacji wykrywane przed dotarciem do bazy danych
- **Makefile + skrypty** → onboarding nowego developera = `make install && make run`
- **CI/CD z bramkami** → błędy wykrywane automatycznie, zanim trafią na główną gałąź

### Podsumowanie metryczne

| Metryka | backend_simple | backend_main |
| :--- | :--- | :--- |
| Liczba plików Python | ~6 | ~20 |
| Warstwy architektury | 1 (monolit) | 4 (api, core, database, infra) |
| Pokrycie testami | 0% | Gotowe na testy |
| Krytyczne podatności bezpieczeństwa | 5+ | 0 |
| Czas onboardingu nowego developera | Wysoki (brak dokumentacji procesu) | Niski (`make install && make run`) |
| Możliwość rollback schematu DB | Nie | Tak (`alembic downgrade`) |
| Deterministyczność budowania | Nie | Tak (`uv.lock`) |

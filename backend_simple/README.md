# backend_simple — "Quick & Dirty" API

Celowy przykład aplikacji napisanej **bez dbałości o jakość oprogramowania**. Projekt realizuje podstawowe CRUD użytkowników i stanowi punkt odniesienia do porównania z podejściem production-ready.

---

## Cel

Pokazanie, jak wygląda kod pisany pod presją czasu (Time-to-Market), bez standardów inżynierskich. Każdy z wymienionych problemów jest **celowy** i ilustruje konkretny dług techniczny.

---

## Uruchomienie

```bash
# Środowisko wirtualne
python -m venv venv
source venv/Scripts/activate   # Windows (Git Bash)

# Zależności
pip install -r requirements.txt

# Migracje bazy
alembic upgrade head

# Serwer lokalnie
uvicorn main:app --reload
# http://127.0.0.1:8000/docs

# Docker (app + PostgreSQL 17 + nginx)
docker-compose up -d --build
# http://localhost/docs
```

---

## Endpointy

| Metoda | Ścieżka | Opis |
| :--- | :--- | :--- |
| `POST` | `/users/` | Utwórz użytkownika |
| `GET` | `/users/{user_id}` | Pobierz użytkownika |
| `GET` | `/users/collection/all` | Pobierz wszystkich użytkowników |
| `PUT` | `/users/{user_id}` | Zaktualizuj użytkownika |
| `DELETE` | `/users/{user_id}` | Usuń użytkownika |

---

## Zidentyfikowane antywzorce

### Bezpieczeństwo
- Hasła przechowywane w **plaintext** w bazie danych
- Brak autentykacji — każdy może czytać, edytować i usuwać dowolnego użytkownika
- `GET /users/collection/all` zwraca wszystkich użytkowników **wraz z hasłami**
- CORS skonfigurowany z `allow_origins=["*"]`
- `.env` z hasłami nie jest szyfrowany

### Obsługa błędów
- Brak `try/catch` — błędy zwracają domyślne HTTP 500
- `GET /{user_id}` zwraca `null` zamiast HTTP 404 gdy użytkownik nie istnieje
- `PUT` i `DELETE` crashują z 500 gdy użytkownik nie istnieje

### Baza danych
- Globalna sesja `session = SessionLocal()` na poziomie modułu — wyciek pamięci
- Brak konfiguracji connection pool
- Brak timeout'ów połączeń

### Walidacja
- Pydantic modele bez walidacji formatu (brak `EmailStr`, brak `min_length`)
- Brak response modeli — `create_user` zwraca hasło w odpowiedzi
- Brak paginacji w `collection/all` — zwraca całą tabelę

### Architektura
- Płaska struktura — wszystko w jednym katalogu (brak warstw domain/service/infrastructure)
- Brak separacji logiki biznesowej od HTTP
- Brak testów jednostkowych i integracyjnych

### DevOps
- `prod.dockerfile` uruchamia aplikację jako **root**
- Single-stage build — cache pip zostaje w obrazie
- Brak `.dockerignore`
- Brak health checków w Dockerfile
- CI/CD używa loginu i hasła SSH zamiast kluczy
- Pipeline nie weryfikuje poprawności aplikacji po deployu (`docker-compose up` bez health check)
- Brak etapu testów i lintingu w pipeline

---

## Struktura plików

```
backend_simple/
├── main.py                          # Punkt wejścia FastAPI
├── urls.py                          # Endpointy (router)
├── models.py                        # Model SQLAlchemy (User)
├── db.py                            # Konfiguracja bazy danych
├── requirements.txt                 # Zależności bez lock file
├── prod.dockerfile                  # Single-stage, root user
├── docker-compose.yml               # app + PostgreSQL 17 + nginx
├── nginx.conf                       # Konfiguracja nginx
├── nginx.default.conf               # Server block (proxy → app:8000)
├── alembic.ini                      # Konfiguracja migracji
├── migrations/
│   ├── env.py
│   └── versions/
│       └── 0001_init.py             # Tworzenie tabeli users
├── .env                             # Zmienne środowiskowe (hasła plaintext)
├── .gitignore
└── .github/
    └── workflows/
        └── ci_cd_run.yml            # CI/CD: build → push → deploy
```
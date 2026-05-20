#!/bin/bash

# Function to show error and exit immediately
show_error() {
    echo "================================"
    echo "BŁĄD: $1"
    echo "================================"
    exit 1
}

# Function to show info
show_info() {
    echo "INFO: $1"
}

# Function to show success
show_success() {
    echo "================================"
    echo "SUKCES: $1"
    echo "================================"
}

show_info "Rozpoczynam migrację bazy danych (TRYB AUTOMATYCZNY)..."

# Get project root directory (3 levels up from this script)
PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

show_info "Katalog projektu: $PROJECT_ROOT"

# Check argument
if [ -z "$1" ]; then
    echo "Użycie: $0 [local|stg|prod]"
    exit 1
fi

show_info "Środowisko: $1"

# Set paths relative to project root
ENV_FILE="$PROJECT_ROOT/env/$1.env"
show_info "Sprawdzam plik środowiskowy: $ENV_FILE"

if [ ! -f "$ENV_FILE" ]; then
    show_error "Plik środowiskowy $ENV_FILE nie istnieje!"
fi

show_info "Ładuję zmienne środowiskowe..."
set -a
source "$ENV_FILE"
set +a

# Check required environment variables
if [ -z "$DB_HOST" ]; then show_error "DB_HOST nie jest ustawione w pliku $1.env"; fi
if [ -z "$DB_PORT" ]; then show_error "DB_PORT nie jest ustawione w pliku $1.env"; fi
if [ -z "$DB_USER" ]; then show_error "DB_USER nie jest ustawione w pliku $1.env"; fi
if [ -z "$DB_PASSWORD" ]; then show_error "DB_PASSWORD nie jest ustawione w pliku $1.env"; fi
if [ -z "$DB_DBNAME" ]; then show_error "DB_DBNAME nie jest ustawione w pliku $1.env"; fi

show_info "Wszystkie zmienne środowiskowe są dostępne"

# Test database connection
export PGPASSWORD="$DB_PASSWORD"
show_info "Testuję połączenie z bazą danych..."
if ! psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_DBNAME" -p "$DB_PORT" -c "SELECT 1;" >/dev/null 2>&1; then
    CONNECTION_TEST=$(psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_DBNAME" -p "$DB_PORT" -c "SELECT 1;" 2>&1)
    echo "================================"
    echo "BŁĄD POŁĄCZENIA Z BAZĄ:"
    echo "$CONNECTION_TEST"
    echo "================================"
    show_error "Nie można połączyć się z bazą danych."
fi

show_info "✓ Połączenie z bazą danych działa"

echo "================================"
echo "GOTOWY DO MIGRACJI"
echo "Baza: $DB_DBNAME na $DB_HOST"
echo "================================"

# Check database_up.sql file
DATABASE_UP_FILE="$PROJECT_ROOT/database/psql/sql/database_up.sql"

if [ ! -f "$DATABASE_UP_FILE" ]; then
    show_error "Plik $DATABASE_UP_FILE nie istnieje!"
fi

show_info "Wykonuję database_up.sql (extensions, encoding)..."
if ! psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_DBNAME" -p "$DB_PORT" -f "$DATABASE_UP_FILE"; then
    show_error "Błąd podczas wykonywania database_up.sql!"
fi

show_info "✓ database_up.sql wykonany"

# Run Alembic migrations
show_info "Uruchamiam migracje Alembic (alembic upgrade head)..."
cd "$PROJECT_ROOT" || show_error "Nie można przejść do katalogu $PROJECT_ROOT"

if ! uv run alembic upgrade head; then
    show_error "Błąd podczas wykonywania migracji Alembic! Sprawdź logi powyżej."
fi

show_info "✓ Migracje Alembic zakończone"

# Seed initial user
echo "Startuję skrypt ładowania użytkownika z pliku .sql..."
"$PROJECT_ROOT/infra/scripts/database/copy_user.sh" "$1"

show_success "Migracja zakończona pomyślnie!"
exit 0
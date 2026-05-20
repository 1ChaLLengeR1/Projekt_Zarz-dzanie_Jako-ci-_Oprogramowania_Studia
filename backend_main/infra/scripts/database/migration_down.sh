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

show_info "Rozpoczynam rollback bazy danych (TRYB AUTOMATYCZNY)..."

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
source "$ENV_FILE"

# Check required environment variables
if [ -z "$DB_HOST" ]; then show_error "DB_HOST nie jest ustawione w pliku $1.env"; fi
if [ -z "$DB_PORT" ]; then show_error "DB_PORT nie jest ustawione w pliku $1.env"; fi
if [ -z "$DB_USER" ]; then show_error "DB_USER nie jest ustawione w pliku $1.env"; fi
if [ -z "$DB_PASSWORD" ]; then show_error "DB_PASSWORD nie jest ustawione w pliku $1.env"; fi
if [ -z "$DB_DBNAME" ]; then show_error "DB_DBNAME nie jest ustawione w pliku $1.env"; fi

show_info "Wszystkie zmienne środowiskowe są dostępne"

DATABASE_DOWN_FILE="$PROJECT_ROOT/database/psql/sql/database_down.sql"

if [ ! -f "$DATABASE_DOWN_FILE" ]; then
    show_error "Plik $DATABASE_DOWN_FILE nie istnieje!"
fi

# Set PostgreSQL password
export PGPASSWORD="$DB_PASSWORD"

# Test database connection
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
echo "⚠️  UWAGA: Wykonuję operację destrukcyjną (DROP TABLES)..."
echo "Baza: $DB_DBNAME na $DB_HOST"
echo "================================"

show_info "Rozpoczynam usuwanie tabel..."
if psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_DBNAME" -p "$DB_PORT" -f "$DATABASE_DOWN_FILE"; then
    show_success "Rollback zakończony pomyślnie!"
    exit 0
else
    show_error "Błąd podczas rollback! Sprawdź logi powyżej."
fi
#!/bin/bash

# Get project root directory (3 levels up from this script)
PROJECT_ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"

set -e
trap 'echo "❌ Wystąpił błąd w linii $LINENO"; sleep 10' ERR

if [ -z "$1" ]; then
    echo "Proszę podać parametr mode_env: local, stg lub prod"
    exit 1
fi

mode_env=${1:-local}

echo "Startuję skrypt ładowania env..."
source "$PROJECT_ROOT/env/$mode_env.env"

SQL_FILE="$PROJECT_ROOT/database/psql/sql/user.sql"

if [ ! -f "$SQL_FILE" ]; then
    echo "❌ Plik SQL nie istnieje: $SQL_FILE"
    echo "   Upewnij się, że plik user.sql istnieje w database/psql/sql/"
    sleep 5
    exit 1
fi

echo "📦 Importowanie użytkownika do PostgreSQL..."
export PGCLIENTENCODING=UTF8
PGPASSWORD="$DB_PASSWORD" psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_DBNAME" -p "$DB_PORT" --single-transaction -f "$SQL_FILE"

echo "✅ Import zakończony pomyślnie"
sleep 3
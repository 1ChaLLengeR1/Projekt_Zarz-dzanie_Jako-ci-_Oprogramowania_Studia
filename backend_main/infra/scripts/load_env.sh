#!/bin/bash

# Get project root directory (2 levels up from this script)
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

set -e
trap 'echo "❌ Wystąpił błąd w linii $LINENO"; sleep 10' ERR

if [ -z "$1" ]; then
    echo "Proszę podać parametr mode_env: local, stg lub prod"
    exit 1
fi

mode_env=${1:-local}

set -a
case "$mode_env" in
    local)
        echo "✅ Ładowanie lokal.env"
        source "$PROJECT_ROOT/env/local.env"
        ;;
    stg)
        echo "✅ Ładowanie stg.env"
        source "$PROJECT_ROOT/env/stg.env"
        ;;
    prod)
        echo "✅ Ładowanie prod.env"
        source "$PROJECT_ROOT/env/prod.env"
        ;;
    *)
        echo "❌ Nieznany tryb: $mode_env"
        exit 1
        ;;
esac
set +a

if [ -z "$DB_HOST" ] || [ -z "$DB_PORT" ] || [ -z "$DB_USER" ] || [ -z "$DB_PASSWORD" ] || [ -z "$DB_DBNAME" ]; then
    echo "Wszystkie zmienne środowiskowe muszą być ustawione w pliku $mode_env.env"
    sleep 10
    exit 1
fi

sleep 1

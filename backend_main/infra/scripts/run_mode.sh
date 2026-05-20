#!/bin/bash

set -e

if [ $# -ne 1 ]; then
  echo "Użycie: $0 <new_mode>"
  echo "Dostępne tryby: local, stg, prod"
  exit 1
fi

NEW_MODE=$1

# Get project root directory (2 levels up from this script)
PROJECT_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"

BASE_DIR="$PROJECT_ROOT"
CONFIG_FILE="$BASE_DIR/config/app_config.py"

if [ ! -f "$CONFIG_FILE" ]; then
  echo "Plik config/app_config.py nie istnieje!"
  exit 1
fi

CONTENT=$(cat "$CONFIG_FILE")

CURRENT_MODE=""

if [[ "$CONTENT" == *"ENV_MODE = 'local'"* ]] || [[ "$CONTENT" == *'ENV_MODE = "local"'* ]]; then
  CURRENT_MODE="local"
elif [[ "$CONTENT" == *"ENV_MODE = 'stg'"* ]] || [[ "$CONTENT" == *'ENV_MODE = "stg"'* ]]; then
  CURRENT_MODE="stg"
elif [[ "$CONTENT" == *"ENV_MODE = 'prod'"* ]] || [[ "$CONTENT" == *'ENV_MODE = "prod"'* ]]; then
  CURRENT_MODE="prod"
fi

if [ -n "$CURRENT_MODE" ]; then
  # Handle both single and double quotes
  CONTENT=$(echo "$CONTENT" | sed "s/ENV_MODE = '$CURRENT_MODE'/ENV_MODE = \"$NEW_MODE\"/")
  CONTENT=$(echo "$CONTENT" | sed "s/ENV_MODE = \"$CURRENT_MODE\"/ENV_MODE = \"$NEW_MODE\"/")

  echo "$CONTENT" > "$CONFIG_FILE"

  echo "Przełączono tryb z '$CURRENT_MODE' na '$NEW_MODE'"
else
  echo "Nie znaleziono obecnej wartości ENV_MODE w pliku."
  exit 1
fi

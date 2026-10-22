#!/usr/bin/env bash
# Actualiza los paquetes instalados y vuelca las versiones exactas en requirements.txt
set -euo pipefail
cd "$(dirname "$0")"

if [ -f .venv/Scripts/activate ]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

python -m pip install --upgrade pip
python -m pip install --upgrade -r requirements.txt
python -m pip freeze > requirements.txt

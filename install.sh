#!/usr/bin/env bash
# Crea el entorno virtual (si no existe) e instala las dependencias de requirements.txt
set -euo pipefail
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
    python -m venv .venv
fi

# Windows (Git Bash) usa Scripts/, Linux/macOS usa bin/
if [ -f .venv/Scripts/activate ]; then
    source .venv/Scripts/activate
else
    source .venv/bin/activate
fi

python -m pip install --upgrade pip
python -m pip install -r requirements.txt

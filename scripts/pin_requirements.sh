#!/usr/bin/env bash
# Script para generar un archivo `requirements.lock` con las versiones actualmente instaladas
# Uso: ejecutarlo desde el entorno virtual del proyecto: `./scripts/pin_requirements.sh`

set -euo pipefail

OUT_FILE="requirements.lock"

python -m pip freeze > "${OUT_FILE}"
echo "Generado ${OUT_FILE} con las dependencias actualmente instaladas."

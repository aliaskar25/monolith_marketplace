#!/usr/bin/env bash
set -euo pipefail

# APP_ENV can be dev or prod
APP_ENV=${APP_ENV:-dev}

if [[ "$APP_ENV" == "dev" ]]; then
  echo "[entrypoint] Running in DEV mode"
  exec uvicorn marketplace.main:app --host 0.0.0.0 --port 8000 --reload
else
  echo "[entrypoint] Running in PROD mode"
  # Increase workers based on CPU count (fallback 2)
  WORKERS=${UVICORN_WORKERS:-$(python - <<'PY'
import os, multiprocessing
print(max(2, multiprocessing.cpu_count()))
PY
)}
  exec uvicorn marketplace.main:app --host 0.0.0.0 --port 8000 --workers "$WORKERS"
fi



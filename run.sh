#!/usr/bin/env bash
# PyDrill — one-command launcher.
#   ./run.sh          start the API + built UI on http://localhost:8000
#   ./run.sh dev      start FastAPI (:8000) + Vite dev server (:5173) with HMR
set -euo pipefail
cd "$(dirname "$0")"

if [ "${1:-}" = "dev" ]; then
  echo "→ API      http://localhost:8000  (docs: /docs)"
  echo "→ Frontend http://localhost:5173  (hot reload, /api proxied)"
  ( cd backend && python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload ) &
  API_PID=$!
  trap 'kill $API_PID 2>/dev/null || true' EXIT
  ( cd frontend && npm run dev )
else
  if [ ! -d backend/static_app ]; then
    echo "→ Building the React app…"
    ( cd frontend && npm install && npm run build )
  fi
  echo "→ PyDrill running on http://localhost:8000"
  cd backend && exec python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
fi

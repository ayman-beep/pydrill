#!/usr/bin/env bash
# PyDrill — one-command launcher.
#
#   ./run.sh          build the static app and serve it  → http://localhost:4173
#   ./run.sh dev      Vite dev server with HMR           → http://localhost:5173
#   ./run.sh api      optional FastAPI backend           → http://localhost:8000
#   ./run.sh deploy   build a Netlify-ready zip           → pydrill-netlify.zip
#
# The app is fully static: the curriculum ships as JSON in the bundle and
# grading runs in the browser, so no backend is required.
set -euo pipefail
cd "$(dirname "$0")"

ensure_deps() {
  if [ ! -d frontend/node_modules ]; then
    echo "→ Installing frontend dependencies…"
    ( cd frontend && npm install )
  fi
}

case "${1:-static}" in
  static|"")
    ensure_deps
    echo "→ Building static bundle…"
    ( cd frontend && npm run build )
    echo "→ Serving dist/ on http://localhost:4173  (Ctrl+C to stop)"
    cd frontend && exec npx vite preview --port 4173 --host 0.0.0.0
    ;;
  dev)
    ensure_deps
    echo "→ Vite dev server: http://localhost:5173"
    cd frontend && exec npm run dev
    ;;
  api)
    echo "→ FastAPI: http://localhost:8000  (docs at /docs)"
    echo "  Note: optional — the static app never calls it."
    cd backend && exec python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
    ;;
  deploy)
    ensure_deps
    ( cd frontend && npm run build )
    rm -f pydrill-netlify.zip
    ( cd frontend/dist && zip -qr ../../pydrill-netlify.zip . )
    echo "→ Built pydrill-netlify.zip — drag it onto https://app.netlify.com/drop"
    echo "  Or connect the GitHub repo: netlify.toml already sets base=frontend, publish=dist."
    ;;
  test)
    python3 tests/grading_parity.py
    ;;
  *)
    echo "usage: ./run.sh [static|dev|api|deploy|test]" >&2
    exit 2
    ;;
esac

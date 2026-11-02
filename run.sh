#!/usr/bin/env bash
# FlashFleet Runner Script

set -e

PORT=${PORT:-8000}
HOST=${HOST:-"0.0.0.0"}

echo "=========================================="
echo " Starting FlashFleet FastAPI Server..."
echo " Running on http://127.0.0.1:${PORT}"
echo " Interactive Docs at http://127.0.0.1:${PORT}/docs"
echo "=========================================="

exec python3 -m uvicorn flashfleet.api:app --host "${HOST}" --port "${PORT}" --reload


"""Vercel Serverless Function entrypoint for FlashFleet."""

from __future__ import annotations

import sys
from pathlib import Path

# Add project root to sys.path so 'flashfleet' package is discoverable
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from flashfleet.config import DB_PATH

# Auto-seed database if running on a fresh Vercel instance where flashfleet.db is absent
if not DB_PATH.exists():
    try:
        from flashfleet.seed_mock_db import seed_database
        seed_database()
    except Exception as exc:
        print(f"Warning: Could not auto-seed database on startup: {exc}")

from flashfleet.api import app as raw_app  # noqa: E402


class VercelPathMiddleware:
    """Normalize request path in Vercel serverless environments.

    Vercel rewrites routes to '/api/index' or '/api/index.py'. This middleware
    strips the Vercel function prefix so FastAPI route handlers match properly.
    """

    def __init__(self, asgi_app):
        self.app = asgi_app

    async def __call__(self, scope, receive, send):
        if scope.get("type") in ("http", "websocket"):
            path = scope.get("path", "")
            for prefix in ("/api/index.py", "/api/index"):
                if path.startswith(prefix):
                    scope["path"] = path[len(prefix):] or "/"
                    break
        await self.app(scope, receive, send)


# Expose ASGI application
app = VercelPathMiddleware(raw_app)
handler = app



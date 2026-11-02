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

from flashfleet.api import app  # noqa: E402


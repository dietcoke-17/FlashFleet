"""Database connection utilities for FlashFleet."""

import sqlite3
from contextlib import contextmanager
from typing import Generator

from flashfleet.config import DB_PATH


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection with Row factory enabled.

    Returns:
        A sqlite3.Connection configured to return rows as sqlite3.Row objects.
    """
    try:
        conn = sqlite3.connect(str(DB_PATH))
    except sqlite3.OperationalError:
        # Fallback for read-only environments (e.g. Vercel serverless)
        conn = sqlite3.connect(f"file:{DB_PATH}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    return conn


def get_engine() -> str:
    """Return the SQLite connection string for the database path.

    Returns:
        A connection string in the format 'sqlite:///path/to/db'.
    """
    return f"sqlite:///{DB_PATH}"


@contextmanager
def db_cursor() -> Generator[sqlite3.Cursor, None, None]:
    """Context manager that yields a database cursor and auto-commits.

    On successful exit the transaction is committed; on exception it is
    rolled back and the exception is re-raised.

    Yields:
        A sqlite3.Cursor bound to the FlashFleet database.
    """
    conn = get_connection()
    cursor = conn.cursor()
    try:
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()

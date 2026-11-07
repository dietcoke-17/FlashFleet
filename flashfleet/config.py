"""FlashFleet configuration constants."""

import os
import shutil
from pathlib import Path

# Project root directory
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# Directory for downloaded CSV data files
DATA_DIR: Path = BASE_DIR / "data"

# SQLite database file path:
# On Vercel or AWS Lambda, the root deployment directory is read-only.
# SQLite requires write permissions for journal/lock files, so we use /tmp on serverless.
if os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME"):
    TMP_DIR = Path("/tmp")
    DB_PATH: Path = TMP_DIR / "flashfleet.db"

    # Copy bundled database to /tmp on cold start if not already copied
    bundled_db = BASE_DIR / "flashfleet.db"
    if bundled_db.exists() and not DB_PATH.exists():
        try:
            shutil.copy2(bundled_db, DB_PATH)
        except Exception as exc:
            print(f"Warning: could not copy bundled database to /tmp: {exc}")
else:
    DB_PATH: Path = BASE_DIR / "flashfleet.db"

# Mapping of logical table names to their corresponding Olist CSV filenames
OLIST_TABLES: dict[str, str] = {
    "orders": "olist_orders_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "products": "olist_products_dataset.csv",
    "geolocation": "olist_geolocation_dataset.csv",
    "customers": "olist_customers_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
}

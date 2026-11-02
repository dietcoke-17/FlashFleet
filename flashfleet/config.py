"""FlashFleet configuration constants."""

from pathlib import Path

# Project root directory
BASE_DIR: Path = Path(__file__).resolve().parent.parent

# Directory for downloaded CSV data files
DATA_DIR: Path = BASE_DIR / "data"

# SQLite database file path
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

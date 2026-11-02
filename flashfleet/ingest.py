"""FlashFleet data ingestion pipeline.

Downloads the Olist Brazilian E-Commerce dataset, cleans the data with Pandas,
loads it into a local SQLite database, and creates performance indexes.
"""

import logging
import shutil
import sqlite3
import sys
from pathlib import Path
from typing import Any

try:
    import pandas as pd
except ImportError:
    pd = None  # Lazy handled in load_tables

from flashfleet.config import DATA_DIR, DB_PATH, OLIST_TABLES

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# SQL Schema
# ---------------------------------------------------------------------------

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS orders (
    order_id TEXT PRIMARY KEY,
    customer_id TEXT NOT NULL,
    order_status TEXT,
    order_purchase_timestamp TEXT,
    order_approved_at TEXT,
    order_delivered_carrier_date TEXT,
    order_delivered_customer_date TEXT,
    order_estimated_delivery_date TEXT
);

CREATE TABLE IF NOT EXISTS order_items (
    order_id TEXT NOT NULL,
    order_item_id INTEGER NOT NULL,
    product_id TEXT NOT NULL,
    seller_id TEXT NOT NULL,
    shipping_limit_date TEXT,
    price REAL,
    freight_value REAL,
    PRIMARY KEY (order_id, order_item_id)
);

CREATE TABLE IF NOT EXISTS products (
    product_id TEXT PRIMARY KEY,
    product_category_name TEXT,
    product_name_lenght INTEGER,
    product_description_lenght INTEGER,
    product_photos_qty INTEGER,
    product_weight_g REAL,
    product_length_cm REAL,
    product_height_cm REAL,
    product_width_cm REAL
);

CREATE TABLE IF NOT EXISTS geolocation (
    geolocation_zip_code_prefix TEXT,
    geolocation_lat REAL,
    geolocation_lng REAL,
    geolocation_city TEXT,
    geolocation_state TEXT
);

CREATE TABLE IF NOT EXISTS customers (
    customer_id TEXT PRIMARY KEY,
    customer_unique_id TEXT,
    customer_zip_code_prefix TEXT,
    customer_city TEXT,
    customer_state TEXT
);

CREATE TABLE IF NOT EXISTS sellers (
    seller_id TEXT PRIMARY KEY,
    seller_zip_code_prefix TEXT,
    seller_city TEXT,
    seller_state TEXT
);

CREATE VIEW IF NOT EXISTS v_order_fulfillment AS
SELECT
    o.order_id,
    o.customer_id,
    c.customer_state AS region,
    o.order_status,
    o.order_purchase_timestamp,
    o.order_delivered_customer_date,
    o.order_estimated_delivery_date,
    julianday(o.order_delivered_customer_date) - julianday(o.order_estimated_delivery_date) AS sla_breach_days,
    julianday(o.order_delivered_customer_date) - julianday(o.order_purchase_timestamp) AS transit_days,
    oi.product_id,
    p.product_weight_g,
    p.product_length_cm,
    p.product_height_cm,
    p.product_width_cm,
    (p.product_length_cm * p.product_height_cm * p.product_width_cm) AS product_volume_cm3,
    CASE WHEN p.product_weight_g >= 5000 THEN 'heavy_freight' ELSE 'lightweight' END AS weight_class
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN products p ON oi.product_id = p.product_id;
"""

INDEX_SQL = [
    "CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);",
    "CREATE INDEX IF NOT EXISTS idx_orders_status ON orders(order_status);",
    "CREATE INDEX IF NOT EXISTS idx_orders_purchase_ts ON orders(order_purchase_timestamp);",
    "CREATE INDEX IF NOT EXISTS idx_order_items_product ON order_items(product_id);",
    "CREATE INDEX IF NOT EXISTS idx_order_items_order ON order_items(order_id);",
    "CREATE INDEX IF NOT EXISTS idx_geolocation_zip ON geolocation(geolocation_zip_code_prefix);",
    "CREATE INDEX IF NOT EXISTS idx_customers_state ON customers(customer_state);",
    "CREATE INDEX IF NOT EXISTS idx_sellers_state ON sellers(seller_state);",
]

# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------


def download_dataset() -> Path:
    """Download the Olist dataset via kagglehub and copy CSVs to DATA_DIR.

    Falls back to using CSVs already present in DATA_DIR if the download
    fails (e.g. missing Kaggle credentials).

    Returns:
        The path to the directory containing the CSV files.

    Raises:
        FileNotFoundError: If neither kagglehub download nor local CSVs are
            available.
    """
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    try:
        import kagglehub  # noqa: WPS433 (local import intentional)

        logger.info("Downloading Olist dataset via kagglehub …")
        cached_path = Path(kagglehub.dataset_download("olistbr/brazilian-ecommerce"))
        logger.info("Dataset cached at: %s", cached_path)

        # Copy CSV files from the kagglehub cache into our DATA_DIR
        for csv_filename in OLIST_TABLES.values():
            src = cached_path / csv_filename
            dst = DATA_DIR / csv_filename
            if src.exists():
                shutil.copy2(src, dst)
                logger.info("Copied %s → %s", src.name, dst)
            else:
                logger.warning("Expected file not found in cache: %s", src)

        return DATA_DIR

    except Exception as exc:
        logger.warning(
            "kagglehub download failed (%s). Falling back to local CSVs in %s",
            exc,
            DATA_DIR,
        )
        logger.info(
            "To fix this, either:\n"
            "  • Set KAGGLE_USERNAME and KAGGLE_KEY environment variables, OR\n"
            "  • Manually download from "
            "https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce\n"
            "    and extract the CSVs into the data/ directory."
        )

        # Verify at least one expected CSV is present locally
        found = [
            DATA_DIR / fn for fn in OLIST_TABLES.values() if (DATA_DIR / fn).exists()
        ]
        if not found:
            raise FileNotFoundError(
                f"No CSV files found in {DATA_DIR}. "
                "Please download the dataset manually."
            ) from exc

        logger.info("Found %d local CSV file(s) — proceeding with ingestion.", len(found))
        return DATA_DIR


# ---------------------------------------------------------------------------
# Schema creation
# ---------------------------------------------------------------------------


def create_schema(conn: sqlite3.Connection) -> None:
    """Create all database tables defined in SCHEMA_SQL.

    Args:
        conn: An open SQLite connection.
    """
    logger.info("Creating database schema …")
    conn.executescript(SCHEMA_SQL)
    conn.commit()
    logger.info("Schema created successfully.")


# ---------------------------------------------------------------------------
# Data cleaning & loading
# ---------------------------------------------------------------------------

ORDERS_TIMESTAMP_COLS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
]


def _clean_orders(df: Any) -> Any:
    """Clean the orders DataFrame.

    • Parse all timestamp columns as datetime.
    • Drop rows where ``order_delivered_customer_date`` is null AND
      ``order_status`` is ``'delivered'`` (inconsistent data).

    Args:
        df: Raw orders DataFrame.

    Returns:
        Cleaned orders DataFrame.
    """
    for col in ORDERS_TIMESTAMP_COLS:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    before = len(df)
    inconsistent_mask = (
        df["order_delivered_customer_date"].isna() & (df["order_status"] == "delivered")
    )
    df = df[~inconsistent_mask].copy()
    dropped = before - len(df)
    if dropped:
        logger.info(
            "Orders: dropped %d inconsistent rows (delivered but no delivery date).",
            dropped,
        )

    # Convert datetime columns to ISO-format strings for SQLite storage
    for col in ORDERS_TIMESTAMP_COLS:
        if col in df.columns:
            df[col] = df[col].dt.strftime("%Y-%m-%d %H:%M:%S")

    return df


def _clean_products(df: Any) -> Any:
    """Clean the products DataFrame.

    • Fill null ``product_weight_g`` with the column median.
    • Fill null dimensions (length, height, width) with their medians.

    Args:
        df: Raw products DataFrame.

    Returns:
        Cleaned products DataFrame.
    """
    fill_cols = [
        "product_weight_g",
        "product_length_cm",
        "product_height_cm",
        "product_width_cm",
    ]
    for col in fill_cols:
        if col in df.columns:
            median_val = df[col].median()
            null_count = df[col].isna().sum()
            df[col] = df[col].fillna(median_val)
            if null_count:
                logger.info(
                    "Products: filled %d nulls in %s with median %.2f.",
                    null_count,
                    col,
                    median_val,
                )
    return df


def _clean_geolocation(df: Any) -> Any:
    """Clean the geolocation DataFrame.

    • Deduplicate by ``geolocation_zip_code_prefix``, keeping the first
      occurrence per prefix to avoid bloating the database.

    Args:
        df: Raw geolocation DataFrame.

    Returns:
        Deduplicated geolocation DataFrame.
    """
    before = len(df)
    df = df.drop_duplicates(subset=["geolocation_zip_code_prefix"], keep="first").copy()
    logger.info(
        "Geolocation: deduplicated from %d to %d rows (by zip_code_prefix).",
        before,
        len(df),
    )
    return df


CLEANERS: dict[str, callable] = {
    "orders": _clean_orders,
    "products": _clean_products,
    "geolocation": _clean_geolocation,
}


def load_tables(conn: sqlite3.Connection, data_dir: Path) -> None:
    """Read, clean, and load all CSV tables into the database.

    Args:
        conn: An open SQLite connection.
        data_dir: Directory containing the Olist CSV files.
    """
    if pd is None:
        raise ImportError(
            "pandas is required to ingest CSV datasets. Please install dependencies: "
            "pip install -r requirements.txt"
        )
    for table_name, csv_filename in OLIST_TABLES.items():
        csv_path = data_dir / csv_filename
        if not csv_path.exists():
            logger.warning("CSV not found, skipping table '%s': %s", table_name, csv_path)
            continue

        logger.info("Reading %s …", csv_path.name)
        df = pd.read_csv(csv_path)
        logger.info("  → %d rows, %d columns", len(df), len(df.columns))

        # Apply table-specific cleaning if available
        cleaner = CLEANERS.get(table_name)
        if cleaner:
            df = cleaner(df)

        # Load into SQLite
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        logger.info("  → Loaded '%s' table (%d rows).", table_name, len(df))


# ---------------------------------------------------------------------------
# Index creation
# ---------------------------------------------------------------------------


def create_indexes(conn: sqlite3.Connection) -> None:
    """Create performance indexes on all tables.

    Args:
        conn: An open SQLite connection.
    """
    logger.info("Creating indexes …")
    for stmt in INDEX_SQL:
        conn.execute(stmt)
    conn.commit()
    logger.info("All indexes created successfully.")


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------


def main() -> None:
    """Run the full ingestion pipeline.

    1. Download / locate CSV files (or generate synthetic data if --seed/--mock passed).
    2. Create the SQLite schema.
    3. Clean and load data into the database.
    4. Create performance indexes.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s  %(levelname)-8s  %(message)s",
        datefmt="%H:%M:%S",
    )

    if "--seed" in sys.argv or "--mock" in sys.argv:
        from flashfleet.seed_mock_db import seed_database
        logger.info("Running synthetic mock database seeder...")
        seed_database()
        return

    logger.info("=" * 60)
    logger.info("FlashFleet — Data Ingestion Pipeline")
    logger.info("=" * 60)

    # Step 1: Download / locate dataset
    data_dir = download_dataset()

    # Step 2–4: Schema, load, index
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    try:
        create_schema(conn)
        load_tables(conn, data_dir)
        create_indexes(conn)
    finally:
        conn.close()

    logger.info("=" * 60)
    logger.info("Ingestion complete. Database: %s", DB_PATH)
    logger.info("=" * 60)


if __name__ == "__main__":
    main()

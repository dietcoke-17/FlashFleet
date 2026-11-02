"""Generate realistic synthetic Olist e-commerce data for local testing and demo.

This allows running FlashFleet immediately without requiring Kaggle credentials
or large external downloads.
"""

from __future__ import annotations

import random
import sqlite3
from datetime import datetime, timedelta

from flashfleet.config import DB_PATH
from flashfleet.ingest import SCHEMA_SQL, INDEX_SQL

REGIONS = ["SP", "RJ", "MG", "RS", "PR", "SC", "BA", "PE", "CE", "DF"]
CATEGORIES = [
    "beleza_saude",
    "informatica_acessorios",
    "cama_mesa_banho",
    "esporte_lazer",
    "moveis_decoracao",
    "utilidades_domesticas",
    "automotivo",
    "brinquedos",
]


def seed_database(num_orders: int = 1200) -> None:
    """Populate SQLite database with synthetic orders, items, products, customers."""
    random.seed(42)

    conn = sqlite3.connect(str(DB_PATH))
    conn.executescript(SCHEMA_SQL)
    for idx_sql in INDEX_SQL:
        conn.execute(idx_sql)

    # 1. Generate Products (some lightweight, some heavy freight)
    products = []
    for i in range(1, 151):
        product_id = f"prod_{i:04d}"
        cat = random.choice(CATEGORIES)
        # 20% heavy freight (>= 5000g), 80% lightweight
        if random.random() < 0.20:
            weight_g = round(random.uniform(5000.0, 30000.0), 1)
            length_cm = round(random.uniform(40.0, 100.0), 1)
            height_cm = round(random.uniform(30.0, 80.0), 1)
            width_cm = round(random.uniform(30.0, 70.0), 1)
        else:
            weight_g = round(random.uniform(100.0, 4500.0), 1)
            length_cm = round(random.uniform(10.0, 35.0), 1)
            height_cm = round(random.uniform(5.0, 25.0), 1)
            width_cm = round(random.uniform(10.0, 30.0), 1)

        products.append((
            product_id,
            cat,
            random.randint(20, 60),
            random.randint(100, 1000),
            random.randint(1, 6),
            weight_g,
            length_cm,
            height_cm,
            width_cm,
        ))

    conn.executemany(
        """INSERT OR REPLACE INTO products VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        products,
    )

    # 2. Generate Customers across Brazilian states (heavy concentration in SP, RJ, MG)
    state_weights = [0.42, 0.15, 0.12, 0.06, 0.05, 0.04, 0.05, 0.04, 0.04, 0.03]
    customers = []
    customer_ids = []
    for i in range(1, 601):
        cust_id = f"cust_{i:04d}"
        customer_ids.append(cust_id)
        state = random.choices(REGIONS, weights=state_weights, k=1)[0]
        zip_prefix = f"{random.randint(1000, 99999):05d}"
        customers.append((
            cust_id,
            f"unique_{cust_id}",
            zip_prefix,
            f"City_{state}",
            state,
        ))

    conn.executemany(
        """INSERT OR REPLACE INTO customers VALUES (?, ?, ?, ?, ?)""",
        customers,
    )

    # 3. Generate Sellers
    sellers = []
    seller_ids = []
    for i in range(1, 51):
        seller_id = f"sell_{i:04d}"
        seller_ids.append(seller_id)
        state = random.choices(REGIONS, weights=state_weights, k=1)[0]
        zip_prefix = f"{random.randint(1000, 99999):05d}"
        sellers.append((seller_id, zip_prefix, f"City_{state}", state))

    conn.executemany(
        """INSERT OR REPLACE INTO sellers VALUES (?, ?, ?, ?)""",
        sellers,
    )

    # 4. Generate Geolocation prefixes
    geolocations = []
    for reg in REGIONS:
        for p in range(10):
            prefix = f"{random.randint(1000, 99999):05d}"
            lat = round(random.uniform(-30.0, -2.0), 4)
            lng = round(random.uniform(-60.0, -35.0), 4)
            geolocations.append((prefix, lat, lng, f"City_{reg}", reg))

    conn.executemany(
        """INSERT OR IGNORE INTO geolocation VALUES (?, ?, ?, ?, ?)""",
        geolocations,
    )

    # 5. Generate Orders & Order Items spanning ~180 days
    base_date = datetime(2023, 1, 1, 10, 0, 0)
    orders = []
    order_items = []

    for i in range(1, num_orders + 1):
        order_id = f"ord_{i:05d}"
        cust_id = random.choice(customer_ids)

        # random purchase date over 180 days
        days_offset = random.uniform(0, 180)
        purchase_time = base_date + timedelta(days=days_offset)
        approved_time = purchase_time + timedelta(hours=random.uniform(1, 24))
        carrier_time = approved_time + timedelta(days=random.uniform(1, 4))

        # Transit days: heavy freight takes longer, certain regions take longer
        # Estimated delivery date is typically 14-25 days from purchase
        estimated_days = random.randint(12, 28)
        estimated_time = purchase_time + timedelta(days=estimated_days)

        # 95% are delivered, 5% cancelled/shipped
        if random.random() < 0.95:
            status = "delivered"
            # Some delivered on time, ~10-15% breach SLA
            if random.random() < 0.12:
                # Breached SLA: delivery after estimated date
                breach_delay = random.uniform(1, 14)
                delivered_time = estimated_time + timedelta(days=breach_delay)
            else:
                # Delivered on time
                actual_transit = random.uniform(3, max(4, estimated_days - 2))
                delivered_time = purchase_time + timedelta(days=actual_transit)

            delivered_time_str = delivered_time.strftime("%Y-%m-%d %H:%M:%S")
        else:
            status = random.choice(["shipped", "invoiced", "canceled"])
            delivered_time_str = None

        orders.append((
            order_id,
            cust_id,
            status,
            purchase_time.strftime("%Y-%m-%d %H:%M:%S"),
            approved_time.strftime("%Y-%m-%d %H:%M:%S"),
            carrier_time.strftime("%Y-%m-%d %H:%M:%S"),
            delivered_time_str,
            estimated_time.strftime("%Y-%m-%d %H:%M:%S"),
        ))

        # Order Items (1 to 3 items per order)
        num_items = random.choices([1, 2, 3], weights=[0.8, 0.15, 0.05], k=1)[0]
        for item_idx in range(1, num_items + 1):
            prod = random.choice(products)
            prod_id = prod[0]
            seller_id = random.choice(seller_ids)
            price = round(random.uniform(25.0, 850.0), 2)
            freight = round(random.uniform(10.0, 80.0), 2)
            ship_limit = (purchase_time + timedelta(days=7)).strftime("%Y-%m-%d %H:%M:%S")

            order_items.append((
                order_id,
                item_idx,
                prod_id,
                seller_id,
                ship_limit,
                price,
                freight,
            ))

    conn.executemany(
        """INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
        orders,
    )
    conn.executemany(
        """INSERT OR REPLACE INTO order_items VALUES (?, ?, ?, ?, ?, ?, ?)""",
        order_items,
    )

    # Create fulfillment helper view
    conn.execute("""
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
    """)

    conn.commit()
    conn.close()
    print(f"✓ Seeded {len(orders)} orders, {len(order_items)} items, {len(products)} products into {DB_PATH}")


if __name__ == "__main__":
    seed_database()


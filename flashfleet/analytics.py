"""Phase 2 – SQL Analytics Module for FlashFleet.

Provides :class:`BaselineAnalytics`, a high-level interface that runs
advanced analytical queries against the FlashFleet SQLite database and
returns plain Python data structures (lists of dicts / dicts) ready for
consumption by the simulation engine or API layer.

Usage::

    from flashfleet.analytics import get_analytics

    analytics = get_analytics()
    breaches  = analytics.get_delivery_sla_breach_by_region()
    summary   = analytics.get_baseline_summary(region="SP")
"""

from __future__ import annotations

import sqlite3
from typing import Any

from flashfleet.db import get_connection


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _rows_to_dicts(rows: list[sqlite3.Row]) -> list[dict[str, Any]]:
    """Convert a list of ``sqlite3.Row`` objects to plain dicts."""
    return [dict(row) for row in rows]


# ---------------------------------------------------------------------------
# BaselineAnalytics
# ---------------------------------------------------------------------------

class BaselineAnalytics:
    """Run advanced analytical queries against the FlashFleet database.

    Each public method executes one or more SQL statements and returns
    results as Python-native data structures (``list[dict]`` or ``dict``).

    Parameters
    ----------
    conn:
        An optional pre-existing ``sqlite3.Connection``.  When *None*,
        a new connection is obtained via :func:`flashfleet.db.get_connection`.
    """

    def __init__(self, conn: sqlite3.Connection | None = None) -> None:
        self._conn = conn or get_connection()

    # ------------------------------------------------------------------
    # 1. Delivery SLA breach by region
    # ------------------------------------------------------------------

    def get_delivery_sla_breach_by_region(self) -> list[dict[str, Any]]:
        """Calculate delivery SLA breaches segmented by customer state.

        A delivery is considered *breached* when the actual delivery date
        exceeds the estimated delivery date (``breach_days > 0``).

        Returns
        -------
        list[dict]
            Each dict contains:
            - ``region`` – customer state code
            - ``total_deliveries`` – number of delivered orders in the region
            - ``breached_orders`` – count of orders that missed the SLA
            - ``avg_breach_days`` – average overshoot in days (breached only)
            - ``breach_rate_pct`` – percentage of breached orders
        """
        sql = """
        WITH delivery_metrics AS (
            SELECT
                c.customer_state AS region,
                o.order_id,
                julianday(o.order_delivered_customer_date)
                    - julianday(o.order_estimated_delivery_date) AS breach_days
            FROM orders o
            JOIN customers c ON o.customer_id = c.customer_id
            WHERE o.order_status = 'delivered'
              AND o.order_delivered_customer_date IS NOT NULL
              AND o.order_estimated_delivery_date IS NOT NULL
        )
        SELECT
            region,
            COUNT(*) AS total_deliveries,
            SUM(CASE WHEN breach_days > 0 THEN 1 ELSE 0 END) AS breached_orders,
            ROUND(AVG(CASE WHEN breach_days > 0 THEN breach_days ELSE NULL END), 2) AS avg_breach_days,
            ROUND(
                100.0 * SUM(CASE WHEN breach_days > 0 THEN 1 ELSE 0 END) / COUNT(*),
                2
            ) AS breach_rate_pct
        FROM delivery_metrics
        GROUP BY region
        ORDER BY breach_rate_pct DESC;
        """
        cur = self._conn.execute(sql)
        return _rows_to_dicts(cur.fetchall())

    # ------------------------------------------------------------------
    # 2. Weekly order volume with rolling average
    # ------------------------------------------------------------------

    def get_weekly_order_volume(self) -> list[dict[str, Any]]:
        """Calculate weekly order volume with a 4-week rolling average.

        Uses ``strftime('%Y-%W', ...)`` to bucket orders and a window
        function for the rolling average.

        Returns
        -------
        list[dict]
            Each dict contains:
            - ``year_week`` – ISO year-week string (``YYYY-WW``)
            - ``order_count`` – orders placed that week
            - ``rolling_4wk_avg`` – 4-week rolling average (current + 3 prior)
            - ``overall_avg`` – grand average across all weeks
        """
        sql = """
        WITH weekly_orders AS (
            SELECT
                strftime('%Y-%W', order_purchase_timestamp) AS year_week,
                COUNT(*) AS order_count
            FROM orders
            WHERE order_purchase_timestamp IS NOT NULL
            GROUP BY year_week
        )
        SELECT
            year_week,
            order_count,
            ROUND(AVG(order_count) OVER (
                ORDER BY year_week
                ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
            ), 2) AS rolling_4wk_avg,
            ROUND(AVG(order_count) OVER (), 2) AS overall_avg
        FROM weekly_orders
        ORDER BY year_week;
        """
        cur = self._conn.execute(sql)
        return _rows_to_dicts(cur.fetchall())

    # ------------------------------------------------------------------
    # 3. Transit-time percentiles by weight class
    # ------------------------------------------------------------------

    def get_transit_time_percentiles(self) -> list[dict[str, Any]]:
        """Compute transit-time distribution for heavy freight vs lightweight.

        *Heavy freight* is defined as ``product_weight_g >= 5000``.
        Uses ``PERCENT_RANK()`` to derive approximate median and P90 values.

        Returns
        -------
        list[dict]
            Each dict contains:
            - ``weight_class`` – ``'heavy_freight'`` or ``'lightweight'``
            - ``sample_size``
            - ``min_transit_days``
            - ``avg_transit_days``
            - ``median_transit_days`` – approximate median (P50)
            - ``p90_transit_days`` – approximate 90th percentile
            - ``max_transit_days``
        """
        sql = """
        WITH order_transit AS (
            SELECT
                oi.order_id,
                p.product_weight_g,
                CASE
                    WHEN p.product_weight_g >= 5000 THEN 'heavy_freight'
                    ELSE 'lightweight'
                END AS weight_class,
                julianday(o.order_delivered_customer_date)
                    - julianday(o.order_purchase_timestamp) AS transit_days
            FROM order_items oi
            JOIN products p ON oi.product_id = p.product_id
            JOIN orders o ON oi.order_id = o.order_id
            WHERE o.order_status = 'delivered'
              AND o.order_delivered_customer_date IS NOT NULL
              AND o.order_purchase_timestamp IS NOT NULL
              AND p.product_weight_g IS NOT NULL
        ),
        ranked AS (
            SELECT
                weight_class,
                transit_days,
                PERCENT_RANK() OVER (
                    PARTITION BY weight_class ORDER BY transit_days
                ) AS pct_rank
            FROM order_transit
        )
        SELECT
            weight_class,
            COUNT(*) AS sample_size,
            ROUND(MIN(transit_days), 2) AS min_transit_days,
            ROUND(AVG(transit_days), 2) AS avg_transit_days,
            ROUND(MAX(CASE WHEN pct_rank <= 0.5 THEN transit_days END), 2) AS median_transit_days,
            ROUND(MAX(CASE WHEN pct_rank <= 0.9 THEN transit_days END), 2) AS p90_transit_days,
            ROUND(MAX(transit_days), 2) AS max_transit_days
        FROM ranked
        GROUP BY weight_class;
        """
        cur = self._conn.execute(sql)
        return _rows_to_dicts(cur.fetchall())

    # ------------------------------------------------------------------
    # 4. Consolidated baseline summary
    # ------------------------------------------------------------------

    def get_baseline_summary(self, region: str | None = None) -> dict[str, Any]:
        """Return a consolidated baseline summary for the simulation engine.

        Parameters
        ----------
        region:
            Optional customer state code.  When provided, all metrics are
            scoped to orders from that region.

        Returns
        -------
        dict
            Keys: ``avg_daily_orders``, ``avg_weekly_orders``,
            ``avg_package_volume_cm3``, ``avg_package_weight_g``,
            ``avg_transit_days``, ``p90_transit_days``, ``total_orders``,
            ``date_range_days``, ``region``.
        """
        # ----- Build optional region filter fragments ------------------
        if region is not None:
            region_join = "JOIN customers c ON o.customer_id = c.customer_id"
            region_where = "AND c.customer_state = ?"
            params: tuple[Any, ...] = (region,)
        else:
            region_join = ""
            region_where = ""
            params = ()

        # ----- Total orders & date range -------------------------------
        sql_counts = f"""
        SELECT
            COUNT(*)                                                        AS total_orders,
            CAST(
                julianday(MAX(o.order_purchase_timestamp))
                - julianday(MIN(o.order_purchase_timestamp))
            AS INTEGER)                                                     AS date_range_days
        FROM orders o
        {region_join}
        WHERE o.order_status = 'delivered'
          AND o.order_purchase_timestamp IS NOT NULL
          {region_where};
        """
        row = dict(self._conn.execute(sql_counts, params).fetchone())
        total_orders: int = row["total_orders"]
        date_range_days: int = row["date_range_days"] or 1  # guard div-by-zero

        avg_daily_orders = round(total_orders / date_range_days, 4)
        avg_weekly_orders = round(total_orders / (date_range_days / 7.0), 4)

        # ----- Average package volume & weight -------------------------
        sql_package = f"""
        SELECT
            ROUND(AVG(p.product_length_cm * p.product_height_cm * p.product_width_cm), 2)
                AS avg_package_volume_cm3,
            ROUND(AVG(p.product_weight_g), 2)
                AS avg_package_weight_g
        FROM order_items oi
        JOIN products p ON oi.product_id = p.product_id
        JOIN orders o ON oi.order_id = o.order_id
        {region_join}
        WHERE o.order_status = 'delivered'
          AND p.product_length_cm IS NOT NULL
          AND p.product_height_cm IS NOT NULL
          AND p.product_width_cm  IS NOT NULL
          AND p.product_weight_g  IS NOT NULL
          {region_where};
        """
        pkg_row = dict(self._conn.execute(sql_package, params).fetchone())
        avg_package_volume_cm3: float = pkg_row["avg_package_volume_cm3"] or 0.0
        avg_package_weight_g: float = pkg_row["avg_package_weight_g"] or 0.0

        # ----- Transit time (avg + P90) --------------------------------
        sql_transit = f"""
        WITH transit AS (
            SELECT
                julianday(o.order_delivered_customer_date)
                    - julianday(o.order_purchase_timestamp) AS transit_days,
                PERCENT_RANK() OVER (ORDER BY
                    julianday(o.order_delivered_customer_date)
                    - julianday(o.order_purchase_timestamp)
                ) AS pct_rank
            FROM orders o
            {region_join}
            WHERE o.order_status = 'delivered'
              AND o.order_delivered_customer_date IS NOT NULL
              AND o.order_purchase_timestamp IS NOT NULL
              {region_where}
        )
        SELECT
            ROUND(AVG(transit_days), 2)                                AS avg_transit_days,
            ROUND(MAX(CASE WHEN pct_rank <= 0.9 THEN transit_days END), 2) AS p90_transit_days
        FROM transit;
        """
        transit_row = dict(self._conn.execute(sql_transit, params).fetchone())
        avg_transit_days: float = transit_row["avg_transit_days"] or 0.0
        p90_transit_days: float = transit_row["p90_transit_days"] or 0.0

        # ----- Baseline SLA breach rate --------------------------------
        sql_breach = f"""
        WITH breach_calc AS (
            SELECT
                CASE WHEN (
                    julianday(o.order_delivered_customer_date)
                    - julianday(o.order_estimated_delivery_date)
                ) > 0 THEN 1 ELSE 0 END AS is_breached
            FROM orders o
            {region_join}
            WHERE o.order_status = 'delivered'
              AND o.order_delivered_customer_date IS NOT NULL
              AND o.order_estimated_delivery_date IS NOT NULL
              {region_where}
        )
        SELECT
            ROUND(100.0 * SUM(is_breached) / MAX(COUNT(*), 1), 2) AS baseline_breach_rate_pct
        FROM breach_calc;
        """
        breach_row = dict(self._conn.execute(sql_breach, params).fetchone())
        baseline_breach_rate_pct: float = breach_row["baseline_breach_rate_pct"] or 0.0

        return {
            "avg_daily_orders": avg_daily_orders,
            "avg_weekly_orders": avg_weekly_orders,
            "avg_package_volume_cm3": avg_package_volume_cm3,
            "avg_package_weight_g": avg_package_weight_g,
            "avg_transit_days": avg_transit_days,
            "p90_transit_days": p90_transit_days,
            "baseline_breach_rate_pct": baseline_breach_rate_pct,
            "total_orders": total_orders,
            "date_range_days": date_range_days,
            "region": region or "ALL",
        }

    # ------------------------------------------------------------------
    # 5. Available regions
    # ------------------------------------------------------------------

    def get_available_regions(self) -> list[str]:
        """Return sorted distinct customer state codes.

        Returns
        -------
        list[str]
            Alphabetically sorted list of state codes present in the
            ``customers`` table.
        """
        sql = """
        SELECT DISTINCT customer_state
        FROM customers
        ORDER BY customer_state;
        """
        cur = self._conn.execute(sql)
        return [row["customer_state"] for row in cur.fetchall()]


# ---------------------------------------------------------------------------
# Module-level convenience
# ---------------------------------------------------------------------------

def get_analytics() -> BaselineAnalytics:
    """Return a ready-to-use :class:`BaselineAnalytics` instance.

    A fresh database connection is created via
    :func:`flashfleet.db.get_connection`.
    """
    return BaselineAnalytics()

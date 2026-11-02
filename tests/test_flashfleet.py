"""Unit and integration test suite for FlashFleet.

Tests:
1. Database Schema and Performance Indexes
2. SQL Analytics Module (CTEs, Window Functions, SLA breach, Percentiles)
3. Surge Simulation Engine (Fleet, Space, Cost, Bottleneck Analysis)
"""

from __future__ import annotations

import sqlite3
import unittest

from flashfleet.analytics import BaselineAnalytics
from flashfleet.config import DB_PATH
from flashfleet.seed_mock_db import seed_database
from flashfleet.simulator import SurgeParams, SurgeSimulator


class TestDatabaseSchema(unittest.TestCase):
    """Verify tables, views, and indexes in SQLite."""

    @classmethod
    def setUpClass(cls):
        seed_database(num_orders=200)

    def test_tables_exist(self):
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = {row[0] for row in cursor.fetchall()}
        conn.close()

        expected = {"orders", "order_items", "products", "geolocation", "customers", "sellers"}
        self.assertTrue(expected.issubset(tables), f"Missing tables: {expected - tables}")

    def test_indexes_exist(self):
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='index';")
        indexes = {row[0] for row in cursor.fetchall()}
        conn.close()

        expected_indexes = {
            "idx_orders_customer",
            "idx_orders_status",
            "idx_orders_purchase_ts",
            "idx_order_items_product",
            "idx_order_items_order",
            "idx_geolocation_zip",
            "idx_customers_state",
            "idx_sellers_state",
        }
        self.assertTrue(expected_indexes.issubset(indexes), f"Missing indexes: {expected_indexes - indexes}")

    def test_fulfillment_view_exists(self):
        conn = sqlite3.connect(str(DB_PATH))
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM v_order_fulfillment;")
        count = cursor.fetchone()[0]
        conn.close()
        self.assertGreater(count, 0)


class TestAnalyticsModule(unittest.TestCase):
    """Verify SQL Analytics queries utilizing CTEs and window functions."""

    def setUp(self):
        self.analytics = BaselineAnalytics()

    def test_available_regions(self):
        regions = self.analytics.get_available_regions()
        self.assertIsInstance(regions, list)
        self.assertIn("SP", regions)

    def test_delivery_sla_breach_by_region(self):
        results = self.analytics.get_delivery_sla_breach_by_region()
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)

        first = results[0]
        self.assertIn("region", first)
        self.assertIn("total_deliveries", first)
        self.assertIn("breached_orders", first)
        self.assertIn("avg_breach_days", first)
        self.assertIn("breach_rate_pct", first)
        self.assertGreaterEqual(first["breach_rate_pct"], 0.0)
        self.assertLessEqual(first["breach_rate_pct"], 100.0)

    def test_weekly_order_volume_window_function(self):
        weekly = self.analytics.get_weekly_order_volume()
        self.assertIsInstance(weekly, list)
        self.assertGreater(len(weekly), 0)

        for row in weekly:
            self.assertIn("year_week", row)
            self.assertIn("order_count", row)
            self.assertIn("rolling_4wk_avg", row)
            self.assertIn("overall_avg", row)
            self.assertGreaterEqual(row["order_count"], 1)
            self.assertGreater(row["rolling_4wk_avg"], 0)
            self.assertGreater(row["overall_avg"], 0)

    def test_transit_time_percentiles(self):
        transit = self.analytics.get_transit_time_percentiles()
        self.assertIsInstance(transit, list)

        weight_classes = {row["weight_class"] for row in transit}
        self.assertTrue(weight_classes.issubset({"heavy_freight", "lightweight"}))

        for row in transit:
            self.assertIn("min_transit_days", row)
            self.assertIn("avg_transit_days", row)
            self.assertIn("median_transit_days", row)
            self.assertIn("p90_transit_days", row)
            self.assertIn("max_transit_days", row)
            self.assertLessEqual(row["min_transit_days"], row["median_transit_days"])
            self.assertLessEqual(row["median_transit_days"], row["p90_transit_days"])
            self.assertLessEqual(row["p90_transit_days"], row["max_transit_days"])

    def test_baseline_summary(self):
        # Global baseline
        summary_all = self.analytics.get_baseline_summary(None)
        self.assertEqual(summary_all["region"], "ALL")
        self.assertGreater(summary_all["avg_daily_orders"], 0)
        self.assertGreater(summary_all["avg_package_volume_cm3"], 0)
        self.assertGreater(summary_all["avg_package_weight_g"], 0)
        self.assertGreater(summary_all["total_orders"], 0)

        # Region-filtered baseline
        summary_sp = self.analytics.get_baseline_summary("SP")
        self.assertEqual(summary_sp["region"], "SP")
        self.assertGreater(summary_sp["total_orders"], 0)


class TestSurgeSimulator(unittest.TestCase):
    """Verify guesstimate simulation engine logic and bottleneck detection."""

    def setUp(self):
        self.simulator = SurgeSimulator()

    def test_simulation_structure(self):
        params = SurgeParams(
            surge_multiplier=3.0,
            target_region="SP",
            surge_duration_days=3,
            rider_capacity_per_day=40,
            rider_daily_wage_brl=150.0,
            warehouse_cost_per_m3_day_brl=5.0,
            staging_buffer_factor=1.3,
        )
        res = self.simulator.simulate(params)

        self.assertIsNotNone(res.simulation_id)
        self.assertIsNotNone(res.timestamp)
        self.assertEqual(res.params.surge_multiplier, 3.0)
        self.assertEqual(res.params.target_region, "SP")

        # Fleet Sizing
        self.assertGreaterEqual(res.fleet.riders_needed_per_day, 1)
        self.assertEqual(res.fleet.total_rider_days, res.fleet.riders_needed_per_day * 3)
        self.assertIn("riders are needed", res.fleet.explanation)

        # Space Sizing
        self.assertGreater(res.space.avg_package_volume_cm3, 0)
        self.assertGreater(res.space.staging_area_m3, 0)
        self.assertAlmostEqual(
            res.space.staging_area_sqm_at_2m_height,
            res.space.staging_area_m3 / 2.0,
            places=3,
        )

        # Cost Projection
        expected_rider_cost = res.fleet.total_rider_days * 150.0
        expected_wh_cost = res.space.staging_area_m3 * 3 * 5.0
        self.assertAlmostEqual(res.cost.rider_cost_brl, expected_rider_cost, places=2)
        self.assertAlmostEqual(res.cost.warehouse_cost_brl, expected_wh_cost, places=2)
        self.assertAlmostEqual(
            res.cost.total_marginal_cost_brl,
            expected_rider_cost + expected_wh_cost,
            places=2,
        )

        # Bottleneck Analysis
        self.assertIn(res.bottleneck_analysis.risk_level, {"LOW", "MEDIUM", "HIGH", "CRITICAL"})
        self.assertIsInstance(res.bottleneck_analysis.bottlenecks, list)
        self.assertIsInstance(res.bottleneck_analysis.recommendations, list)

        # SLA Optimization Impact (25% reduction verification)
        self.assertAlmostEqual(res.sla_impact.sla_breach_reduction_pct, 25.0, places=1)
        self.assertLess(res.sla_impact.optimized_breach_rate_pct, res.sla_impact.baseline_breach_rate_pct)
        self.assertLess(res.sla_impact.optimized_breach_rate_pct, res.sla_impact.unmitigated_surge_breach_rate_pct)
        self.assertIn("25.0% reduction", res.sla_impact.explanation)

    def test_extreme_surge_critical_risk(self):
        params = SurgeParams(
            surge_multiplier=6.0,  # >= 5.0 triggers CRITICAL
            surge_duration_days=7,
        )
        res = self.simulator.simulate(params)
        self.assertEqual(res.bottleneck_analysis.risk_level, "CRITICAL")
        self.assertTrue(any("overwhelm" in b.lower() for b in res.bottleneck_analysis.bottlenecks))


if __name__ == "__main__":
    unittest.main()


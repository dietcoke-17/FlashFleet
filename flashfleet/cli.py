"""FlashFleet Command-Line Interface (CLI).

Run simulations and view analytics directly from your terminal.

Examples:
    python3 -m flashfleet.cli simulate --surge 4.0 --region SP
    python3 -m flashfleet.cli analytics --type sla
    python3 -m flashfleet.cli analytics --type weekly
    python3 -m flashfleet.cli analytics --type transit
    python3 -m flashfleet.cli seed --orders 1500
"""

from __future__ import annotations

import argparse
import json
import sys

from flashfleet.analytics import get_analytics
from flashfleet.simulator import SurgeParams, SurgeSimulator


def cmd_simulate(args: argparse.Namespace) -> None:
    """Run a surge simulation and print formatted results."""
    params = SurgeParams(
        surge_multiplier=args.surge,
        target_region=args.region,
        surge_duration_days=args.duration,
        rider_capacity_per_day=args.rider_capacity,
        rider_daily_wage_brl=args.rider_wage,
        warehouse_cost_per_m3_day_brl=args.warehouse_rate,
        staging_buffer_factor=args.buffer_factor,
    )
    sim = SurgeSimulator()
    res = sim.simulate(params)

    if args.json:
        print(res.model_dump_json(indent=2))
        return

    print("=" * 70)
    print("FLASHFLEET SURGE SIMULATION RESULTS")
    print("=" * 70)
    print(f"Simulation ID: {res.simulation_id}")
    print(f"Timestamp:     {res.timestamp}")
    print(f"Target Region: {res.params.target_region or 'ALL'}")
    print(f"Surge Factor:  {res.params.surge_multiplier:.1f}x for {res.params.surge_duration_days} days")
    print("-" * 70)

    print("\n[1] BASELINE OPERATIONAL METRICS")
    print(f"  • Avg Daily Orders:        {res.baseline['avg_daily_orders']:,.1f}")
    print(f"  • Avg Package Volume:      {res.baseline['avg_package_volume_cm3']:,.1f} cm³")
    print(f"  • Avg Transit Time:        {res.baseline['avg_transit_days']:.1f} days (P90: {res.baseline['p90_transit_days']:.1f} days)")

    print("\n[2] FLEET SIZING REQUIREMENTS")
    print(f"  • Surge Daily Orders:      {res.fleet.surge_daily_orders:,.1f}")
    print(f"  • Total Projected Orders:  {res.fleet.total_surge_orders:,}")
    print(f"  • Riders Needed / Day:     {res.fleet.riders_needed_per_day:,} (capacity: {args.rider_capacity} pkgs/day)")
    print(f"  • Total Rider-Days:        {res.fleet.total_rider_days:,}")

    print("\n[3] WAREHOUSE SPACE SIZING")
    print(f"  • Total Surge Volume:      {res.space.total_surge_volume_m3:,.2f} m³")
    print(f"  • Staging Area Required:   {res.space.staging_area_m3:,.2f} m³ (buffer: {args.buffer_factor}x)")
    print(f"  • Staging Floor Footprint: {res.space.staging_area_sqm_at_2m_height:,.2f} m² (@ 2m stacking height)")

    print("\n[4] MARGINAL COST PROJECTION")
    print(f"  • Rider Wages:             R${res.cost.rider_cost_brl:,.2f}")
    print(f"  • Spot Warehouse Leasing:  R${res.cost.warehouse_cost_brl:,.2f}")
    print(f"  • Total Marginal Cost:     R${res.cost.total_marginal_cost_brl:,.2f}")
    print(f"  • Cost Per Surge Order:    R${res.cost.cost_per_order_brl:,.2f}")

    print("\n[5] ACTIONABLE SLA OPTIMIZATION IMPACT")
    print(f"  • Baseline SLA Breach:     {res.sla_impact.baseline_breach_rate_pct:.1f}%")
    print(f"  • Unmitigated Surge Risk:  {res.sla_impact.unmitigated_surge_breach_rate_pct:.1f}%")
    print(f"  • Mitigated Breach Rate:   {res.sla_impact.optimized_breach_rate_pct:.1f}% (-{res.sla_impact.sla_breach_reduction_pct:.1f}% reduction)")
    print(f"  • Orders Protected:        {res.sla_impact.prevented_breaches:,} deliveries saved from SLA breach")

    print("\n[6] BOTTLENECK & RISK ANALYSIS")
    print(f"  • Risk Level:              [{res.bottleneck_analysis.risk_level}]")
    if res.bottleneck_analysis.bottlenecks:
        print("  • Identified Bottlenecks:")
        for b in res.bottleneck_analysis.bottlenecks:
            print(f"     ⚠ {b}")
    print("  • Strategic Recommendations:")
    for r in res.bottleneck_analysis.recommendations:
        print(f"     ✔ {r}")
    print("=" * 70)


def cmd_analytics(args: argparse.Namespace) -> None:
    """Run baseline SQL queries and display output."""
    analytics = get_analytics()

    if args.type in ("sla", "breaches"):
        data = analytics.get_delivery_sla_breach_by_region()
        print(f"Delivery SLA Breaches by Region ({len(data)} regions):")
        print(json.dumps(data, indent=2))
    elif args.type == "weekly":
        data = analytics.get_weekly_order_volume()
        print(f"Weekly Order Volume Density ({len(data)} weeks):")
        print(json.dumps(data, indent=2))
    elif args.type == "transit":
        data = analytics.get_transit_time_percentiles()
        print("Transit Time Percentiles by Freight Class:")
        print(json.dumps(data, indent=2))
    elif args.type == "baseline":
        data = analytics.get_baseline_summary(args.region)
        print(f"Baseline Summary for Region [{args.region or 'ALL'}]:")
        print(json.dumps(data, indent=2))
    elif args.type == "regions":
        data = analytics.get_available_regions()
        print("Available Customer State Codes:")
        print(data)


def cmd_seed(args: argparse.Namespace) -> None:
    """Seed synthetic testing data into local SQLite database."""
    from flashfleet.seed_mock_db import seed_database
    seed_database(num_orders=args.orders)


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="flashfleet",
        description="FlashFleet: E-Commerce Fulfillment & Surge Capacity Simulator CLI",
    )
    subparsers = parser.add_subparsers(dest="subcommand", required=True)

    # simulate
    p_sim = subparsers.add_parser("simulate", help="Run surge capacity simulation")
    p_sim.add_argument("--surge", type=float, default=3.0, help="Surge multiplier (e.g. 3.0)")
    p_sim.add_argument("--region", type=str, default=None, help="Target region code (e.g. SP)")
    p_sim.add_argument("--duration", type=int, default=3, help="Duration in days")
    p_sim.add_argument("--rider-capacity", type=int, default=40, help="Packages per rider per day")
    p_sim.add_argument("--rider-wage", type=float, default=150.0, help="Rider daily wage in BRL")
    p_sim.add_argument("--warehouse-rate", type=float, default=5.0, help="Lease rate/m³/day in BRL")
    p_sim.add_argument("--buffer-factor", type=float, default=1.3, help="Warehouse buffer factor")
    p_sim.add_argument("--json", action="store_true", help="Output raw JSON")
    p_sim.set_defaults(func=cmd_simulate)

    # analytics
    p_ana = subparsers.add_parser("analytics", help="Execute baseline SQL queries")
    p_ana.add_argument(
        "--type",
        choices=["sla", "breaches", "weekly", "transit", "baseline", "regions"],
        default="sla",
        help="Query type to execute",
    )
    p_ana.add_argument("--region", type=str, default=None, help="State filter for baseline")
    p_ana.set_defaults(func=cmd_analytics)

    # seed
    p_seed = subparsers.add_parser("seed", help="Seed mock database")
    p_seed.add_argument("--orders", type=int, default=1200, help="Number of orders to generate")
    p_seed.set_defaults(func=cmd_seed)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()


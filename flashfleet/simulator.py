"""FlashFleet Surge Simulation Engine.

This module provides a guesstimate-style simulation for flash-sale logistics
planning.  Given historical baseline metrics (from ``flashfleet.analytics``)
and a set of surge parameters, it computes:

* **Fleet sizing** — how many temporary riders are needed.
* **Space sizing** — warehouse staging area required.
* **Cost projection** — marginal cost of the surge operation.
* **Bottleneck analysis** — risk assessment with actionable recommendations.
"""

from __future__ import annotations

import math
import uuid
from datetime import datetime, timezone

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Pydantic models — Inputs
# ---------------------------------------------------------------------------


class SurgeParams(BaseModel):
    """User-facing knobs that control the surge simulation."""

    surge_multiplier: float = Field(
        default=3.0,
        ge=1.0,
        le=20.0,
        description="Demand multiplier (e.g., 3.0 = 300% increase)",
    )
    target_region: str | None = Field(
        default=None,
        description="Target state code (e.g., 'SP', 'RJ'). None = all regions",
    )
    surge_duration_days: int = Field(
        default=3,
        ge=1,
        le=30,
        description="Duration of the flash sale in days",
    )
    rider_capacity_per_day: int = Field(
        default=40,
        ge=1,
        description="Packages a single rider can deliver per day",
    )
    rider_daily_wage_brl: float = Field(
        default=150.0,
        ge=0,
        description="Daily wage for a temporary rider in BRL",
    )
    warehouse_cost_per_m3_day_brl: float = Field(
        default=5.0,
        ge=0,
        description="Spot warehouse lease cost per cubic meter per day in BRL",
    )
    staging_buffer_factor: float = Field(
        default=1.3,
        ge=1.0,
        le=3.0,
        description=(
            "Buffer multiplier for warehouse staging area "
            "(1.3 = 30% extra)"
        ),
    )


# ---------------------------------------------------------------------------
# Pydantic models — Output components
# ---------------------------------------------------------------------------


class FleetSizing(BaseModel):
    """Rider / fleet requirements derived from the surge scenario."""

    baseline_daily_orders: float
    surge_daily_orders: float
    total_surge_orders: int
    riders_needed_per_day: int
    total_rider_days: int
    explanation: str


class SpaceSizing(BaseModel):
    """Warehouse staging-area requirements."""

    avg_package_volume_cm3: float
    avg_package_volume_m3: float
    total_surge_volume_m3: float
    staging_area_m3: float  # with buffer
    staging_area_sqm_at_2m_height: float  # assuming 2m stacking height
    explanation: str


class CostProjection(BaseModel):
    """Marginal cost breakdown for the surge period."""

    rider_cost_brl: float
    warehouse_cost_brl: float
    total_marginal_cost_brl: float
    cost_per_order_brl: float
    explanation: str


class BottleneckAnalysis(BaseModel):
    """Risk assessment with identified bottlenecks and recommendations."""

    risk_level: str  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    bottlenecks: list[str]
    recommendations: list[str]


class SurgeSimulationResult(BaseModel):
    """Complete output of a single surge simulation run."""

    simulation_id: str
    timestamp: str
    params: SurgeParams
    baseline: dict
    fleet: FleetSizing
    space: SpaceSizing
    cost: CostProjection
    bottleneck_analysis: BottleneckAnalysis


# ---------------------------------------------------------------------------
# Simulation engine
# ---------------------------------------------------------------------------


class SurgeSimulator:
    """Core simulation engine that ties baseline analytics to surge planning.

    Usage::

        from flashfleet.simulator import SurgeSimulator, SurgeParams

        sim = SurgeSimulator()
        result = sim.simulate(SurgeParams(surge_multiplier=5.0, target_region="SP"))
        print(result.model_dump_json(indent=2))
    """

    def __init__(self) -> None:
        from flashfleet.analytics import get_analytics  # noqa: WPS433

        self.analytics = get_analytics()

    # -- public API ---------------------------------------------------------

    def simulate(self, params: SurgeParams) -> SurgeSimulationResult:
        """Run the full surge simulation and return a structured result.

        Args:
            params: Surge scenario parameters supplied by the user.

        Returns:
            A :class:`SurgeSimulationResult` containing fleet sizing, space
            sizing, cost projection, and bottleneck analysis.
        """
        baseline = self.analytics.get_baseline_summary(params.target_region)

        fleet = self._compute_fleet_sizing(baseline, params)
        space = self._compute_space_sizing(baseline, fleet, params)
        cost = self._compute_cost_projection(fleet, space, params)
        bottleneck = self._compute_bottleneck_analysis(
            baseline, fleet, space, cost, params
        )

        return SurgeSimulationResult(
            simulation_id=str(uuid.uuid4()),
            timestamp=datetime.now(timezone.utc).isoformat(),
            params=params,
            baseline=baseline,
            fleet=fleet,
            space=space,
            cost=cost,
            bottleneck_analysis=bottleneck,
        )

    # -- private helpers ----------------------------------------------------

    @staticmethod
    def _compute_fleet_sizing(
        baseline: dict,
        params: SurgeParams,
    ) -> FleetSizing:
        """Determine how many riders are required for the surge period."""
        baseline_daily = baseline["avg_daily_orders"]
        surge_daily = baseline_daily * params.surge_multiplier
        total_surge = int(surge_daily * params.surge_duration_days)
        riders_per_day = math.ceil(surge_daily / params.rider_capacity_per_day)
        total_rider_days = riders_per_day * params.surge_duration_days

        explanation = (
            f"Baseline daily orders: {baseline_daily:,.1f}. "
            f"With a {params.surge_multiplier}x surge multiplier, "
            f"surge daily orders = {surge_daily:,.1f}. "
            f"Over {params.surge_duration_days} day(s) that totals "
            f"{total_surge:,} orders. "
            f"At {params.rider_capacity_per_day} packages/rider/day, "
            f"{riders_per_day:,} riders are needed each day "
            f"({total_rider_days:,} total rider-days)."
        )

        return FleetSizing(
            baseline_daily_orders=baseline_daily,
            surge_daily_orders=surge_daily,
            total_surge_orders=total_surge,
            riders_needed_per_day=riders_per_day,
            total_rider_days=total_rider_days,
            explanation=explanation,
        )

    @staticmethod
    def _compute_space_sizing(
        baseline: dict,
        fleet: FleetSizing,
        params: SurgeParams,
    ) -> SpaceSizing:
        """Estimate warehouse staging-area requirements."""
        avg_vol_cm3 = baseline["avg_package_volume_cm3"]
        avg_vol_m3 = avg_vol_cm3 / 1_000_000
        total_surge_vol_m3 = avg_vol_m3 * fleet.total_surge_orders
        staging_m3 = total_surge_vol_m3 * params.staging_buffer_factor
        staging_sqm = staging_m3 / 2.0  # 2 m stacking height

        explanation = (
            f"Average package volume: {avg_vol_cm3:,.1f} cm³ "
            f"({avg_vol_m3:.6f} m³). "
            f"Total surge volume for {fleet.total_surge_orders:,} orders: "
            f"{total_surge_vol_m3:,.2f} m³. "
            f"With a {params.staging_buffer_factor}x staging buffer: "
            f"{staging_m3:,.2f} m³. "
            f"At 2 m stacking height ≈ {staging_sqm:,.2f} m² of floor space."
        )

        return SpaceSizing(
            avg_package_volume_cm3=avg_vol_cm3,
            avg_package_volume_m3=avg_vol_m3,
            total_surge_volume_m3=total_surge_vol_m3,
            staging_area_m3=staging_m3,
            staging_area_sqm_at_2m_height=staging_sqm,
            explanation=explanation,
        )

    @staticmethod
    def _compute_cost_projection(
        fleet: FleetSizing,
        space: SpaceSizing,
        params: SurgeParams,
    ) -> CostProjection:
        """Project the marginal cost of the surge operation."""
        rider_cost = fleet.total_rider_days * params.rider_daily_wage_brl
        warehouse_cost = (
            space.staging_area_m3
            * params.surge_duration_days
            * params.warehouse_cost_per_m3_day_brl
        )
        total_cost = rider_cost + warehouse_cost
        cost_per_order = total_cost / max(fleet.total_surge_orders, 1)

        explanation = (
            f"Rider cost: {fleet.total_rider_days:,} rider-days × "
            f"R${params.rider_daily_wage_brl:,.2f} = R${rider_cost:,.2f}. "
            f"Warehouse cost: {space.staging_area_m3:,.2f} m³ × "
            f"{params.surge_duration_days} days × "
            f"R${params.warehouse_cost_per_m3_day_brl:,.2f}/m³/day = "
            f"R${warehouse_cost:,.2f}. "
            f"Total marginal cost: R${total_cost:,.2f} "
            f"(R${cost_per_order:,.2f} per order)."
        )

        return CostProjection(
            rider_cost_brl=rider_cost,
            warehouse_cost_brl=warehouse_cost,
            total_marginal_cost_brl=total_cost,
            cost_per_order_brl=cost_per_order,
            explanation=explanation,
        )

    @staticmethod
    def _compute_bottleneck_analysis(
        baseline: dict,
        fleet: FleetSizing,
        space: SpaceSizing,
        cost: CostProjection,
        params: SurgeParams,
    ) -> BottleneckAnalysis:
        """Assess operational risks and generate recommendations."""
        bottlenecks: list[str] = []
        recommendations: list[str] = []
        risk_level = "LOW"

        # --- Rule: extreme demand surge ---
        if params.surge_multiplier >= 5.0:
            risk_level = "CRITICAL"
            bottlenecks.append(
                "Extreme demand surge may overwhelm last-mile delivery network"
            )
            recommendations.append(
                "Consider multi-wave flash sale to flatten demand peak"
            )
        elif params.surge_multiplier >= 3.0:
            risk_level = "HIGH"

        # --- Rule: large temporary workforce ---
        if fleet.riders_needed_per_day > 500:
            bottlenecks.append(
                "Large temporary workforce requires significant "
                "recruitment lead time"
            )
            recommendations.append(
                "Start rider recruitment at least 2 weeks in advance and "
                "partner with gig-economy platforms for rapid scaling"
            )

        # --- Rule: slow transit times ---
        if baseline.get("p90_transit_days", 0) > 15:
            bottlenecks.append(
                "Region has historically slow transit times (P90 > 15 days)"
            )
            recommendations.append(
                "Pre-position inventory in regional hubs closer to end "
                "customers to cut last-mile distance"
            )

        # --- Rule: large warehouse staging ---
        staging_sqm = space.staging_area_sqm_at_2m_height
        if staging_sqm > 5000:
            bottlenecks.append(
                "Warehouse staging requirement exceeds typical "
                "flex-space availability"
            )
            recommendations.append(
                "Negotiate bulk warehouse rates or split staging across "
                "multiple smaller facilities"
            )

        # --- Rule: high per-order cost ---
        if cost.cost_per_order_brl > 50:
            bottlenecks.append(
                "Per-order marginal cost is high, potentially eroding margins"
            )
            recommendations.append(
                "Explore shared-logistics partnerships or dynamic pricing to "
                "offset elevated per-order costs"
            )

        # --- Determine final risk level (upgrade only) ---
        if bottlenecks and risk_level == "LOW":
            risk_level = "MEDIUM"

        # --- Fallback for clean scenario ---
        if not bottlenecks:
            risk_level = "LOW"
            recommendations.append(
                "No major bottlenecks detected. Continue monitoring demand "
                "signals and adjust rider allocation dynamically."
            )

        return BottleneckAnalysis(
            risk_level=risk_level,
            bottlenecks=bottlenecks,
            recommendations=recommendations,
        )

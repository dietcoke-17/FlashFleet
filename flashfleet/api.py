"""FlashFleet REST API — Phase 4.

Wraps the analytics and simulation engine in a FastAPI application,
exposing endpoints for surge simulation and baseline exploration.

Start the server::

    uvicorn flashfleet.api:app --reload
"""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, JSONResponse

from flashfleet.analytics import BaselineAnalytics, get_analytics
from flashfleet.dashboard_html import DASHBOARD_HTML
from flashfleet.simulator import SurgeParams, SurgeSimulator, SurgeSimulationResult

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

app = FastAPI(
    title="FlashFleet",
    description=(
        "E-Commerce Fulfillment & Surge Capacity Simulator — "
        "analyse historical Olist data and guesstimate logistics "
        "requirements for flash-sale demand surges."
    ),
    version="1.0.0",
)


# ---------------------------------------------------------------------------
# Lifespan / shared state
# ---------------------------------------------------------------------------

_simulator: SurgeSimulator | None = None
_analytics: BaselineAnalytics | None = None


def _get_simulator() -> SurgeSimulator:
    global _simulator  # noqa: WPS420
    if _simulator is None:
        _simulator = SurgeSimulator()
    return _simulator


def _get_analytics() -> BaselineAnalytics:
    global _analytics  # noqa: WPS420
    if _analytics is None:
        _analytics = get_analytics()
    return _analytics


# ---------------------------------------------------------------------------
# Interactive Web Dashboard
# ---------------------------------------------------------------------------


@app.get("/", response_class=HTMLResponse, tags=["ui"])
def dashboard() -> HTMLResponse:
    """Serve the interactive FlashFleet logistics simulation dashboard."""
    return HTMLResponse(content=DASHBOARD_HTML)


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------


@app.get("/health", tags=["ops"])
def health_check() -> dict[str, str]:
    """Basic liveness probe."""
    return {"status": "ok", "service": "flashfleet"}


# ---------------------------------------------------------------------------
# Core simulation endpoint
# ---------------------------------------------------------------------------


@app.post(
    "/simulate-surge",
    response_model=SurgeSimulationResult,
    tags=["simulation"],
    summary="Run a flash-sale surge simulation",
    description=(
        "Accepts surge parameters, pulls baseline metrics from the "
        "historical data via SQL, runs the guesstimate engine, and "
        "returns a structured JSON payload with fleet sizing, warehouse "
        "space requirements, cost projections, and bottleneck analysis."
    ),
)
def simulate_surge(params: SurgeParams) -> SurgeSimulationResult:
    """Execute the full surge simulation pipeline."""
    try:
        simulator = _get_simulator()
        result = simulator.simulate(params)
        return result
    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Database not found. Run the ingestion pipeline first: "
                "python -m flashfleet.ingest"
            ),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Simulation failed: {exc}",
        ) from exc


# ---------------------------------------------------------------------------
# Analytics exploration endpoints
# ---------------------------------------------------------------------------


@app.get(
    "/analytics/regions",
    tags=["analytics"],
    summary="List available regions",
)
def list_regions() -> dict[str, list[str]]:
    """Return all customer state codes present in the database."""
    analytics = _get_analytics()
    return {"regions": analytics.get_available_regions()}


@app.get(
    "/analytics/baseline",
    tags=["analytics"],
    summary="Get baseline summary metrics",
)
def get_baseline(
    region: str | None = Query(
        default=None,
        description="Customer state code (e.g. 'SP'). Omit for all regions.",
    ),
) -> dict[str, Any]:
    """Return consolidated baseline operational metrics."""
    analytics = _get_analytics()
    return analytics.get_baseline_summary(region)


@app.get(
    "/analytics/sla-breaches",
    tags=["analytics"],
    summary="Delivery SLA breach analysis by region",
)
def get_sla_breaches() -> list[dict[str, Any]]:
    """Delivery SLA breach rates segmented by customer state."""
    analytics = _get_analytics()
    return analytics.get_delivery_sla_breach_by_region()


@app.get(
    "/analytics/weekly-volume",
    tags=["analytics"],
    summary="Weekly order volume with rolling average",
)
def get_weekly_volume() -> list[dict[str, Any]]:
    """Weekly order counts with 4-week rolling and overall averages."""
    analytics = _get_analytics()
    return analytics.get_weekly_order_volume()


@app.get(
    "/analytics/transit-percentiles",
    tags=["analytics"],
    summary="Transit time percentiles by weight class",
)
def get_transit_percentiles() -> list[dict[str, Any]]:
    """Transit-time distributions for heavy freight vs lightweight parcels."""
    analytics = _get_analytics()
    return analytics.get_transit_time_percentiles()


# ---------------------------------------------------------------------------
# Custom exception handler for nicer error payloads
# ---------------------------------------------------------------------------


@app.exception_handler(HTTPException)
async def custom_http_exception_handler(request, exc):  # noqa: ANN001
    """Return a consistent error payload shape."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "detail": exc.detail,
        },
    )


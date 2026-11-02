# FlashFleet: E-Commerce Fulfillment & Surge Capacity Simulator

A data pipeline and simulation engine that ingests historical Brazilian e-commerce delivery data (Olist), identifies operational bottlenecks using SQL analytics, and guesstimates the logistics requirements needed to handle dynamic demand surges during flash sales.

## Architecture

```
┌──────────────┐     ┌─────────────────┐     ┌──────────────────┐     ┌───────────┐
│  Olist CSVs  │────▶│  ingest.py      │────▶│  SQLite DB       │────▶│  FastAPI   │
│  (Kaggle)    │     │  Clean & Load   │     │  flashfleet.db   │     │  REST API  │
└──────────────┘     └─────────────────┘     └──────┬───────────┘     └─────┬─────┘
                                                     │                       │
                                               ┌─────▼──────┐         ┌─────▼──────┐
                                               │ analytics  │         │ simulator  │
                                               │ SQL CTEs + │◀────────│ Guesstimate│
                                               │ Windows    │ baseline│ Engine     │
                                               └────────────┘         └────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
cd FlashFleet
pip install -r requirements.txt
```

### 2. Database Ingestion & Seeding

You can ingest the full historical dataset or generate a local synthetic seed:

**Option A: Ingest Real Olist Dataset (Kaggle)**
```bash
python3 -m flashfleet.ingest
```
*Note: Automatically downloads via `kagglehub` if `KAGGLE_USERNAME` and `KAGGLE_KEY` are configured, or reads manual CSVs placed in `data/`.*

**Option B: Instant Local Seeding (No Kaggle or downloads needed)**
```bash
python3 -m flashfleet.ingest --seed
```

### 3. Run the CLI Simulation

Simulate a flash-sale demand surge directly in your terminal:

```bash
# 4x surge in São Paulo (SP) over a 3-day flash sale
python3 -m flashfleet.cli simulate --surge 4.0 --region SP --duration 3

# View delivery SLA breaches by Brazilian state
python3 -m flashfleet.cli analytics --type sla

# View heavy freight vs lightweight transit times
python3 -m flashfleet.cli analytics --type transit
```

### 4. Run the Unit & Integration Tests

```bash
python3 -m unittest discover -s tests
```

### 5. Start the FastAPI REST API Server

```bash
uvicorn flashfleet.api:app --reload
```
Or simply run:
```bash
./run.sh
```
Open **`http://127.0.0.1:8000`** in your browser for the interactive simulator dashboard.

---

## Deploy to Vercel

FlashFleet is pre-configured for serverless deployment on Vercel:

1. Push your repository to GitHub (already completed at [`dietcoke-17/FlashFleet`](https://github.com/dietcoke-17/FlashFleet)).
2. Log in to [Vercel Dashboard](https://vercel.com/new).
3. Select **Import** next to your `dietcoke-17/FlashFleet` repository.
4. Leave all default build settings (**Other** framework preset) — Vercel detects `vercel.json` and `api/index.py` automatically.
5. Click **Deploy**.

Alternatively, deploy directly from your command line:
```bash
npx vercel
```

The server runs at `http://127.0.0.1:8000`. Interactive API docs are at `http://127.0.0.1:8000/docs`.

## API Endpoints

### `POST /simulate-surge` — Core Simulation

Runs the full surge simulation pipeline. Accepts a JSON body with tunable parameters:

```json
{
  "surge_multiplier": 3.0,
  "target_region": "SP",
  "surge_duration_days": 3,
  "rider_capacity_per_day": 40,
  "rider_daily_wage_brl": 150.0,
  "warehouse_cost_per_m3_day_brl": 5.0,
  "staging_buffer_factor": 1.3
}
```

**Response** includes:
- **Fleet Sizing** — riders needed per day, total rider-days
- **Space Sizing** — warehouse staging area in m³ and m²
- **Cost Projection** — rider costs, warehouse costs, per-order marginal cost
- **Bottleneck Analysis** — risk level (LOW/MEDIUM/HIGH/CRITICAL) with actionable recommendations

### `GET /analytics/baseline` — Baseline Metrics

Returns consolidated baseline metrics. Optional `?region=SP` query parameter.

### `GET /analytics/sla-breaches` — SLA Breach Analysis

Delivery SLA breach rates segmented by geographic region (customer state).

### `GET /analytics/weekly-volume` — Order Volume Trends

Weekly order counts with 4-week rolling average and overall average.

### `GET /analytics/transit-percentiles` — Transit Time Analysis

90th percentile transit times for heavy freight (≥5kg) vs lightweight parcels.

### `GET /analytics/regions` — Available Regions

Lists all customer state codes in the dataset.

### `GET /health` — Health Check

Basic liveness probe.

## Example: cURL Simulation

```bash
curl -X POST http://127.0.0.1:8000/simulate-surge \
  -H "Content-Type: application/json" \
  -d '{
    "surge_multiplier": 5.0,
    "target_region": "SP",
    "surge_duration_days": 5,
    "rider_capacity_per_day": 40,
    "rider_daily_wage_brl": 150,
    "warehouse_cost_per_m3_day_brl": 5.0,
    "staging_buffer_factor": 1.5
  }'
```

## Project Structure

```
FlashFleet/
├── flashfleet/
│   ├── __init__.py          # Package init
│   ├── config.py            # Constants (paths, table mappings)
│   ├── db.py                # SQLite connection utilities
│   ├── ingest.py            # Phase 1: Data ingestion pipeline (Kaggle / local)
│   ├── seed_mock_db.py      # Synthetic database generator
│   ├── analytics.py         # Phase 2: SQL analytics (CTEs, window functions)
│   ├── simulator.py         # Phase 3: Guesstimate simulation engine
│   ├── cli.py               # Terminal simulation & analytics CLI
│   └── api.py               # Phase 4: FastAPI REST API
├── tests/
│   └── test_flashfleet.py   # Unit & integration test suite
├── data/                    # CSV directory (auto-created)
├── flashfleet.db            # SQLite database
├── requirements.txt         # Dependencies
└── README.md
```

## Tech Stack

- **Database:** SQLite
- **Backend:** Python with FastAPI
- **Data Processing:** Pandas
- **Validation:** Pydantic v2
- **Data Source:** [Olist Brazilian E-Commerce Dataset](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)


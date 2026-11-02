"""HTML template for the FlashFleet interactive web dashboard."""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>FlashFleet — Logistics Surge Capacity Simulator</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg: #0b0f19;
      --card-bg: #111827;
      --card-border: #1f2937;
      --card-hover: #1e293b;
      --text-main: #f9fafb;
      --text-muted: #94a3b8;
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --accent-cyan: #06b6d4;
      --accent-emerald: #10b981;
      --accent-amber: #f59e0b;
      --accent-rose: #f43f5e;
      --accent-purple: #8b5cf6;
      --radius: 14px;
      --font: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
      --mono: 'JetBrains Mono', monospace;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg);
      color: var(--text-main);
      font-family: var(--font);
      min-height: 100vh;
      line-height: 1.5;
      padding-bottom: 60px;
    }

    /* Header */
    header {
      background: linear-gradient(180deg, rgba(30, 41, 59, 0.7) 0%, rgba(15, 23, 42, 0) 100%);
      border-bottom: 1px solid var(--card-border);
      padding: 1.25rem 2rem;
      display: flex;
      justify-content: space-between;
      align-items: center;
      position: sticky;
      top: 0;
      backdrop-filter: blur(12px);
      z-index: 50;
    }
    .brand {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .logo-badge {
      background: linear-gradient(135deg, #3b82f6 0%, #8b5cf6 100%);
      color: white;
      font-weight: 800;
      font-size: 1.25rem;
      width: 40px;
      height: 40px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 14px rgba(59, 130, 246, 0.4);
    }
    .brand-title h1 {
      font-size: 1.35rem;
      font-weight: 800;
      letter-spacing: -0.02em;
      background: linear-gradient(90deg, #ffffff 0%, #cbd5e1 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .brand-title p {
      font-size: 0.8rem;
      color: var(--text-muted);
    }
    .header-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .status-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      background: rgba(16, 185, 129, 0.12);
      border: 1px solid rgba(16, 185, 129, 0.3);
      color: #34d399;
      font-size: 0.75rem;
      font-weight: 600;
      padding: 6px 12px;
      border-radius: 9999px;
    }
    .status-dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 10px #10b981;
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.5; transform: scale(0.85); }
    }
    .docs-btn {
      color: var(--text-muted);
      text-decoration: none;
      font-size: 0.82rem;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: 8px;
      border: 1px solid var(--card-border);
      background: var(--card-bg);
      transition: all 0.2s;
    }
    .docs-btn:hover {
      color: white;
      border-color: #3b82f6;
    }

    /* Layout */
    .container {
      max-width: 1400px;
      margin: 0 auto;
      padding: 2rem 1.5rem;
    }
    .grid-main {
      display: grid;
      grid-template-columns: 380px 1fr;
      gap: 1.75rem;
      align-items: start;
    }
    @media (max-width: 1024px) {
      .grid-main { grid-template-columns: 1fr; }
    }

    /* Cards */
    .card {
      background: var(--card-bg);
      border: 1px solid var(--card-border);
      border-radius: var(--radius);
      padding: 1.5rem;
      box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
    }
    .card-title {
      font-size: 1.1rem;
      font-weight: 700;
      margin-bottom: 0.25rem;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .card-subtitle {
      font-size: 0.8rem;
      color: var(--text-muted);
      margin-bottom: 1.25rem;
    }

    /* Form Controls */
    .form-group {
      margin-bottom: 1.25rem;
    }
    .form-group label {
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      font-weight: 600;
      color: #e2e8f0;
      margin-bottom: 0.4rem;
    }
    .form-group label span.val {
      color: var(--accent-cyan);
      font-family: var(--mono);
      font-weight: 700;
    }
    .input-range {
      width: 100%;
      height: 6px;
      border-radius: 4px;
      background: #334155;
      outline: none;
      -webkit-appearance: none;
    }
    .input-range::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--primary);
      cursor: pointer;
      box-shadow: 0 0 10px var(--primary);
      transition: 0.15s;
    }
    .input-range::-webkit-slider-thumb:hover {
      transform: scale(1.15);
    }
    .input-select, .input-text {
      width: 100%;
      padding: 0.65rem 0.85rem;
      background: #1e293b;
      border: 1px solid #334155;
      border-radius: 8px;
      color: white;
      font-family: var(--font);
      font-size: 0.88rem;
      outline: none;
      transition: border 0.2s;
    }
    .input-select:focus, .input-text:focus {
      border-color: var(--primary);
    }
    .presets {
      display: flex;
      gap: 6px;
      margin-bottom: 1.25rem;
      flex-wrap: wrap;
    }
    .preset-btn {
      background: #1e293b;
      border: 1px solid #334155;
      color: #cbd5e1;
      padding: 4px 10px;
      border-radius: 6px;
      font-size: 0.75rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }
    .preset-btn:hover {
      background: #334155;
      color: white;
    }
    .preset-btn.active {
      background: rgba(59, 130, 246, 0.2);
      border-color: var(--primary);
      color: #60a5fa;
    }

    .btn-run {
      width: 100%;
      padding: 0.85rem;
      background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
      color: white;
      border: none;
      border-radius: 10px;
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 18px rgba(59, 130, 246, 0.4);
      transition: all 0.2s;
    }
    .btn-run:hover {
      transform: translateY(-1px);
      box-shadow: 0 6px 24px rgba(59, 130, 246, 0.5);
    }

    /* Results Header / Risk Banner */
    .risk-banner {
      border-radius: var(--radius);
      padding: 1.25rem 1.5rem;
      margin-bottom: 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border: 1px solid transparent;
      transition: all 0.3s;
    }
    .risk-CRITICAL {
      background: rgba(244, 63, 94, 0.12);
      border-color: rgba(244, 63, 94, 0.4);
      color: #fb7185;
    }
    .risk-HIGH {
      background: rgba(245, 158, 11, 0.12);
      border-color: rgba(245, 158, 11, 0.4);
      color: #fbbf24;
    }
    .risk-MEDIUM {
      background: rgba(59, 130, 246, 0.12);
      border-color: rgba(59, 130, 246, 0.4);
      color: #60a5fa;
    }
    .risk-LOW {
      background: rgba(16, 185, 129, 0.12);
      border-color: rgba(16, 185, 129, 0.4);
      color: #34d399;
    }
    .risk-title {
      font-size: 1.15rem;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .risk-badge {
      padding: 4px 12px;
      border-radius: 9999px;
      font-size: 0.78rem;
      font-weight: 800;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      background: currentColor;
    }
    .risk-badge span {
      color: #0b0f19;
    }

    /* KPI Grid */
    .kpi-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }
    .kpi-card {
      background: #162032;
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 1.15rem;
      position: relative;
      overflow: hidden;
    }
    .kpi-card::before {
      content: "";
      position: absolute;
      top: 0;
      left: 0;
      width: 4px;
      height: 100%;
      background: var(--kpi-color, #3b82f6);
    }
    .kpi-label {
      font-size: 0.75rem;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 0.35rem;
    }
    .kpi-value {
      font-size: 1.65rem;
      font-weight: 800;
      font-family: var(--font);
      letter-spacing: -0.02em;
      color: #ffffff;
      margin-bottom: 0.2rem;
    }
    .kpi-desc {
      font-size: 0.78rem;
      color: #94a3b8;
    }

    /* Breakdown section */
    .breakdown-card {
      background: #141d2e;
      border: 1px solid var(--card-border);
      border-radius: 12px;
      padding: 1.25rem;
      margin-bottom: 1.25rem;
    }
    .breakdown-header {
      font-size: 0.92rem;
      font-weight: 700;
      margin-bottom: 0.5rem;
      display: flex;
      align-items: center;
      gap: 8px;
      color: #e2e8f0;
    }
    .breakdown-text {
      font-size: 0.84rem;
      color: #cbd5e1;
      line-height: 1.6;
    }

    /* Bottlenecks & Recommendations */
    .alerts-container {
      margin-top: 1.5rem;
    }
    .alert-box {
      border-radius: 10px;
      padding: 1rem 1.2rem;
      margin-bottom: 0.75rem;
      display: flex;
      gap: 12px;
      align-items: flex-start;
      font-size: 0.85rem;
    }
    .alert-box.bottleneck {
      background: rgba(245, 158, 11, 0.08);
      border: 1px solid rgba(245, 158, 11, 0.25);
      color: #fde68a;
    }
    .alert-box.recommendation {
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.25);
      color: #a7f3d0;
    }

    /* Analytics Explorer Section */
    .analytics-section {
      margin-top: 2.5rem;
    }
    .tabs {
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--card-border);
      margin-bottom: 1.25rem;
    }
    .tab-btn {
      background: none;
      border: none;
      color: var(--text-muted);
      font-family: var(--font);
      font-size: 0.88rem;
      font-weight: 600;
      padding: 0.65rem 1.2rem;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.2s;
    }
    .tab-btn:hover {
      color: white;
    }
    .tab-btn.active {
      color: var(--primary);
      border-bottom-color: var(--primary);
    }
    .tab-content {
      display: none;
    }
    .tab-content.active {
      display: block;
    }

    /* Tables */
    .table-wrap {
      overflow-x: auto;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.85rem;
      text-align: left;
    }
    th {
      background: #1e293b;
      color: #cbd5e1;
      padding: 0.75rem 1rem;
      font-weight: 600;
      border-bottom: 1px solid #334155;
    }
    td {
      padding: 0.75rem 1rem;
      border-bottom: 1px solid #1e293b;
      color: #e2e8f0;
    }
    tr:hover td {
      background: rgba(255, 255, 255, 0.02);
    }
    .bar-wrap {
      background: #334155;
      height: 6px;
      border-radius: 3px;
      width: 80px;
      display: inline-block;
      margin-right: 8px;
      overflow: hidden;
      vertical-align: middle;
    }
    .bar-fill {
      height: 100%;
      background: var(--accent-rose);
      border-radius: 3px;
    }

    /* Loader */
    .loading-overlay {
      display: none;
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(11, 15, 25, 0.75);
      backdrop-filter: blur(4px);
      z-index: 20;
      border-radius: var(--radius);
      align-items: center;
      justify-content: center;
      font-weight: 700;
      font-size: 1rem;
      gap: 10px;
    }
  </style>
</head>
<body>

  <header>
    <div class="brand">
      <div class="logo-badge">⚡</div>
      <div class="brand-title">
        <h1>FlashFleet Simulator</h1>
        <p>E-Commerce Fulfillment & Surge Capacity Planning</p>
      </div>
    </div>
    <div class="header-actions">
      <div class="status-pill">
        <span class="status-dot"></span>
        <span>SQLite Database Connected</span>
      </div>
      <a href="/docs" target="_blank" class="docs-btn">Swagger API Docs ↗</a>
    </div>
  </header>

  <div class="container">

    <div class="grid-main">
      <!-- LEFT: Control Panel -->
      <div class="card" style="position: relative;">
        <h2 class="card-title">🎛 Surge Parameters</h2>
        <p class="card-subtitle">Configure top-down parameters for flash-sale demand.</p>

        <div class="presets">
          <button class="preset-btn active" onclick="setPreset(3.0, 3, 'SP')">Weekend 3x</button>
          <button class="preset-btn" onclick="setPreset(5.0, 5, 'SP')">Mega Flash 5x</button>
          <button class="preset-btn" onclick="setPreset(2.0, 2, 'RJ')">Mini Surge 2x</button>
          <button class="preset-btn" onclick="setPreset(8.0, 7, null)">Black Friday 8x</button>
        </div>

        <form id="surgeForm" onsubmit="handleSimulate(event)">
          <div class="form-group">
            <label>
              <span>Demand Surge Multiplier</span>
              <span id="lbl_multiplier" class="val">3.0x (+300%)</span>
            </label>
            <input type="range" id="param_multiplier" class="input-range" min="1.0" max="10.0" step="0.5" value="3.0" oninput="updateMultiplier(this.value)">
          </div>

          <div class="form-group">
            <label>Target Delivery Region (State)</label>
            <select id="param_region" class="input-select" onchange="runSim()">
              <option value="">All Regions (Nationwide)</option>
              <option value="SP" selected>SP — São Paulo</option>
              <option value="RJ">RJ — Rio de Janeiro</option>
              <option value="MG">MG — Minas Gerais</option>
              <option value="RS">RS — Rio Grande do Sul</option>
              <option value="PR">PR — Paraná</option>
              <option value="SC">SC — Santa Catarina</option>
              <option value="BA">BA — Bahia</option>
            </select>
          </div>

          <div class="form-group">
            <label>
              <span>Flash Sale Duration</span>
              <span id="lbl_duration" class="val">3 Days</span>
            </label>
            <input type="range" id="param_duration" class="input-range" min="1" max="14" step="1" value="3" oninput="updateDuration(this.value)">
          </div>

          <div class="form-group">
            <label>Rider Delivery Capacity (pkgs/rider/day)</label>
            <input type="number" id="param_capacity" class="input-text" min="5" max="200" value="40">
          </div>

          <div class="form-group">
            <label>Temporary Rider Wage (R$ / day)</label>
            <input type="number" id="param_wage" class="input-text" min="50" max="1000" value="150.0">
          </div>

          <div class="form-group">
            <label>Warehouse Spot Lease (R$ / m³ / day)</label>
            <input type="number" id="param_warehouse" class="input-text" min="1" max="100" value="5.0">
          </div>

          <div class="form-group">
            <label>Staging Buffer Factor (Footprint Safety Multiplier)</label>
            <input type="number" id="param_buffer" class="input-text" min="1.0" max="3.0" step="0.1" value="1.3">
          </div>

          <button type="submit" class="btn-run">
            <span>🚀 Run Surge Simulation</span>
          </button>
        </form>
      </div>

      <!-- RIGHT: Simulation Results -->
      <div class="card" style="position: relative;">
        <div id="simLoader" class="loading-overlay">
          <span>⚡ Computing baseline analytics & logistics sizing...</span>
        </div>

        <div id="riskBanner" class="risk-banner risk-HIGH">
          <div class="risk-title">
            <span>Operational Risk Assessment:</span>
            <div class="risk-badge"><span id="riskText">HIGH</span></div>
          </div>
          <div style="font-size: 0.8rem; font-family: var(--mono); color: #cbd5e1;" id="simMeta">Simulation: Ready</div>
        </div>

        <!-- 4 KPI Cards -->
        <div class="kpi-grid">
          <div class="kpi-card" style="--kpi-color: #3b82f6;">
            <div class="kpi-label">🛵 Fleet Sizing</div>
            <div class="kpi-value" id="kpi_riders">0</div>
            <div class="kpi-desc" id="kpi_rider_days">0 total rider-days needed</div>
          </div>

          <div class="kpi-card" style="--kpi-color: #8b5cf6;">
            <div class="kpi-label">🏬 Warehouse Staging</div>
            <div class="kpi-value" id="kpi_space">0.0 m²</div>
            <div class="kpi-desc" id="kpi_volume">0.0 m³ package staging volume</div>
          </div>

          <div class="kpi-card" style="--kpi-color: #10b981;">
            <div class="kpi-label">💰 Marginal Cost</div>
            <div class="kpi-value" id="kpi_cost">R$ 0</div>
            <div class="kpi-desc" id="kpi_cost_per_order">R$ 0.00 marginal / order</div>
          </div>

          <div class="kpi-card" style="--kpi-color: #06b6d4;">
            <div class="kpi-label">📦 Projected Orders</div>
            <div class="kpi-value" id="kpi_orders">0</div>
            <div class="kpi-desc" id="kpi_baseline_daily">Baseline: 0 / day</div>
          </div>
        </div>

        <!-- Explanations & Formulas -->
        <div class="breakdown-card">
          <div class="breakdown-header">🛵 Fleet Requirement Logic</div>
          <div class="breakdown-text" id="exp_fleet">Loading fleet explanation...</div>
        </div>

        <div class="breakdown-card">
          <div class="breakdown-header">🏬 Warehouse Space Calculation (2m Stacking Limit)</div>
          <div class="breakdown-text" id="exp_space">Loading space explanation...</div>
        </div>

        <div class="breakdown-card">
          <div class="breakdown-header">💰 Marginal Cost Breakdown</div>
          <div class="breakdown-text" id="exp_cost">Loading cost explanation...</div>
        </div>

        <!-- Bottlenecks & Recommendations -->
        <div class="alerts-container">
          <h3 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.6rem; color: #f1f5f9;">Identified Bottlenecks & Mitigations</h3>
          <div id="bottlenecksList"></div>
          <div id="recommendationsList"></div>
        </div>

      </div>
    </div>

    <!-- BOTTOM: SQL Baseline Analytics Module -->
    <div class="card analytics-section">
      <h2 class="card-title">📊 SQL Baseline Operational Intelligence</h2>
      <p class="card-subtitle">Real metrics extracted via CTEs and Window Functions from the historical Olist dataset.</p>

      <div class="tabs">
        <button class="tab-btn active" onclick="switchTab(0)">Regional SLA Breaches</button>
        <button class="tab-btn" onclick="switchTab(1)">Freight Transit Percentiles (P90)</button>
        <button class="tab-btn" onclick="switchTab(2)">Weekly Volume Density</button>
      </div>

      <!-- Tab 1: SLA Breaches -->
      <div id="tab0" class="tab-content active">
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Region (State)</th>
                <th>Total Deliveries</th>
                <th>Breached Deliveries</th>
                <th>SLA Breach Rate</th>
                <th>Avg Delay (Days)</th>
              </tr>
            </thead>
            <tbody id="table_sla_body">
              <tr><td colspan="5" style="text-align: center;">Loading regional SLA data...</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tab 2: Freight Transit Percentiles -->
      <div id="tab1" class="tab-content">
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Freight Category</th>
                <th>Sample Size</th>
                <th>Min Transit</th>
                <th>Avg Transit</th>
                <th>Median (P50)</th>
                <th>90th Percentile (P90)</th>
                <th>Max Transit</th>
              </tr>
            </thead>
            <tbody id="table_transit_body">
              <tr><td colspan="7" style="text-align: center;">Loading transit percentiles...</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tab 3: Weekly Order Volume Density -->
      <div id="tab2" class="tab-content">
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>Year-Week</th>
                <th>Order Volume</th>
                <th>4-Week Rolling Average (Window Function)</th>
                <th>Overall Average</th>
              </tr>
            </thead>
            <tbody id="table_weekly_body">
              <tr><td colspan="4" style="text-align: center;">Loading weekly order volume...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

  </div>

  <script>
    function updateMultiplier(val) {
      document.getElementById('lbl_multiplier').innerText = parseFloat(val).toFixed(1) + 'x (+' + ((val - 1) * 100).toFixed(0) + '%)';
    }
    function updateDuration(val) {
      document.getElementById('lbl_duration').innerText = val + (val == 1 ? ' Day' : ' Days');
    }

    function setPreset(mult, days, region) {
      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');
      document.getElementById('param_multiplier').value = mult;
      updateMultiplier(mult);
      document.getElementById('param_duration').value = days;
      updateDuration(days);
      if (region !== null) {
        document.getElementById('param_region').value = region;
      } else {
        document.getElementById('param_region').value = '';
      }
      runSim();
    }

    function switchTab(index) {
      document.querySelectorAll('.tab-btn').forEach((b, i) => {
        b.classList.toggle('active', i === index);
      });
      document.querySelectorAll('.tab-content').forEach((c, i) => {
        c.classList.toggle('active', i === index);
      });
    }

    async function handleSimulate(e) {
      if (e) e.preventDefault();
      runSim();
    }

    async function runSim() {
      const loader = document.getElementById('simLoader');
      loader.style.display = 'flex';

      const payload = {
        surge_multiplier: parseFloat(document.getElementById('param_multiplier').value),
        target_region: document.getElementById('param_region').value || null,
        surge_duration_days: parseInt(document.getElementById('param_duration').value, 10),
        rider_capacity_per_day: parseInt(document.getElementById('param_capacity').value, 10),
        rider_daily_wage_brl: parseFloat(document.getElementById('param_wage').value),
        warehouse_cost_per_m3_day_brl: parseFloat(document.getElementById('param_warehouse').value),
        staging_buffer_factor: parseFloat(document.getElementById('param_buffer').value)
      };

      try {
        const res = await fetch('/simulate-surge', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload)
        });
        if (!res.ok) throw new Error('Simulation failed: ' + res.statusText);
        const data = await res.json();
        renderSimulationResults(data);
      } catch (err) {
        alert('Simulation error: ' + err.message);
      } finally {
        loader.style.display = 'none';
      }
    }

    function renderSimulationResults(data) {
      // Risk Banner
      const risk = data.bottleneck_analysis.risk_level;
      const banner = document.getElementById('riskBanner');
      banner.className = 'risk-banner risk-' + risk;
      document.getElementById('riskText').innerText = risk;
      document.getElementById('simMeta').innerText = 'Sim ID: ' + data.simulation_id.substring(0, 8) + '... | Region: ' + (data.params.target_region || 'ALL');

      // KPIs
      document.getElementById('kpi_riders').innerText = data.fleet.riders_needed_per_day.toLocaleString();
      document.getElementById('kpi_rider_days').innerText = data.fleet.total_rider_days.toLocaleString() + ' total rider-days';
      document.getElementById('kpi_space').innerText = data.space.staging_area_sqm_at_2m_height.toFixed(1) + ' m²';
      document.getElementById('kpi_volume').innerText = data.space.staging_area_m3.toFixed(2) + ' m³ staging volume';
      document.getElementById('kpi_cost').innerText = 'R$ ' + data.cost.total_marginal_cost_brl.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      document.getElementById('kpi_cost_per_order').innerText = 'R$ ' + data.cost.cost_per_order_brl.toFixed(2) + ' marginal / order';
      document.getElementById('kpi_orders').innerText = data.fleet.total_surge_orders.toLocaleString();
      document.getElementById('kpi_baseline_daily').innerText = 'Baseline: ' + data.fleet.baseline_daily_orders.toFixed(1) + ' / day';

      // Explanations
      document.getElementById('exp_fleet').innerText = data.fleet.explanation;
      document.getElementById('exp_space').innerText = data.space.explanation;
      document.getElementById('exp_cost').innerText = data.cost.explanation;

      // Bottlenecks & Recommendations
      const bList = document.getElementById('bottlenecksList');
      bList.innerHTML = '';
      if (data.bottleneck_analysis.bottlenecks && data.bottleneck_analysis.bottlenecks.length > 0) {
        data.bottleneck_analysis.bottlenecks.forEach(b => {
          bList.innerHTML += `<div class="alert-box bottleneck"><span>⚠</span><div><strong>Bottleneck Identified:</strong> ${b}</div></div>`;
        });
      }

      const rList = document.getElementById('recommendationsList');
      rList.innerHTML = '';
      if (data.bottleneck_analysis.recommendations && data.bottleneck_analysis.recommendations.length > 0) {
        data.bottleneck_analysis.recommendations.forEach(r => {
          rList.innerHTML += `<div class="alert-box recommendation"><span>✔</span><div><strong>Recommended Action:</strong> ${r}</div></div>`;
        });
      }
    }

    // Load SQL Analytics Data on Page Load
    async function loadAnalyticsData() {
      // SLA Breaches
      try {
        const res = await fetch('/analytics/sla-breaches');
        const list = await res.json();
        const tbody = document.getElementById('table_sla_body');
        tbody.innerHTML = '';
        list.slice(0, 12).forEach(row => {
          tbody.innerHTML += `
            <tr>
              <td><strong>${row.region}</strong></td>
              <td>${row.total_deliveries.toLocaleString()}</td>
              <td>${row.breached_orders.toLocaleString()}</td>
              <td>
                <span class="bar-wrap"><span class="bar-fill" style="width: ${Math.min(100, row.breach_rate_pct)}%"></span></span>
                <strong>${row.breach_rate_pct}%</strong>
              </td>
              <td>${row.avg_breach_days !== null ? row.avg_breach_days + ' days' : 'N/A'}</td>
            </tr>
          `;
        });
      } catch (e) { console.error('SLA fetch error', e); }

      // Transit Percentiles
      try {
        const res = await fetch('/analytics/transit-percentiles');
        const list = await res.json();
        const tbody = document.getElementById('table_transit_body');
        tbody.innerHTML = '';
        list.forEach(row => {
          tbody.innerHTML += `
            <tr>
              <td><strong>${row.weight_class === 'heavy_freight' ? 'Heavy Freight (≥ 5kg)' : 'Lightweight Parcels (< 5kg)'}</strong></td>
              <td>${row.sample_size.toLocaleString()}</td>
              <td>${row.min_transit_days}d</td>
              <td>${row.avg_transit_days}d</td>
              <td><strong>${row.median_transit_days}d</strong></td>
              <td><strong style="color: var(--accent-rose);">${row.p90_transit_days}d (P90)</strong></td>
              <td>${row.max_transit_days}d</td>
            </tr>
          `;
        });
      } catch (e) { console.error('Transit fetch error', e); }

      // Weekly Volume
      try {
        const res = await fetch('/analytics/weekly-volume');
        const list = await res.json();
        const tbody = document.getElementById('table_weekly_body');
        tbody.innerHTML = '';
        list.slice(-15).reverse().forEach(row => {
          tbody.innerHTML += `
            <tr>
              <td><code>${row.year_week}</code></td>
              <td><strong>${row.order_count.toLocaleString()} orders</strong></td>
              <td>${row.rolling_4wk_avg} / week</td>
              <td>${row.overall_avg} / week</td>
            </tr>
          `;
        });
      } catch (e) { console.error('Weekly fetch error', e); }
    }

    // Init
    window.addEventListener('DOMContentLoaded', () => {
      runSim();
      loadAnalyticsData();
    });
  </script>
</body>
</html>
"""


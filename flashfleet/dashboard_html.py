"""HTML template for the FlashFleet interactive web dashboard.

Built following tasteskill 2.5 (anti-slop frontend design system for software/tech):
- Kind: software (data-type="software", site-kind="software")
- Palette: blue-black-cornflower (#0a0d14, #131824, #e9edf3, #5ab9fc)
- Type: Urbanist + DM Mono
- Equal edges, semantic <main> and <section> tags, quiet micro-interactions
"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en" data-type="software" data-radius="soft">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="page-type" content="software">
  <meta name="site-kind" content="software">
  <title>FlashFleet — E-Commerce Fulfillment & Surge Capacity Simulator</title>
  
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
  
  <style>
    :root {
      --p-bg: #0a0d14;
      --p-surface: #131824;
      --p-surface-2: #1b2335;
      --p-border: #222d42;
      --p-border-hover: #334360;
      --p-ink: #e9edf3;
      --p-muted: #8891a1;
      --p-accent: #5ab9fc;
      --p-accent-ink: #0a0d14;
      --p-action: #5ab9fc;
      --p-action-hover: #38a5f8;
      
      --emerald: #10b981;
      --amber: #f59e0b;
      --rose: #f43f5e;
      --cyan: #06b6d4;

      --font-display: "Urbanist", system-ui, sans-serif;
      --font-text: "Urbanist", system-ui, sans-serif;
      --font-mono: "DM Mono", ui-monospace, Menlo, Consolas, monospace;
      
      --display-weight: 600;
      --display-tracking: -0.03em;
      --radius: 12px;
      --radius-sm: 8px;
      --container: 1320px;
      --gut: 24px;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    body {
      background-color: var(--p-bg);
      color: var(--p-ink);
      font-family: var(--font-text);
      min-height: 100vh;
      line-height: 1.55;
      -webkit-font-smoothing: antialiased;
    }

    /* Header */
    header.site-nav {
      background: rgba(10, 13, 20, 0.85);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--p-border);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 1rem 0;
    }
    .nav-wrap {
      max-width: var(--container);
      margin: 0 auto;
      padding: 0 var(--gut);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .brand-group {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .brand-symbol {
      width: 38px;
      height: 38px;
      border-radius: var(--radius-sm);
      background: linear-gradient(135deg, #2563eb 0%, #5ab9fc 100%);
      color: #0a0d14;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.25rem;
      box-shadow: 0 4px 16px rgba(90, 185, 252, 0.25);
    }
    .brand-meta h1 {
      font-family: var(--font-display);
      font-size: 1.25rem;
      font-weight: 700;
      letter-spacing: var(--display-tracking);
      color: #ffffff;
      line-height: 1.2;
    }
    .brand-meta p {
      font-size: 0.78rem;
      color: var(--p-muted);
    }

    .nav-actions {
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .live-badge {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 5px 12px;
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.25);
      border-radius: 9999px;
      font-size: 0.75rem;
      font-weight: 600;
      color: #34d399;
    }
    .pulse-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
      animation: pulseAnim 2s infinite;
    }
    @keyframes pulseAnim {
      0%, 100% { opacity: 1; transform: scale(1); }
      50% { opacity: 0.4; transform: scale(0.85); }
    }
    .btn-docs {
      color: var(--p-muted);
      text-decoration: none;
      font-size: 0.8rem;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--p-border);
      background: var(--p-surface);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .btn-docs:hover {
      color: #ffffff;
      border-color: var(--p-action);
      transform: translateY(-1px);
    }

    /* Main Container */
    main.wrap {
      max-width: var(--container);
      margin: 0 auto;
      padding: 2.5rem var(--gut) 4rem var(--gut);
    }

    /* Section Rhythm */
    section {
      margin-bottom: 3.5rem;
    }
    .section-head {
      margin-bottom: 1.5rem;
    }
    .section-head h2 {
      font-family: var(--font-display);
      font-size: 1.5rem;
      font-weight: 700;
      letter-spacing: var(--display-tracking);
      color: #ffffff;
      margin-bottom: 0.25rem;
    }
    .section-head p {
      font-size: 0.88rem;
      color: var(--p-muted);
    }

    /* Layout Grid */
    .sim-grid {
      display: grid;
      grid-template-columns: 380px 1fr;
      gap: 1.75rem;
      align-items: start;
    }
    @media (max-width: 1024px) {
      .sim-grid { grid-template-columns: 1fr; }
    }

    /* Panels */
    .panel {
      background: var(--p-surface);
      border: 1px solid var(--p-border);
      border-radius: var(--radius);
      padding: 1.6rem;
      box-shadow: 0 12px 32px rgba(0, 0, 0, 0.25);
    }

    /* Presets */
    .preset-bar {
      display: flex;
      gap: 6px;
      margin-bottom: 1.4rem;
      flex-wrap: wrap;
    }
    .btn-preset {
      background: var(--p-surface-2);
      border: 1px solid var(--p-border);
      color: var(--p-muted);
      padding: 5px 11px;
      border-radius: var(--radius-sm);
      font-size: 0.76rem;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .btn-preset:hover {
      background: var(--p-border);
      color: #ffffff;
    }
    .btn-preset.active {
      background: rgba(90, 185, 252, 0.15);
      border-color: var(--p-action);
      color: var(--p-action);
    }

    /* Form Fields */
    .field {
      margin-bottom: 1.25rem;
    }
    .field label {
      display: flex;
      justify-content: space-between;
      font-size: 0.82rem;
      font-weight: 600;
      color: #cbd5e1;
      margin-bottom: 0.4rem;
    }
    .field label span.num {
      color: var(--p-accent);
      font-family: var(--font-mono);
      font-weight: 700;
    }
    .slider {
      width: 100%;
      height: 6px;
      border-radius: 4px;
      background: #1e293b;
      outline: none;
      -webkit-appearance: none;
    }
    .slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 18px;
      height: 18px;
      border-radius: 50%;
      background: var(--p-action);
      cursor: pointer;
      box-shadow: 0 0 10px rgba(90, 185, 252, 0.6);
      transition: transform 0.15s;
    }
    .slider::-webkit-slider-thumb:hover {
      transform: scale(1.15);
    }
    .select-box, .text-box {
      width: 100%;
      padding: 0.7rem 0.85rem;
      background: var(--p-surface-2);
      border: 1px solid var(--p-border);
      border-radius: var(--radius-sm);
      color: #ffffff;
      font-family: var(--font-text);
      font-size: 0.88rem;
      outline: none;
      transition: border 0.2s;
    }
    .select-box:focus, .text-box:focus {
      border-color: var(--p-action);
    }

    .btn-submit {
      width: 100%;
      padding: 0.9rem;
      background: var(--p-action);
      color: var(--p-action-ink);
      border: none;
      border-radius: var(--radius-sm);
      font-family: var(--font-display);
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      gap: 8px;
      box-shadow: 0 4px 20px rgba(90, 185, 252, 0.35);
      transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
    }
    .btn-submit:hover {
      background: var(--p-action-hover);
      transform: translateY(-2px);
      box-shadow: 0 6px 26px rgba(90, 185, 252, 0.45);
    }
    .btn-submit:active {
      transform: translateY(0);
    }

    /* Simulation Output Header / Risk Banner */
    .risk-banner {
      border-radius: var(--radius-sm);
      padding: 1.15rem 1.4rem;
      margin-bottom: 1.5rem;
      display: flex;
      align-items: center;
      justify-content: space-between;
      border: 1px solid transparent;
      transition: all 0.3s ease;
    }
    .risk-CRITICAL {
      background: rgba(244, 63, 94, 0.1);
      border-color: rgba(244, 63, 94, 0.35);
      color: #fb7185;
    }
    .risk-HIGH {
      background: rgba(245, 158, 11, 0.1);
      border-color: rgba(245, 158, 11, 0.35);
      color: #fbbf24;
    }
    .risk-MEDIUM {
      background: rgba(90, 185, 252, 0.1);
      border-color: rgba(90, 185, 252, 0.35);
      color: #7dd3fc;
    }
    .risk-LOW {
      background: rgba(16, 185, 129, 0.1);
      border-color: rgba(16, 185, 129, 0.35);
      color: #34d399;
    }
    .risk-heading {
      font-size: 1.05rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .risk-tag {
      padding: 3px 10px;
      border-radius: 9999px;
      font-size: 0.74rem;
      font-weight: 800;
      letter-spacing: 0.05em;
      text-transform: uppercase;
      background: currentColor;
    }
    .risk-tag span {
      color: #0a0d14;
    }

    /* KPI Grid */
    .kpi-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
      gap: 1rem;
      margin-bottom: 1.5rem;
    }
    .kpi-tile {
      background: var(--p-surface-2);
      border: 1px solid var(--p-border);
      border-radius: var(--radius-sm);
      padding: 1.15rem;
      position: relative;
      overflow: hidden;
      transition: border-color 0.2s, transform 0.2s;
    }
    .kpi-tile:hover {
      border-color: var(--p-border-hover);
      transform: translateY(-2px);
    }
    .kpi-tile::before {
      content: "";
      position: absolute;
      top: 0; left: 0;
      width: 4px; height: 100%;
      background: var(--tile-bar, var(--p-action));
    }
    .kpi-title {
      font-size: 0.74rem;
      font-weight: 600;
      color: var(--p-muted);
      text-transform: uppercase;
      letter-spacing: 0.04em;
      margin-bottom: 0.3rem;
    }
    .kpi-stat {
      font-family: var(--font-display);
      font-size: 1.75rem;
      font-weight: 700;
      letter-spacing: var(--display-tracking);
      color: #ffffff;
      margin-bottom: 0.2rem;
    }
    .kpi-sub {
      font-size: 0.78rem;
      color: #94a3b8;
    }

    /* Actionable SLA Impact Tile */
    .sla-impact-card {
      background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(6, 182, 212, 0.04) 100%);
      border: 1px solid rgba(16, 185, 129, 0.25);
      border-radius: var(--radius-sm);
      padding: 1.25rem;
      margin-bottom: 1.5rem;
    }
    .sla-impact-top {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 0.6rem;
      flex-wrap: wrap;
      gap: 8px;
    }
    .sla-impact-title {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.95rem;
      font-weight: 700;
      color: #34d399;
    }
    .sla-impact-badge {
      background: rgba(16, 185, 129, 0.2);
      color: #34d399;
      font-weight: 800;
      font-size: 0.78rem;
      padding: 3px 12px;
      border-radius: 9999px;
      border: 1px solid rgba(16, 185, 129, 0.4);
    }
    .sla-stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 10px;
      margin-top: 0.75rem;
      text-align: center;
    }
    .sla-stat-box {
      background: rgba(0, 0, 0, 0.3);
      padding: 0.65rem;
      border-radius: var(--radius-sm);
      border: 1px solid var(--p-border);
    }
    .sla-stat-label {
      font-size: 0.68rem;
      color: var(--p-muted);
      text-transform: uppercase;
      font-weight: 600;
    }
    .sla-stat-val {
      font-size: 1.25rem;
      font-weight: 800;
      margin-top: 2px;
    }
    .sla-explanation {
      font-size: 0.82rem;
      color: #cbd5e1;
      margin-top: 0.85rem;
      line-height: 1.55;
    }

    /* Explanation Boxes */
    .note-box {
      background: var(--p-surface-2);
      border: 1px solid var(--p-border);
      border-radius: var(--radius-sm);
      padding: 1.15rem;
      margin-bottom: 1rem;
    }
    .note-title {
      font-size: 0.88rem;
      font-weight: 700;
      margin-bottom: 0.4rem;
      color: #f1f5f9;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .note-body {
      font-size: 0.84rem;
      color: #cbd5e1;
      line-height: 1.6;
    }

    /* Bottleneck & Recommendations */
    .callout {
      border-radius: var(--radius-sm);
      padding: 0.9rem 1.15rem;
      margin-bottom: 0.65rem;
      display: flex;
      gap: 12px;
      align-items: flex-start;
      font-size: 0.84rem;
    }
    .callout.warn {
      background: rgba(245, 158, 11, 0.08);
      border: 1px solid rgba(245, 158, 11, 0.25);
      color: #fde68a;
    }
    .callout.rec {
      background: rgba(16, 185, 129, 0.08);
      border: 1px solid rgba(16, 185, 129, 0.25);
      color: #a7f3d0;
    }

    /* Tabs & Tables */
    .tab-bar {
      display: flex;
      gap: 8px;
      border-bottom: 1px solid var(--p-border);
      margin-bottom: 1.25rem;
    }
    .tab-item {
      background: none;
      border: none;
      color: var(--p-muted);
      font-family: var(--font-text);
      font-size: 0.88rem;
      font-weight: 600;
      padding: 0.65rem 1.2rem;
      cursor: pointer;
      border-bottom: 2px solid transparent;
      transition: all 0.2s;
    }
    .tab-item:hover { color: #ffffff; }
    .tab-item.active {
      color: var(--p-action);
      border-bottom-color: var(--p-action);
    }
    .tab-pane { display: none; }
    .tab-pane.active { display: block; }

    .table-container {
      overflow-x: auto;
      border: 1px solid var(--p-border);
      border-radius: var(--radius-sm);
    }
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 0.84rem;
      text-align: left;
    }
    th {
      background: var(--p-surface-2);
      color: #cbd5e1;
      padding: 0.75rem 1rem;
      font-weight: 600;
      border-bottom: 1px solid var(--p-border);
    }
    td {
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--p-surface-2);
      color: #e2e8f0;
    }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: rgba(255, 255, 255, 0.02); }

    .pct-bar-bg {
      background: #1e293b;
      height: 6px;
      border-radius: 3px;
      width: 70px;
      display: inline-block;
      margin-right: 8px;
      overflow: hidden;
      vertical-align: middle;
    }
    .pct-bar-fill {
      height: 100%;
      background: var(--rose);
      border-radius: 3px;
    }

    footer.site-footer {
      border-top: 1px solid var(--p-border);
      padding: 2rem var(--gut);
      text-align: center;
      font-size: 0.8rem;
      color: var(--p-muted);
    }
    footer.site-footer a {
      color: var(--p-accent);
      text-decoration: none;
    }

    /* Loading Overlay */
    .busy-overlay {
      display: none;
      position: absolute;
      top: 0; left: 0; right: 0; bottom: 0;
      background: rgba(10, 13, 20, 0.75);
      backdrop-filter: blur(4px);
      z-index: 20;
      border-radius: var(--radius);
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 0.95rem;
      gap: 10px;
    }
  </style>
</head>
<body>

  <!-- Navigation -->
  <header class="site-nav">
    <div class="nav-wrap">
      <div class="brand-group">
        <div class="brand-symbol">⚡</div>
        <div class="brand-meta">
          <h1>FlashFleet</h1>
          <p>E-Commerce Fulfillment & Surge Capacity Simulator</p>
        </div>
      </div>
      <div class="nav-actions">
        <div class="live-badge">
          <span class="pulse-dot"></span>
          <span>100k+ Records Indexed</span>
        </div>
        <a href="/docs" target="_blank" class="btn-docs">API Docs ↗</a>
      </div>
    </div>
  </header>

  <!-- Main Content -->
  <main class="wrap">

    <!-- Section 1: Surge Simulator -->
    <section id="simulator">
      <div class="sim-grid">
        
        <!-- Controls Column -->
        <div class="panel" style="position: relative;">
          <div class="section-head" style="margin-bottom: 1.1rem;">
            <h2>🎛 Surge Parameters</h2>
            <p>Model dynamic flash-sale volume increases.</p>
          </div>

          <div class="preset-bar">
            <button class="btn-preset active" onclick="setPreset(3.0, 3, 'SP')">Weekend 3x</button>
            <button class="btn-preset" onclick="setPreset(5.0, 5, 'SP')">Mega 5x</button>
            <button class="btn-preset" onclick="setPreset(2.0, 2, 'RJ')">Mini 2x</button>
            <button class="btn-preset" onclick="setPreset(8.0, 7, null)">Black Friday 8x</button>
          </div>

          <form id="simForm" onsubmit="handleFormSubmit(event)">
            <div class="field">
              <label>
                <span>Demand Surge Multiplier</span>
                <span id="lbl_multiplier" class="num">3.0x (+300%)</span>
              </label>
              <input type="range" id="param_multiplier" class="slider" min="1.0" max="10.0" step="0.5" value="3.0" oninput="onMultiplierChange(this.value)">
            </div>

            <div class="field">
              <label>Target Region (State)</label>
              <select id="param_region" class="select-box" onchange="triggerSim()">
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

            <div class="field">
              <label>
                <span>Sale Duration</span>
                <span id="lbl_duration" class="num">3 Days</span>
              </label>
              <input type="range" id="param_duration" class="slider" min="1" max="14" step="1" value="3" oninput="onDurationChange(this.value)">
            </div>

            <div class="field">
              <label>Rider Throughput (pkgs/rider/day)</label>
              <input type="number" id="param_capacity" class="text-box" min="5" max="200" value="40">
            </div>

            <div class="field">
              <label>Rider Daily Wage (R$ / day)</label>
              <input type="number" id="param_wage" class="text-box" min="50" max="1000" value="150.0">
            </div>

            <div class="field">
              <label>Warehouse Spot Lease (R$ / m³ / day)</label>
              <input type="number" id="param_warehouse" class="text-box" min="1" max="100" value="5.0">
            </div>

            <div class="field">
              <label>Staging Area Buffer (Safety Multiplier)</label>
              <input type="number" id="param_buffer" class="text-box" min="1.0" max="3.0" step="0.1" value="1.3">
            </div>

            <button type="submit" class="btn-submit">
              <span>🚀 Run Surge Simulation</span>
            </button>
          </form>
        </div>

        <!-- Results Column -->
        <div class="panel" style="position: relative;">
          <div id="busyIndicator" class="busy-overlay">
            <span>⚡ Calculating fleet requirements & SQL baseline metrics...</span>
          </div>

          <!-- Risk Assessment Banner -->
          <div id="riskBanner" class="risk-banner risk-HIGH">
            <div class="risk-heading">
              <span>Operational Risk:</span>
              <div class="risk-tag"><span id="riskBadgeText">HIGH</span></div>
            </div>
            <div style="font-size: 0.78rem; font-family: var(--font-mono); color: #cbd5e1;" id="simMeta">Sim ID: Ready</div>
          </div>

          <!-- 4 KPI Metric Cards -->
          <div class="kpi-row">
            <div class="kpi-tile" style="--tile-bar: #38bdf8;">
              <div class="kpi-title">🛵 Fleet Sizing</div>
              <div class="kpi-stat" id="kpi_riders">0</div>
              <div class="kpi-sub" id="kpi_rider_days">0 total rider-days</div>
            </div>

            <div class="kpi-tile" style="--tile-bar: #a855f7;">
              <div class="kpi-title">🏬 Warehouse Footprint</div>
              <div class="kpi-stat" id="kpi_space">0.0 m²</div>
              <div class="kpi-sub" id="kpi_volume">0.0 m³ package staging</div>
            </div>

            <div class="kpi-tile" style="--tile-bar: #10b981;">
              <div class="kpi-title">💰 Marginal Cost</div>
              <div class="kpi-stat" id="kpi_cost">R$ 0</div>
              <div class="kpi-sub" id="kpi_cost_per_order">R$ 0.00 / order</div>
            </div>

            <div class="kpi-tile" style="--tile-bar: #06b6d4;">
              <div class="kpi-title">📦 Surge Volume</div>
              <div class="kpi-stat" id="kpi_orders">0</div>
              <div class="kpi-sub" id="kpi_baseline_daily">Baseline: 0 / day</div>
            </div>
          </div>

          <!-- Actionable SLA Optimization Impact -->
          <div class="sla-impact-card">
            <div class="sla-impact-top">
              <div class="sla-impact-title">
                <span>🎯</span>
                <strong>Actionable SLA Optimization Impact</strong>
              </div>
              <span class="sla-impact-badge">-25.0% SLA Breaches</span>
            </div>
            <div class="sla-stats-grid">
              <div class="sla-stat-box">
                <div class="sla-stat-label">Unmitigated Surge Breach</div>
                <div id="sla_unmitigated" class="sla-stat-val" style="color: #fb7185;">0.0%</div>
              </div>
              <div class="sla-stat-box">
                <div class="sla-stat-label">Optimized Breach Rate</div>
                <div id="sla_optimized" class="sla-stat-val" style="color: #34d399;">0.0%</div>
              </div>
              <div class="sla-stat-box">
                <div class="sla-stat-label">Protected Deliveries</div>
                <div id="sla_prevented" class="sla-stat-val" style="color: #38bdf8;">0</div>
              </div>
            </div>
            <p id="sla_explanation" class="sla-explanation"></p>
          </div>

          <!-- Formulas & Logic Breakdown -->
          <div class="note-box">
            <div class="note-title">🛵 Fleet Sizing Logic</div>
            <div class="note-body" id="exp_fleet">Computing fleet allocation...</div>
          </div>

          <div class="note-box">
            <div class="note-title">🏬 Warehouse Footprint Calculation (2m Stacking Height)</div>
            <div class="note-body" id="exp_space">Computing storage footprint...</div>
          </div>

          <div class="note-box">
            <div class="note-title">💰 Marginal Operational Cost Projection</div>
            <div class="note-body" id="exp_cost">Computing marginal expenditure...</div>
          </div>

          <!-- Bottlenecks & Recommendations -->
          <div style="margin-top: 1.4rem;">
            <h3 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.6rem; color: #f1f5f9;">Identified Bottlenecks & Strategic Mitigations</h3>
            <div id="bottlenecksList"></div>
            <div id="recommendationsList"></div>
          </div>

        </div>
      </div>
    </section>

    <!-- Section 2: SQL Baseline Analytics -->
    <section id="analytics" class="panel">
      <div class="section-head">
        <h2>📊 SQL Baseline Operational Intelligence</h2>
        <p>Real historical benchmarks extracted from the Olist delivery dataset via CTEs and Window Functions.</p>
      </div>

      <div class="tab-bar">
        <button class="tab-item active" onclick="activateTab(0)">Regional SLA Breaches</button>
        <button class="tab-item" onclick="activateTab(1)">Freight Transit Percentiles (P90)</button>
        <button class="tab-item" onclick="activateTab(2)">Weekly Volume Density</button>
      </div>

      <!-- Tab 1: SLA Breaches -->
      <div id="tabPane0" class="tab-pane active">
        <div class="table-container">
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
            <tbody id="slaTableBody">
              <tr><td colspan="5" style="text-align: center; color: var(--p-muted);">Querying delivery SLA data...</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tab 2: Freight Transit Percentiles -->
      <div id="tabPane1" class="tab-pane">
        <div class="table-container">
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
            <tbody id="transitTableBody">
              <tr><td colspan="7" style="text-align: center; color: var(--p-muted);">Computing transit percentiles...</td></tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- Tab 3: Weekly Order Volume Density -->
      <div id="tabPane2" class="tab-pane">
        <div class="table-container">
          <table>
            <thead>
              <tr>
                <th>Year-Week</th>
                <th>Order Volume</th>
                <th>4-Week Rolling Average (Window Function)</th>
                <th>Overall Average</th>
              </tr>
            </thead>
            <tbody id="weeklyTableBody">
              <tr><td colspan="4" style="text-align: center; color: var(--p-muted);">Aggregating order volume density...</td></tr>
            </tbody>
          </table>
        </div>
      </div>
    </section>

  </main>

  <footer class="site-footer">
    <p>FlashFleet E-Commerce Fulfillment Simulator • Historical Brazilian E-Commerce Data (Olist) • Fast, resilient SQLite & FastAPI</p>
  </footer>

  <script>
    function onMultiplierChange(val) {
      document.getElementById('lbl_multiplier').innerText = parseFloat(val).toFixed(1) + 'x (+' + ((val - 1) * 100).toFixed(0) + '%)';
    }
    function onDurationChange(val) {
      document.getElementById('lbl_duration').innerText = val + (val == 1 ? ' Day' : ' Days');
    }

    function setPreset(mult, days, region) {
      document.querySelectorAll('.btn-preset').forEach(b => b.classList.remove('active'));
      event.target.classList.add('active');
      document.getElementById('param_multiplier').value = mult;
      onMultiplierChange(mult);
      document.getElementById('param_duration').value = days;
      onDurationChange(days);
      document.getElementById('param_region').value = (region !== null) ? region : '';
      triggerSim();
    }

    function activateTab(index) {
      document.querySelectorAll('.tab-item').forEach((b, i) => b.classList.toggle('active', i === index));
      document.querySelectorAll('.tab-pane').forEach((c, i) => c.classList.toggle('active', i === index));
    }

    function handleFormSubmit(e) {
      if (e) e.preventDefault();
      triggerSim();
    }

    async function triggerSim() {
      const loader = document.getElementById('busyIndicator');
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
        if (!res.ok) throw new Error('Simulation endpoint failed: ' + res.statusText);
        const data = await res.json();
        renderResults(data);
      } catch (err) {
        console.error('Simulation error:', err);
      } finally {
        loader.style.display = 'none';
      }
    }

    function renderResults(data) {
      // Risk Banner
      const risk = data.bottleneck_analysis.risk_level;
      const banner = document.getElementById('riskBanner');
      banner.className = 'risk-banner risk-' + risk;
      document.getElementById('riskBadgeText').innerText = risk;
      document.getElementById('simMeta').innerText = 'Sim ID: ' + data.simulation_id.substring(0, 8) + '... | ' + (data.params.target_region || 'ALL');

      // KPIs
      document.getElementById('kpi_riders').innerText = data.fleet.riders_needed_per_day.toLocaleString();
      document.getElementById('kpi_rider_days').innerText = data.fleet.total_rider_days.toLocaleString() + ' total rider-days';
      document.getElementById('kpi_space').innerText = data.space.staging_area_sqm_at_2m_height.toFixed(1) + ' m²';
      document.getElementById('kpi_volume').innerText = data.space.staging_area_m3.toFixed(2) + ' m³ staging volume';
      document.getElementById('kpi_cost').innerText = 'R$ ' + data.cost.total_marginal_cost_brl.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      document.getElementById('kpi_cost_per_order').innerText = 'R$ ' + data.cost.cost_per_order_brl.toFixed(2) + ' / order';
      document.getElementById('kpi_orders').innerText = data.fleet.total_surge_orders.toLocaleString();
      document.getElementById('kpi_baseline_daily').innerText = 'Baseline: ' + data.fleet.baseline_daily_orders.toFixed(1) + ' / day';

      // Explanations
      document.getElementById('exp_fleet').innerText = data.fleet.explanation;
      document.getElementById('exp_space').innerText = data.space.explanation;
      document.getElementById('exp_cost').innerText = data.cost.explanation;

      // SLA Impact
      if (data.sla_impact) {
        document.getElementById('sla_unmitigated').innerText = data.sla_impact.unmitigated_surge_breach_rate_pct.toFixed(1) + '%';
        document.getElementById('sla_optimized').innerText = data.sla_impact.optimized_breach_rate_pct.toFixed(1) + '%';
        document.getElementById('sla_prevented').innerText = data.sla_impact.prevented_breaches.toLocaleString() + ' orders';
        document.getElementById('sla_explanation').innerText = data.sla_impact.explanation;
      }

      // Bottlenecks & Recommendations
      const bList = document.getElementById('bottlenecksList');
      bList.innerHTML = '';
      if (data.bottleneck_analysis.bottlenecks && data.bottleneck_analysis.bottlenecks.length > 0) {
        data.bottleneck_analysis.bottlenecks.forEach(b => {
          bList.innerHTML += `<div class="callout warn"><span>⚠</span><div><strong>Bottleneck:</strong> ${b}</div></div>`;
        });
      }

      const rList = document.getElementById('recommendationsList');
      rList.innerHTML = '';
      if (data.bottleneck_analysis.recommendations && data.bottleneck_analysis.recommendations.length > 0) {
        data.bottleneck_analysis.recommendations.forEach(r => {
          rList.innerHTML += `<div class="callout rec"><span>✔</span><div><strong>Recommendation:</strong> ${r}</div></div>`;
        });
      }
    }

    async function loadSqlAnalytics() {
      // 1. SLA Breaches
      try {
        const res = await fetch('/analytics/sla-breaches');
        const list = await res.json();
        const tbody = document.getElementById('slaTableBody');
        tbody.innerHTML = '';
        list.slice(0, 10).forEach(row => {
          tbody.innerHTML += `
            <tr>
              <td><strong>${row.region}</strong></td>
              <td>${row.total_deliveries.toLocaleString()}</td>
              <td>${row.breached_orders.toLocaleString()}</td>
              <td>
                <span class="pct-bar-bg"><span class="pct-bar-fill" style="width: ${Math.min(100, row.breach_rate_pct)}%"></span></span>
                <strong>${row.breach_rate_pct}%</strong>
              </td>
              <td>${row.avg_breach_days !== null ? row.avg_breach_days + 'd' : '—'}</td>
            </tr>
          `;
        });
      } catch (e) { console.error('SLA error', e); }

      // 2. Freight Transit Percentiles
      try {
        const res = await fetch('/analytics/transit-percentiles');
        const list = await res.json();
        const tbody = document.getElementById('transitTableBody');
        tbody.innerHTML = '';
        list.forEach(row => {
          tbody.innerHTML += `
            <tr>
              <td><strong>${row.weight_class === 'heavy_freight' ? 'Heavy Freight (≥ 5kg)' : 'Lightweight Parcels (< 5kg)'}</strong></td>
              <td>${row.sample_size.toLocaleString()}</td>
              <td>${row.min_transit_days}d</td>
              <td>${row.avg_transit_days}d</td>
              <td><strong>${row.median_transit_days}d</strong></td>
              <td><strong style="color: var(--rose);">${row.p90_transit_days}d (P90)</strong></td>
              <td>${row.max_transit_days}d</td>
            </tr>
          `;
        });
      } catch (e) { console.error('Transit error', e); }

      // 3. Weekly Volume
      try {
        const res = await fetch('/analytics/weekly-volume');
        const list = await res.json();
        const tbody = document.getElementById('weeklyTableBody');
        tbody.innerHTML = '';
        list.slice(-12).reverse().forEach(row => {
          tbody.innerHTML += `
            <tr>
              <td><code style="font-family: var(--font-mono); color: var(--p-accent);">${row.year_week}</code></td>
              <td><strong>${row.order_count.toLocaleString()} orders</strong></td>
              <td>${row.rolling_4wk_avg} / wk</td>
              <td>${row.overall_avg} / wk</td>
            </tr>
          `;
        });
      } catch (e) { console.error('Weekly error', e); }
    }

    window.addEventListener('DOMContentLoaded', () => {
      triggerSim();
      loadSqlAnalytics();
    });
  </script>
</body>
</html>
"""

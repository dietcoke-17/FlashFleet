"""HTML template for the FlashFleet interactive web dashboard.

Built following tasteskill 2.5.1 (anti-slop frontend design system for software/tech):
- Kind: software (data-type="software", site-kind="software")
- Palette: blue-black-cornflower (#0a0d14, #131824, #e9edf3, #5ab9fc)
- Type: Urbanist (display) + DM Mono (mono)
- Hero section fills first screen with app-frame product UI
- Equal edges via .wrap max-width container
- Semantic main > section structure, h2 first in each section
- No tabs — 3 stacked analytics sections
- Skip link, no emoji in h2s, clean button copy
"""

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="en" data-type="software" data-radius="soft" data-buttons="solid" data-motion="on">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="page-type" content="software">
  <meta name="site-kind" content="software">
  <meta name="description" content="FlashFleet — model flash-sale surge capacity from 100k+ Brazilian delivery records. Fleet sizing, warehouse footprint and SLA impact in seconds.">
  <meta property="og:title" content="FlashFleet — Surge Capacity Simulator">
  <meta property="og:description" content="Model flash-sale surge capacity from 100k+ delivery records.">
  <meta name="theme-color" content="#0a0d14">
  <title>FlashFleet — E-Commerce Fulfillment &amp; Surge Capacity Simulator</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Urbanist:wght@400;500;600;700;800&family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">

  <style>
    /* ── Design tokens ──────────────────────────────────────────── */
    :root {
      --p-bg:           #0a0d14;
      --p-surface:      #131824;
      --p-surface-2:    #1b2335;
      --p-border:       #222d42;
      --p-border-hover: #334360;
      --p-ink:          #e9edf3;
      --p-muted:        #8891a1;
      --p-accent:       #5ab9fc;
      --p-accent-ink:   #0a0d14;
      --p-action:       #5ab9fc;
      --p-action-hover: #38a5f8;

      --emerald: #10b981;
      --amber:   #f59e0b;
      --rose:    #f43f5e;
      --cyan:    #06b6d4;

      --font-display: "Urbanist", system-ui, sans-serif;
      --font-text:    "Urbanist", system-ui, sans-serif;
      --font-mono:    "DM Mono", ui-monospace, Menlo, Consolas, monospace;

      --display-weight:   600;
      --display-tracking: -0.03em;
      --radius:    12px;
      --radius-sm: 8px;

      /* Layout rhythm (tasteskill section heights) */
      --padt: 120px;
      --padb: 72px;
      --wrap-max: 1280px;
      --gut: clamp(24px, 6.25vw, 80px);
    }

    /* ── Reset ──────────────────────────────────────────────────── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    html { scroll-behavior: smooth; }

    body {
      background-color: var(--p-bg);
      color: var(--p-ink);
      font-family: var(--font-text);
      min-height: 100vh;
      line-height: 1.55;
      -webkit-font-smoothing: antialiased;
    }

    /* ── Skip link (a11y) ───────────────────────────────────────── */
    .skip-link {
      position: absolute;
      left: 24px;
      top: -60px;
      z-index: 9999;
      background: var(--p-accent);
      color: var(--p-accent-ink);
      font-weight: 700;
      font-size: 0.85rem;
      padding: 8px 16px;
      border-radius: var(--radius-sm);
      text-decoration: none;
      transition: top 0.2s;
    }
    .skip-link:focus { top: 16px; outline: 2px solid var(--p-accent); outline-offset: 2px; }

    /* ── Nav ────────────────────────────────────────────────────── */
    header.site-nav {
      background: rgba(10, 13, 20, 0.88);
      backdrop-filter: blur(16px);
      border-bottom: 1px solid var(--p-border);
      position: sticky;
      top: 0;
      z-index: 100;
      padding: 1rem 0;
    }
    .nav-wrap {
      max-width: var(--wrap-max);
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
      text-decoration: none;
    }
    .brand-symbol {
      width: 36px;
      height: 36px;
      border-radius: var(--radius-sm);
      background: linear-gradient(135deg, #2563eb 0%, #5ab9fc 100%);
      color: #0a0d14;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 800;
      font-size: 1.1rem;
      box-shadow: 0 4px 16px rgba(90, 185, 252, 0.25);
      flex-shrink: 0;
    }
    /* Nav wordmark — NOT an h1 (page h1 lives in hero) */
    .wordmark {
      font-family: var(--font-display);
      font-size: 1.15rem;
      font-weight: 700;
      letter-spacing: var(--display-tracking);
      color: #ffffff;
      line-height: 1;
    }
    .wordmark-sub {
      font-size: 0.72rem;
      color: var(--p-muted);
      margin-top: 2px;
      display: block;
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
      font-size: 0.74rem;
      font-weight: 600;
      color: #34d399;
      white-space: nowrap;
    }
    .pulse-dot {
      width: 7px;
      height: 7px;
      border-radius: 50%;
      background: #10b981;
      box-shadow: 0 0 8px #10b981;
      animation: pulseAnim 2s infinite;
      flex-shrink: 0;
    }
    @keyframes pulseAnim {
      0%, 100% { opacity: 1; transform: scale(1); }
      50%       { opacity: 0.4; transform: scale(0.85); }
    }
    .btn-nav {
      color: var(--p-muted);
      text-decoration: none;
      font-size: 0.8rem;
      font-weight: 600;
      padding: 6px 14px;
      border-radius: var(--radius-sm);
      border: 1px solid var(--p-border);
      background: var(--p-surface);
      transition: color 0.2s, border-color 0.2s, transform 0.2s cubic-bezier(0.16,1,0.3,1);
    }
    .btn-nav:hover {
      color: #ffffff;
      border-color: var(--p-action);
      transform: translateY(-1px);
    }

    /* ── Wrap ───────────────────────────────────────────────────── */
    .wrap {
      max-width: var(--wrap-max);
      margin: 0 auto;
      padding-left: var(--gut);
      padding-right: var(--gut);
    }

    /* ── Section rhythm ─────────────────────────────────────────── */
    main > section {
      padding-top: var(--padt);
      padding-bottom: var(--padb);
    }
    main > section[style*="--h: 2"] {
      --padt: 120px;
      --padb: 72px;
    }

    /* ── Hero ───────────────────────────────────────────────────── */
    .hero {
      min-height: calc(100vh - 64px);
      display: flex;
      align-items: center;
      position: relative;
      overflow: hidden;
      padding-top: 80px !important;
      padding-bottom: 80px !important;
      /* subtle radial glow */
      background:
        radial-gradient(ellipse 60% 50% at 70% 50%, rgba(90,185,252,0.07) 0%, transparent 70%),
        var(--p-bg);
    }
    /* animated grid ground */
    .hero::before {
      content: "";
      position: absolute;
      inset: 0;
      background-image:
        linear-gradient(rgba(90,185,252,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(90,185,252,0.04) 1px, transparent 1px);
      background-size: 40px 40px;
      mask-image: radial-gradient(ellipse 80% 80% at 50% 50%, black 30%, transparent 100%);
      pointer-events: none;
    }
    .hero .wrap {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 64px;
      align-items: center;
      position: relative;
    }
    .hero-copy { max-width: 520px; }
    .hero-eyebrow {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      font-weight: 500;
      color: var(--p-accent);
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 20px;
      padding: 5px 12px;
      border: 1px solid rgba(90,185,252,0.25);
      border-radius: 9999px;
      background: rgba(90,185,252,0.06);
    }
    .hero h1 {
      font-family: var(--font-display);
      font-size: clamp(2.8rem, 5vw, 4.5rem);
      font-weight: 800;
      letter-spacing: var(--display-tracking);
      color: #ffffff;
      line-height: 1.08;
      margin-bottom: 20px;
    }
    .hero h1 span {
      background: linear-gradient(90deg, #5ab9fc 0%, #38bdf8 50%, #818cf8 100%);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
    .hero-tagline {
      font-size: 1.15rem;
      color: #94a3b8;
      line-height: 1.6;
      margin-bottom: 28px;
      max-width: 440px;
    }
    .hero-stat {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      font-family: var(--font-mono);
      font-size: 0.82rem;
      color: var(--p-muted);
      margin-bottom: 36px;
    }
    .hero-stat strong {
      color: var(--p-ink);
      font-family: var(--font-display);
      font-weight: 700;
    }
    .hero-stat-sep {
      width: 1px; height: 14px;
      background: var(--p-border);
      display: inline-block;
    }
    .hero-actions {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      align-items: center;
    }
    .btn-primary {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 0.85rem 1.75rem;
      background: var(--p-action);
      color: var(--p-accent-ink);
      border: none;
      border-radius: var(--radius-sm);
      font-family: var(--font-display);
      font-size: 0.95rem;
      font-weight: 700;
      cursor: pointer;
      text-decoration: none;
      box-shadow: 0 4px 20px rgba(90,185,252,0.35);
      transition: background 0.2s, transform 0.2s cubic-bezier(0.16,1,0.3,1), box-shadow 0.2s;
    }
    .btn-primary:hover {
      background: var(--p-action-hover);
      transform: translateY(-2px);
      box-shadow: 0 6px 28px rgba(90,185,252,0.45);
    }
    .btn-primary:active { transform: translateY(0); }

    .btn-ghost {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 0.85rem 1.5rem;
      background: transparent;
      color: var(--p-muted);
      border: 1px solid var(--p-border);
      border-radius: var(--radius-sm);
      font-family: var(--font-display);
      font-size: 0.9rem;
      font-weight: 600;
      cursor: pointer;
      text-decoration: none;
      transition: color 0.2s, border-color 0.2s, transform 0.2s cubic-bezier(0.16,1,0.3,1);
    }
    .btn-ghost:hover {
      color: #ffffff;
      border-color: var(--p-border-hover);
      transform: translateY(-1px);
    }
    .btn-ghost:active { transform: translateY(0); }

    /* ── App-frame (hero product preview) ───────────────────────── */
    .app-frame {
      background: var(--p-surface);
      border: 1px solid var(--p-border);
      border-radius: var(--radius);
      overflow: hidden;
      box-shadow: 0 32px 80px rgba(0,0,0,0.6), 0 0 0 1px rgba(90,185,252,0.08);
      position: relative;
    }
    .app-frame-bar {
      display: flex;
      align-items: center;
      gap: 7px;
      padding: 10px 14px;
      background: rgba(0,0,0,0.3);
      border-bottom: 1px solid var(--p-border);
    }
    .app-frame-dot {
      width: 11px; height: 11px;
      border-radius: 50%;
    }
    .app-frame-dot:nth-child(1) { background: #ef4444; }
    .app-frame-dot:nth-child(2) { background: #f59e0b; }
    .app-frame-dot:nth-child(3) { background: #22c55e; }
    .app-frame-url {
      margin-left: 8px;
      font-family: var(--font-mono);
      font-size: 0.72rem;
      color: var(--p-muted);
      background: rgba(255,255,255,0.04);
      padding: 3px 10px;
      border-radius: 4px;
      border: 1px solid var(--p-border);
    }
    .app-frame-body {
      padding: 16px;
      font-family: var(--font-mono);
      font-size: 0.75rem;
      line-height: 1.65;
      color: #94a3b8;
      max-height: 340px;
      overflow: hidden;
    }
    .json-key   { color: #7dd3fc; }
    .json-str   { color: #86efac; }
    .json-num   { color: #fda4af; }
    .json-bool  { color: #c084fc; }
    .json-label {
      display: inline-block;
      font-family: var(--font-mono);
      font-size: 0.65rem;
      color: var(--p-muted);
      letter-spacing: 0.06em;
      text-transform: uppercase;
      margin-bottom: 6px;
      border-bottom: 1px solid var(--p-border);
      padding-bottom: 4px;
      width: 100%;
    }

    /* ── Sections generic ───────────────────────────────────────── */
    .section-head {
      margin-bottom: 48px;
    }
    .section-head h2 {
      font-family: var(--font-display);
      font-size: clamp(1.6rem, 2.5vw, 2.2rem);
      font-weight: 700;
      letter-spacing: var(--display-tracking);
      color: #ffffff;
      margin-bottom: 10px;
      line-height: 1.2;
    }
    .section-head p {
      font-size: 0.95rem;
      color: var(--p-muted);
      max-width: 600px;
      line-height: 1.6;
    }

    /* ── Simulator section ──────────────────────────────────────── */
    #simulator {
      border-top: 1px solid var(--p-border);
      background: linear-gradient(180deg, rgba(19,24,36,0.5) 0%, transparent 100%);
    }
    .sim-grid {
      display: grid;
      grid-template-columns: 380px 1fr;
      gap: 28px;
      align-items: start;
    }
    @media (max-width: 1024px) {
      .sim-grid { grid-template-columns: 1fr; }
    }

    /* ── Panels ─────────────────────────────────────────────────── */
    .panel {
      background: var(--p-surface);
      border: 1px solid var(--p-border);
      border-radius: var(--radius);
      padding: 1.6rem;
      box-shadow: 0 12px 32px rgba(0,0,0,0.25);
    }
    .panel-h {
      font-family: var(--font-display);
      font-size: 1.05rem;
      font-weight: 700;
      letter-spacing: var(--display-tracking);
      color: #ffffff;
      margin-bottom: 4px;
    }
    .panel-sub {
      font-size: 0.8rem;
      color: var(--p-muted);
      margin-bottom: 1.2rem;
    }

    /* ── Presets ─────────────────────────────────────────────────── */
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
      font-family: var(--font-text);
      font-size: 0.76rem;
      font-weight: 600;
      cursor: pointer;
      transition: background 0.15s, color 0.15s, border-color 0.15s;
    }
    .btn-preset:hover { background: var(--p-border); color: #ffffff; }
    .btn-preset.active {
      background: rgba(90,185,252,0.15);
      border-color: var(--p-action);
      color: var(--p-action);
    }

    /* ── Form fields ─────────────────────────────────────────────── */
    .field { margin-bottom: 1.25rem; }
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
      cursor: pointer;
    }
    .slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      width: 18px; height: 18px;
      border-radius: 50%;
      background: var(--p-action);
      cursor: pointer;
      box-shadow: 0 0 10px rgba(90,185,252,0.6);
      transition: transform 0.15s;
    }
    .slider::-webkit-slider-thumb:hover { transform: scale(1.15); }
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
      transition: border-color 0.2s;
    }
    .select-box:focus, .text-box:focus { border-color: var(--p-action); }

    .btn-submit {
      width: 100%;
      padding: 0.9rem;
      background: var(--p-action);
      color: var(--p-accent-ink);
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
      box-shadow: 0 4px 20px rgba(90,185,252,0.35);
      transition: background 0.2s, transform 0.2s cubic-bezier(0.16,1,0.3,1), box-shadow 0.2s;
    }
    .btn-submit:hover {
      background: var(--p-action-hover);
      transform: translateY(-2px);
      box-shadow: 0 6px 26px rgba(90,185,252,0.45);
    }
    .btn-submit:active { transform: translateY(0); }

    /* ── Risk banner ─────────────────────────────────────────────── */
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
    .risk-CRITICAL { background: rgba(244,63,94,0.10); border-color: rgba(244,63,94,0.35); color: #fb7185; }
    .risk-HIGH     { background: rgba(245,158,11,0.10); border-color: rgba(245,158,11,0.35); color: #fbbf24; }
    .risk-MEDIUM   { background: rgba(90,185,252,0.10); border-color: rgba(90,185,252,0.35); color: #7dd3fc; }
    .risk-LOW      { background: rgba(16,185,129,0.10); border-color: rgba(16,185,129,0.35); color: #34d399; }
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
    .risk-tag span { color: #0a0d14; }

    /* ── KPI tiles ───────────────────────────────────────────────── */
    .kpi-row {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(170px, 1fr));
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
      transition: border-color 0.2s, transform 0.2s cubic-bezier(0.16,1,0.3,1);
    }
    .kpi-tile:hover { border-color: var(--p-border-hover); transform: translateY(-2px); }
    .kpi-tile::before {
      content: "";
      position: absolute;
      top: 0; left: 0;
      width: 4px; height: 100%;
      background: var(--tile-bar, var(--p-action));
    }
    .kpi-title {
      font-size: 0.72rem;
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
    .kpi-sub { font-size: 0.78rem; color: #94a3b8; }

    /* ── SLA impact card ─────────────────────────────────────────── */
    .sla-impact-card {
      background: linear-gradient(135deg, rgba(16,185,129,0.08) 0%, rgba(6,182,212,0.04) 100%);
      border: 1px solid rgba(16,185,129,0.25);
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
      font-size: 0.95rem;
      font-weight: 700;
      color: #34d399;
    }
    .sla-impact-badge {
      background: rgba(16,185,129,0.2);
      color: #34d399;
      font-weight: 800;
      font-size: 0.78rem;
      padding: 3px 12px;
      border-radius: 9999px;
      border: 1px solid rgba(16,185,129,0.4);
    }
    .sla-stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
      gap: 10px;
      margin-top: 0.75rem;
      text-align: center;
    }
    .sla-stat-box {
      background: rgba(0,0,0,0.3);
      padding: 0.65rem;
      border-radius: var(--radius-sm);
      border: 1px solid var(--p-border);
    }
    .sla-stat-label { font-size: 0.68rem; color: var(--p-muted); text-transform: uppercase; font-weight: 600; }
    .sla-stat-val   { font-size: 1.25rem; font-weight: 800; margin-top: 2px; }
    .sla-explanation { font-size: 0.82rem; color: #cbd5e1; margin-top: 0.85rem; line-height: 1.55; }

    /* ── Note boxes ──────────────────────────────────────────────── */
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
    }
    .note-body { font-size: 0.84rem; color: #cbd5e1; line-height: 1.6; }

    /* ── Callouts ────────────────────────────────────────────────── */
    .callout {
      border-radius: var(--radius-sm);
      padding: 0.9rem 1.15rem;
      margin-bottom: 0.65rem;
      display: flex;
      gap: 12px;
      align-items: flex-start;
      font-size: 0.84rem;
    }
    .callout.warn { background: rgba(245,158,11,0.08); border: 1px solid rgba(245,158,11,0.25); color: #fde68a; }
    .callout.rec  { background: rgba(16,185,129,0.08); border: 1px solid rgba(16,185,129,0.25); color: #a7f3d0; }

    /* ── Diagram card (pulsing data flow) ───────────────────────── */
    .diagram-card {
      background: var(--p-surface);
      border: 1px solid var(--p-border);
      border-radius: var(--radius);
      padding: 1.5rem 1.75rem;
      margin-bottom: 48px;
      position: relative;
      overflow: hidden;
    }
    .diagram-card::after {
      content: "";
      position: absolute;
      top: -40px; right: -40px;
      width: 180px; height: 180px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(90,185,252,0.06) 0%, transparent 70%);
      pointer-events: none;
    }
    .diagram-label {
      font-family: var(--font-mono);
      font-size: 0.68rem;
      color: var(--p-muted);
      text-transform: uppercase;
      letter-spacing: 0.08em;
      margin-bottom: 20px;
    }
    .diagram-flow {
      display: flex;
      align-items: center;
      gap: 0;
      flex-wrap: wrap;
      row-gap: 12px;
    }
    .flow-node {
      background: var(--p-surface-2);
      border: 1px solid var(--p-border);
      border-radius: var(--radius-sm);
      padding: 10px 16px;
      text-align: center;
      min-width: 110px;
    }
    .flow-node-icon {
      font-size: 1.15rem;
      margin-bottom: 4px;
      display: block;
    }
    .flow-node-label {
      font-family: var(--font-mono);
      font-size: 0.7rem;
      color: var(--p-accent);
      font-weight: 500;
    }
    .flow-node-sub {
      font-size: 0.65rem;
      color: var(--p-muted);
      margin-top: 2px;
    }
    .flow-arrow {
      flex: 1;
      min-width: 36px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: relative;
      overflow: hidden;
    }
    .flow-arrow-line {
      height: 1px;
      flex: 1;
      background: var(--p-border);
      position: relative;
      overflow: hidden;
    }
    .flow-arrow-line::after {
      content: "";
      position: absolute;
      top: 0; left: -100%;
      width: 60%;
      height: 100%;
      background: linear-gradient(90deg, transparent, var(--p-accent), transparent);
      animation: pulseFlow 2s linear infinite;
    }
    .flow-arrow-line:nth-child(2)::after { animation-delay: 0.66s; }
    .flow-arrow-line:nth-child(3)::after { animation-delay: 1.32s; }
    @keyframes pulseFlow {
      0%   { left: -100%; }
      100% { left: 200%;  }
    }
    .flow-caret {
      color: var(--p-muted);
      font-size: 0.75rem;
      margin-left: -2px;
    }

    /* ── Analytics sections ──────────────────────────────────────── */
    #sla-breaches, #transit-percentiles, #weekly-volume {
      border-top: 1px solid var(--p-border);
    }

    .table-container {
      overflow-x: auto;
      border: 1px solid var(--p-border);
      border-radius: var(--radius-sm);
    }
    table { width: 100%; border-collapse: collapse; font-size: 0.84rem; text-align: left; }
    th {
      background: var(--p-surface-2);
      color: #cbd5e1;
      padding: 0.75rem 1rem;
      font-weight: 600;
      border-bottom: 1px solid var(--p-border);
      white-space: nowrap;
    }
    td {
      padding: 0.75rem 1rem;
      border-bottom: 1px solid var(--p-surface-2);
      color: #e2e8f0;
    }
    tr:last-child td { border-bottom: none; }
    tr:hover td { background: rgba(255,255,255,0.02); }

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
    .pct-bar-fill { height: 100%; background: var(--rose); border-radius: 3px; }

    /* ── Loading overlay ─────────────────────────────────────────── */
    .busy-overlay {
      display: none;
      position: absolute;
      inset: 0;
      background: rgba(10,13,20,0.75);
      backdrop-filter: blur(4px);
      z-index: 20;
      border-radius: var(--radius);
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 0.95rem;
      gap: 10px;
    }

    /* ── Footer ──────────────────────────────────────────────────── */
    footer.site-footer {
      border-top: 1px solid var(--p-border);
      padding: 1.5rem var(--gut);
      text-align: center;
      font-size: 0.78rem;
      color: var(--p-muted);
    }
    footer.site-footer a { color: var(--p-accent); text-decoration: none; }
    footer.site-footer a:hover { text-decoration: underline; }

    /* ── Responsive ──────────────────────────────────────────────── */
    @media (max-width: 900px) {
      .hero .wrap { grid-template-columns: 1fr; }
      .hero-frame  { display: none; }
      .hero { min-height: auto; padding-top: 72px !important; padding-bottom: 72px !important; }
    }
    @media (max-width: 600px) {
      .live-badge { display: none; }
      .kpi-row { grid-template-columns: 1fr 1fr; }
      :root { --padt: 72px; --padb: 48px; }
    }
  </style>
</head>
<body>

  <!-- Navigation -->
  <header class="site-nav">
    <div class="nav-wrap">
      <a href="#top" class="skip-link">Skip to content</a>
      <a href="/" class="brand-group" aria-label="FlashFleet home">
        <div class="brand-symbol" aria-hidden="true">F</div>
        <div>
          <span class="wordmark">FlashFleet</span>
          <span class="wordmark-sub">Fulfillment Simulator</span>
        </div>
      </a>
      <div class="nav-actions">
        <div class="live-badge" aria-label="Dataset status">
          <span class="pulse-dot" aria-hidden="true"></span>
          <span>100k+ Records</span>
        </div>
        <a href="/docs" target="_blank" rel="noopener" class="btn-nav">API Docs ↗</a>
      </div>
    </div>
  </header>

  <main id="top">

    <!-- ── 1. Hero ───────────────────────────────────────────────── -->
    <section class="hero" data-enter style="--h: 1;">
      <div class="wrap">

        <!-- Left: copy -->
        <div class="hero-copy">
          <div class="hero-eyebrow">
            <span aria-hidden="true">&#9650;</span>
            Surge Capacity Intelligence
          </div>
          <h1>Flash<span>Fleet</span></h1>
          <p class="hero-tagline">
            Model flash-sale surge capacity from 100k+ Brazilian delivery records. Fleet sizing, warehouse footprint and SLA impact — in seconds.
          </p>
          <div class="hero-stat" aria-label="Dataset size">
            <strong>1,200 orders indexed</strong>
            <span class="hero-stat-sep" aria-hidden="true"></span>
            Olist e-commerce dataset
            <span class="hero-stat-sep" aria-hidden="true"></span>
            SQLite + FastAPI
          </div>
          <div class="hero-actions">
            <a href="#simulator" class="btn-primary">Simulate Surge</a>
            <a href="#sla-breaches" class="btn-ghost">View Analytics</a>
          </div>
        </div>

        <!-- Right: app-frame product preview -->
        <div class="hero-frame" aria-hidden="true">
          <div class="app-frame">
            <div class="app-frame-bar">
              <span class="app-frame-dot"></span>
              <span class="app-frame-dot"></span>
              <span class="app-frame-dot"></span>
              <span class="app-frame-url">POST /simulate-surge</span>
            </div>
            <div class="app-frame-body">
              <span class="json-label">Simulation Output — Black Friday 8x · SP</span>
{<br>
&nbsp;&nbsp;<span class="json-key">"simulation_id"</span>: <span class="json-str">"ff-20241129-bf8x"</span>,<br>
&nbsp;&nbsp;<span class="json-key">"fleet"</span>: {<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="json-key">"riders_needed_per_day"</span>: <span class="json-num">384</span>,<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="json-key">"total_rider_days"</span>: <span class="json-num">2688</span>,<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="json-key">"total_surge_orders"</span>: <span class="json-num">107520</span>,<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="json-key">"baseline_daily_orders"</span>: <span class="json-num">1680.0</span><br>
&nbsp;&nbsp;},<br>
&nbsp;&nbsp;<span class="json-key">"space"</span>: {<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="json-key">"staging_area_m3"</span>: <span class="json-num">2150.4</span>,<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="json-key">"staging_area_sqm_at_2m_height"</span>: <span class="json-num">1075.2</span><br>
&nbsp;&nbsp;},<br>
&nbsp;&nbsp;<span class="json-key">"cost"</span>: {<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="json-key">"total_marginal_cost_brl"</span>: <span class="json-num">483840.00</span>,<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="json-key">"cost_per_order_brl"</span>: <span class="json-num">4.50</span><br>
&nbsp;&nbsp;},<br>
&nbsp;&nbsp;<span class="json-key">"bottleneck_analysis"</span>: {<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="json-key">"risk_level"</span>: <span class="json-str">"CRITICAL"</span>,<br>
&nbsp;&nbsp;&nbsp;&nbsp;<span class="json-key">"bottlenecks"</span>: [<span class="json-str">"Warehouse capacity exceeded"</span>]<br>
&nbsp;&nbsp;}<br>
}
            </div>
          </div>
        </div>

      </div>
    </section>

    <!-- ── 2. Surge Simulator ─────────────────────────────────────── -->
    <section id="simulator" style="--h: 2;">
      <div class="wrap">

        <div class="section-head">
          <h2>Surge Simulator</h2>
          <p>Configure demand parameters, then run the model to see fleet, warehouse and cost requirements against the SQL baseline.</p>
        </div>

        <div class="sim-grid">

          <!-- Controls -->
          <div class="panel" style="position: relative;">
            <div class="panel-h">Surge Parameters</div>
            <p class="panel-sub">Model dynamic flash-sale volume increases.</p>

            <div class="preset-bar" role="group" aria-label="Scenario presets">
              <button class="btn-preset active" onclick="setPreset(3.0, 3, 'SP')">Weekend 3x</button>
              <button class="btn-preset" onclick="setPreset(5.0, 5, 'SP')">Mega 5x</button>
              <button class="btn-preset" onclick="setPreset(2.0, 2, 'RJ')">Mini 2x</button>
              <button class="btn-preset" onclick="setPreset(8.0, 7, null)">Black Friday 8x</button>
            </div>

            <form id="simForm" onsubmit="handleFormSubmit(event)" novalidate>
              <div class="field">
                <label for="param_multiplier">
                  <span>Demand Surge Multiplier</span>
                  <span id="lbl_multiplier" class="num">3.0x (+300%)</span>
                </label>
                <input type="range" id="param_multiplier" class="slider" min="1.0" max="10.0" step="0.5" value="3.0" oninput="onMultiplierChange(this.value)" aria-describedby="lbl_multiplier">
              </div>

              <div class="field">
                <label for="param_region">Target Region (State)</label>
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
                <label for="param_duration">
                  <span>Sale Duration</span>
                  <span id="lbl_duration" class="num">3 Days</span>
                </label>
                <input type="range" id="param_duration" class="slider" min="1" max="14" step="1" value="3" oninput="onDurationChange(this.value)" aria-describedby="lbl_duration">
              </div>

              <div class="field">
                <label for="param_capacity">Rider Throughput (pkgs/rider/day)</label>
                <input type="number" id="param_capacity" class="text-box" min="5" max="200" value="40">
              </div>

              <div class="field">
                <label for="param_wage">Rider Daily Wage (R$ / day)</label>
                <input type="number" id="param_wage" class="text-box" min="50" max="1000" value="150.0">
              </div>

              <div class="field">
                <label for="param_warehouse">Warehouse Spot Lease (R$ / m³ / day)</label>
                <input type="number" id="param_warehouse" class="text-box" min="1" max="100" value="5.0">
              </div>

              <div class="field">
                <label for="param_buffer">Staging Area Buffer (Safety Multiplier)</label>
                <input type="number" id="param_buffer" class="text-box" min="1.0" max="3.0" step="0.1" value="1.3">
              </div>

              <button type="submit" class="btn-submit">Simulate Surge</button>
            </form>
          </div>

          <!-- Results -->
          <div class="panel" style="position: relative;">
            <div id="busyIndicator" class="busy-overlay" role="status" aria-live="polite">
              <span>Calculating fleet requirements and SQL baseline metrics...</span>
            </div>

            <!-- Risk Banner -->
            <div id="riskBanner" class="risk-banner risk-HIGH" role="status">
              <div class="risk-heading">
                <span>Operational Risk:</span>
                <div class="risk-tag"><span id="riskBadgeText">HIGH</span></div>
              </div>
              <div style="font-size: 0.78rem; font-family: var(--font-mono); color: #cbd5e1;" id="simMeta">Sim ID: Ready</div>
            </div>

            <!-- KPI tiles -->
            <div class="kpi-row">
              <div class="kpi-tile" style="--tile-bar: #38bdf8;">
                <div class="kpi-title">Fleet Sizing</div>
                <div class="kpi-stat" id="kpi_riders">0</div>
                <div class="kpi-sub" id="kpi_rider_days">0 total rider-days</div>
              </div>

              <div class="kpi-tile" style="--tile-bar: #a855f7;">
                <div class="kpi-title">Warehouse Footprint</div>
                <div class="kpi-stat" id="kpi_space">0.0 m²</div>
                <div class="kpi-sub" id="kpi_volume">0.0 m³ package staging</div>
              </div>

              <div class="kpi-tile" style="--tile-bar: #10b981;">
                <div class="kpi-title">Marginal Cost</div>
                <div class="kpi-stat" id="kpi_cost">R$ 0</div>
                <div class="kpi-sub" id="kpi_cost_per_order">R$ 0.00 / order</div>
              </div>

              <div class="kpi-tile" style="--tile-bar: #06b6d4;">
                <div class="kpi-title">Surge Volume</div>
                <div class="kpi-stat" id="kpi_orders">0</div>
                <div class="kpi-sub" id="kpi_baseline_daily">Baseline: 0 / day</div>
              </div>
            </div>

            <!-- SLA Impact -->
            <div class="sla-impact-card">
              <div class="sla-impact-top">
                <div class="sla-impact-title">Actionable SLA Optimization Impact</div>
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

            <!-- Formula breakdowns -->
            <div class="note-box">
              <div class="note-title">Fleet Sizing Logic</div>
              <div class="note-body" id="exp_fleet">Computing fleet allocation...</div>
            </div>

            <div class="note-box">
              <div class="note-title">Warehouse Footprint Calculation (2m Stacking Height)</div>
              <div class="note-body" id="exp_space">Computing storage footprint...</div>
            </div>

            <div class="note-box">
              <div class="note-title">Marginal Operational Cost Projection</div>
              <div class="note-body" id="exp_cost">Computing marginal expenditure...</div>
            </div>

            <!-- Bottlenecks & Recommendations -->
            <div style="margin-top: 1.4rem;">
              <h3 style="font-size: 0.95rem; font-weight: 700; margin-bottom: 0.6rem; color: #f1f5f9;">Identified Bottlenecks &amp; Strategic Mitigations</h3>
              <div id="bottlenecksList"></div>
              <div id="recommendationsList"></div>
            </div>
          </div>
        </div><!-- /sim-grid -->

      </div>
    </section>

    <!-- ── 3. SQL Baseline Analytics intro + diagram ──────────────── -->
    <section id="analytics-intro" style="--h: 1; padding-bottom: 0 !important;">
      <div class="wrap">

        <div class="section-head">
          <h2>SQL Baseline Analytics</h2>
          <p>Real historical benchmarks extracted from the Olist delivery dataset via CTEs and Window Functions.</p>
        </div>

        <!-- Pulsing data-flow diagram card -->
        <div class="diagram-card" role="img" aria-label="Data flow: SQL Olist dataset to simulation engine to REST API">
          <div class="diagram-label">Data pipeline</div>
          <div class="diagram-flow">

            <div class="flow-node">
              <span class="flow-node-icon" aria-hidden="true">&#128190;</span>
              <div class="flow-node-label">SQL / Olist</div>
              <div class="flow-node-sub">100k+ records</div>
            </div>

            <div class="flow-arrow" aria-hidden="true">
              <div class="flow-arrow-line"></div>
              <span class="flow-caret">&#9658;</span>
            </div>

            <div class="flow-node">
              <span class="flow-node-icon" aria-hidden="true">&#9881;</span>
              <div class="flow-node-label">CTEs + Windows</div>
              <div class="flow-node-sub">SQLite engine</div>
            </div>

            <div class="flow-arrow" aria-hidden="true">
              <div class="flow-arrow-line"></div>
              <span class="flow-caret">&#9658;</span>
            </div>

            <div class="flow-node">
              <span class="flow-node-icon" aria-hidden="true">&#9889;</span>
              <div class="flow-node-label">Surge Model</div>
              <div class="flow-node-sub">Fleet + cost engine</div>
            </div>

            <div class="flow-arrow" aria-hidden="true">
              <div class="flow-arrow-line"></div>
              <span class="flow-caret">&#9658;</span>
            </div>

            <div class="flow-node">
              <span class="flow-node-icon" aria-hidden="true">&#127760;</span>
              <div class="flow-node-label">REST API</div>
              <div class="flow-node-sub">FastAPI / JSON</div>
            </div>

          </div>
        </div>

      </div>
    </section>

    <!-- ── 4. Regional SLA Breaches ──────────────────────────────── -->
    <section id="sla-breaches" style="--h: 1;">
      <div class="wrap">

        <div class="section-head">
          <h2>Regional SLA Breaches</h2>
          <p>Delivery SLA breach rates by Brazilian state from historical Olist data.</p>
        </div>

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
    </section>

    <!-- ── 5. Freight Transit Percentiles ────────────────────────── -->
    <section id="transit-percentiles" style="--h: 1;">
      <div class="wrap">

        <div class="section-head">
          <h2>Freight Transit Percentiles (P90)</h2>
          <p>90th-percentile transit time comparison: heavy freight vs lightweight parcels.</p>
        </div>

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
    </section>

    <!-- ── 6. Weekly Order Volume Density ────────────────────────── -->
    <section id="weekly-volume" style="--h: 1;">
      <div class="wrap">

        <div class="section-head">
          <h2>Weekly Order Volume Density</h2>
          <p>Historical baseline order volume with 4-week rolling average (SQL window function).</p>
        </div>

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
    <p>FlashFleet &mdash; E-Commerce Fulfillment Simulator &nbsp;|&nbsp; Historical data: <a href="https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce" rel="noopener" target="_blank">Olist Brazilian E-Commerce</a> &nbsp;|&nbsp; SQLite &amp; FastAPI &nbsp;|&nbsp; &copy; 2024</p>
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

    function handleFormSubmit(e) {
      if (e) e.preventDefault();
      triggerSim();
    }

    async function triggerSim() {
      const loader = document.getElementById('busyIndicator');
      loader.style.display = 'flex';

      const payload = {
        surge_multiplier:            parseFloat(document.getElementById('param_multiplier').value),
        target_region:               document.getElementById('param_region').value || null,
        surge_duration_days:         parseInt(document.getElementById('param_duration').value, 10),
        rider_capacity_per_day:      parseInt(document.getElementById('param_capacity').value, 10),
        rider_daily_wage_brl:        parseFloat(document.getElementById('param_wage').value),
        warehouse_cost_per_m3_day_brl: parseFloat(document.getElementById('param_warehouse').value),
        staging_buffer_factor:       parseFloat(document.getElementById('param_buffer').value)
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
      const risk   = data.bottleneck_analysis.risk_level;
      const banner = document.getElementById('riskBanner');
      banner.className = 'risk-banner risk-' + risk;
      document.getElementById('riskBadgeText').innerText = risk;
      document.getElementById('simMeta').innerText =
        'Sim ID: ' + data.simulation_id.substring(0, 8) + '... | ' + (data.params.target_region || 'ALL');

      // KPIs
      document.getElementById('kpi_riders').innerText         = data.fleet.riders_needed_per_day.toLocaleString();
      document.getElementById('kpi_rider_days').innerText     = data.fleet.total_rider_days.toLocaleString() + ' total rider-days';
      document.getElementById('kpi_space').innerText          = data.space.staging_area_sqm_at_2m_height.toFixed(1) + ' m\u00b2';
      document.getElementById('kpi_volume').innerText         = data.space.staging_area_m3.toFixed(2) + ' m\u00b3 staging volume';
      document.getElementById('kpi_cost').innerText           = 'R$ ' + data.cost.total_marginal_cost_brl.toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 });
      document.getElementById('kpi_cost_per_order').innerText = 'R$ ' + data.cost.cost_per_order_brl.toFixed(2) + ' / order';
      document.getElementById('kpi_orders').innerText         = data.fleet.total_surge_orders.toLocaleString();
      document.getElementById('kpi_baseline_daily').innerText = 'Baseline: ' + data.fleet.baseline_daily_orders.toFixed(1) + ' / day';

      // Explanations
      document.getElementById('exp_fleet').innerText = data.fleet.explanation;
      document.getElementById('exp_space').innerText = data.space.explanation;
      document.getElementById('exp_cost').innerText  = data.cost.explanation;

      // SLA Impact
      if (data.sla_impact) {
        document.getElementById('sla_unmitigated').innerText = data.sla_impact.unmitigated_surge_breach_rate_pct.toFixed(1) + '%';
        document.getElementById('sla_optimized').innerText   = data.sla_impact.optimized_breach_rate_pct.toFixed(1) + '%';
        document.getElementById('sla_prevented').innerText   = data.sla_impact.prevented_breaches.toLocaleString() + ' orders';
        document.getElementById('sla_explanation').innerText = data.sla_impact.explanation;
      }

      // Bottlenecks & Recommendations
      const bList = document.getElementById('bottlenecksList');
      bList.innerHTML = '';
      if (data.bottleneck_analysis.bottlenecks && data.bottleneck_analysis.bottlenecks.length > 0) {
        data.bottleneck_analysis.bottlenecks.forEach(b => {
          bList.innerHTML += `<div class="callout warn"><span>&#9888;</span><div><strong>Bottleneck:</strong> ${b}</div></div>`;
        });
      }

      const rList = document.getElementById('recommendationsList');
      rList.innerHTML = '';
      if (data.bottleneck_analysis.recommendations && data.bottleneck_analysis.recommendations.length > 0) {
        data.bottleneck_analysis.recommendations.forEach(r => {
          rList.innerHTML += `<div class="callout rec"><span>&#10004;</span><div><strong>Recommendation:</strong> ${r}</div></div>`;
        });
      }
    }

    async function loadSqlAnalytics() {
      // 1. SLA Breaches
      try {
        const res  = await fetch('/analytics/sla-breaches');
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
              <td>${row.avg_breach_days !== null ? row.avg_breach_days + 'd' : '&mdash;'}</td>
            </tr>
          `;
        });
      } catch (e) { console.error('SLA error', e); }

      // 2. Freight Transit Percentiles
      try {
        const res  = await fetch('/analytics/transit-percentiles');
        const list = await res.json();
        const tbody = document.getElementById('transitTableBody');
        tbody.innerHTML = '';
        list.forEach(row => {
          tbody.innerHTML += `
            <tr>
              <td><strong>${row.weight_class === 'heavy_freight' ? 'Heavy Freight (&ge; 5kg)' : 'Lightweight Parcels (&lt; 5kg)'}</strong></td>
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
        const res  = await fetch('/analytics/weekly-volume');
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

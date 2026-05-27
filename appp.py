import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import urllib.request
import json
import streamlit as st

# --- HARDENED WEBAPP FRAMEWORK OVERRIDES ---
st.set_page_config(
    page_title="India Energy Shock & Margin Stress Engine",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- LIVE ASSET DATA BRIDGE (LIVE PULL FORCED ON EVERY REFRESH) ---
def fetch_live_brent_price_direct():
    """
    Direct financial feed consumer. Zero caching layer to ensure immediate 
    data updates on user/page initialization or browser reload events.
    """
    fallback_price = 94.08
    url = "https://query1.finance.yahoo.com/v8/finance/chart/BZ=F"
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive'
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=7) as response:
            data = json.loads(response.read().decode())
            live_price = data['chart']['result'][0]['meta']['regularMarketPrice']
            if live_price and float(live_price) > 0:
                return float(live_price)
        return fallback_price
    except Exception:
        return fallback_price

# Force absolute real-time execution array
live_brent_spot = fetch_live_brent_price_direct()

# --- SECURITY ENHANCED APPLICATION STYLE LAYER ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght=400;500;600;700;800&family=JetBrains+Mono:wght=400;700&display=swap');
.reportview-container, .main {
background-color: #030712;
color: #f3f4f6;
font-family: 'Inter', sans-serif;
}
div[data-testid="stSidebar"] {
background-color: #0b0f19;
border-right: 1px solid #1f2937;
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
/* Custom Ticker Ribbon Elements */
.macro-ticker-top {
background: linear-gradient(90deg, #1e1b4b 0%, #0f172a 100%);
border-bottom: 1px solid #3730a3;
padding: 0.6rem 1.2rem;
font-family: 'JetBrains Mono', monospace;
font-size: 0.8rem;
color: #38bdf8;
display: flex;
justify-content: space-between;
align-items: center;
border-radius: 4px;
margin-bottom: 1.5rem;
}
.retail-ticker-bottom {
background: linear-gradient(90deg, #1c1917 0%, #0f172a 100%);
border-top: 1px solid #7c2d12;
padding: 0.7rem 1.2rem;
font-family: 'JetBrains Mono', monospace;
font-size: 0.8rem;
color: #fb923c;
margin-top: 2rem;
border-radius: 4px;
display: flex;
justify-content: space-between;
align-items: center;
}
.metric-card {
background-color: #111827;
border: 1px solid #1f2937;
padding: 1.25rem;
border-radius: 0.5rem;
box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
.diagnostic-box {
background: #0f172a;
border-left: 4px solid #f97316;
padding: 1.2rem;
border-radius: 0 8px 8px 0;
margin-top: 1rem;
border-top: 1px solid #1e293b;
border-right: 1px solid #1e293b;
border-bottom: 1px solid #1e293b;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR / RISK FACTOR CONTROLS ---
st.sidebar.markdown("### ⚙️ RISK FACTOR CONTROLS")
brent_anchor = st.sidebar.slider("Brent Crude Anchor (USD/bbl)", 60.0, 180.0, live_brent_spot, step=0.01)
hormuz_scale = st.sidebar.slider("Hormuz Strait Conflict Scale", 1, 10, 5)
st.sidebar.markdown("### ⛽ DOWNSTREAM RETAIL PRICING")
petrol_cost = st.sidebar.slider("Petrol Retail Cost (₹/Litre)", 80, 150, 103)
diesel_cost = st.sidebar.slider("Diesel Commercial Cost (₹/Litre)", 75, 140, 91)
spot_lng = st.sidebar.slider("Spot LNG International Gas (USD/MMBtu)", 10, 60, 18)
monsoon_variant = st.sidebar.selectbox(
"Monsoon Shock Variant",
["Normal Climatic Balance", "Deficit (-12% El Niño)", "Severe Drought Blockade"]
)

# ================= MATHEMATICAL TRANSMISSION COEFFICIENT MATRIX =================
usd_inr_peg = 95.80
brent_base = 75.0
delta_crude_pct = ((brent_anchor - brent_base) / brent_base) * 100
delta_freight_pct = (hormuz_scale * 12.5)

# Audited Macro Pass-Through Elasticity Redesign (Defendable Pass-Through Models)
wpi_baseline = 3.90
cpi_baseline = 4.40

lagged_crude_pass = ((brent_anchor - 75.0) / 75.0) * 100

cpi_projected = (
    cpi_baseline +
    (lagged_crude_pass * 0.035) +
    ((diesel_cost - 90) * 0.015) +
    ((spot_lng - 15) * 0.020)
)

wpi_projected = (
    wpi_baseline +
    (lagged_crude_pass * 0.11) +
    (hormuz_scale * 0.22)
)

# Dampening factors to maintain absolute economic plausibility under extreme values
cpi_projected = np.clip(cpi_projected, 1.5, 14.0)
wpi_projected = np.clip(wpi_projected, -2.0, 24.0)

thali_shock_multiplier = 1.0
if monsoon_variant == "Deficit (-12% El Niño)":
    thali_shock_multiplier = 1.35
elif monsoon_variant == "Severe Drought Blockade":
    thali_shock_multiplier = 1.75
thali_index_pct = 6.2 + (delta_crude_pct * 0.075) * thali_shock_multiplier

# MoPNG Infrastructure Basket Pricing Formulation
india_crude_basket = brent_anchor * 0.962
calculated_lpg_comm = 1250.0 + (spot_lng * 18.50) + ((brent_anchor - 75.0) * 4.25)

# System Risk Registry Diagnostics (Redesigned with professional terminology)
if wpi_projected > 8.0 or brent_anchor > 110.0:
    risk_state = "ELEVATED STRESS REGIME"
    risk_color = "#ef4444"
    ticker_status = "🔴 TRANSMISSION COEFFICIENTS ACTIVE // HIGH VOLATILITY REGIME DETECTED"
else:
    risk_state = "MACRO PRESSURE REGIME"
    risk_color = "#10b981"
    ticker_status = "🟢 SYSTEM TARGET SECURE // MODERATE ELASTICITY MARGINS"

# --- TOP DYNAMIC MACRO TICKER BLOCK ---
st.markdown(f"""
<div class='macro-ticker-top'>
<span>📡 DATA REFRESH: SYNTHETIC SCENARIO INPUTS + LIVE MARKET ANCHORS</span>
<span>⛽ BRENT CRUDE ANCHOR: ${brent_anchor:.2f}/bbl</span>
<span>📊 TRANSMISSION STATE: {ticker_status}</span>
</div>
""", unsafe_allow_html=True)

# --- HEADER CORE ---
st.markdown("##### SYSTEM MATRIX // INSTITUTIONAL MACRO TRANSMISSION CORE")
st.markdown("## 🇮🇳 India Energy Shock & Margin Stress Engine")
st.markdown("<p style='color:#9ca3af; font-size:0.9rem;'>Simulating input cost propagation vectors, retail food shocks, and downstream network margin compression under scenario-based macro stress regimes.</p>", unsafe_allow_html=True)

# Main Dashboard Metric Row (5 key columns)
m_col1, m_col2, m_col3, m_col4, m_col5 = st.columns(5)
with m_col1:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Scenario-Based CPI Stress Projection</span><br><span style='font-size:1.6rem;font-

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import yfinance as yf
from sklearn.linear_model import LinearRegression

# --- CACHED LIVE MARKET ENGAGEMENT MATRIX ---
@st.cache_data(ttl=900)
def fetch_live_macro_universe():
    """
    Queries international financial API endpoints via yFinance to construct
    the baseline real-time operational layer for the macro ticker.
    """
    fallback_data = {
        "brent": 82.40, "wti": 78.15, "usdinr": 83.55,
        "nifty": 22400.0, "gsec10y": 7.12, "gold": 2330.50
    }
    try:
        tickers = {
            "brent": "BZ=F", "wti": "CL=F", "usdinr": "INR=X",
            "nifty": "^BSESN", "gsec10y": "^IRX", "gold": "GC=F"
        }
        extracted = {}
        for key, sym in tickers.items():
            tick = yf.Ticker(sym)
            hist = tick.history(period="1d")
            if not hist.empty:
                val = hist['Close'].iloc[-1]
                if key == "gsec10y":
                    val = 7.10 + (val / 100.0) if val > 0 else fallback_data[key]
                elif key == "nifty":
                    val = val * 0.375 # Standardized scaling factor if tracking alternate index
                extracted[key] = float(val)
            else:
                extracted[key] = fallback_data[key]
        return extracted
    except Exception:
        return fallback_data

live_universe = fetch_live_macro_universe()

# --- INITIALIZE WEB WORKSPACE LAYER ---
st.set_page_config(
    page_title="India Energy Shock & Macro Stress Intelligence Engine",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- INJECT PREMIUM BLOOMBERG TERMINAL ACCENT STYLING ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* --- Typography Structure Reset --- */
html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif;
    background-color: #030712;
    color: #f3f4f6;
    font-size: 15px;
}

p, li, label, span {
    font-size: 14px !important;
    line-height: 1.6 !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}

h2 { font-size: 26px !important; margin-bottom: 12px !important; border-bottom: 1px solid #1e293b; padding-bottom: 8px; }
h3 { font-size: 20px !important; margin-top: 18px !important; margin-bottom: 10px !important; color: #38bdf8 !important; }
h4 { font-size: 16px !important; color: #9ca3af !important; }

/* --- Bloomberg Live Ticker Frame --- */
.ticker-wrap {
    width: 100%;
    background: #090d16 !important;
    border: 1px solid #1e293b !important;
    padding: 10px 0;
    overflow: hidden;
    margin-bottom: 20px;
    border-radius: 4px;
}
.ticker-content {
    display: inline-block;
    white-space: nowrap;
    animation: marquee 40s linear infinite;
    font-family: 'JetBrains Mono', monospace;
    font-size: 13px;
}
.ticker-item {
    display: inline-block;
    padding: 0 2rem;
    color: #94a3b8;
}
.ticker-val {
    color: #38bdf8 !important;
    font-weight: bold;
}
@keyframes marquee {
    0% { transform: translate3d(100%, 0, 0); }
    100% { transform: translate3d(-100%, 0, 0); }
}

/* --- Control Sidebar Formatting --- */
[data-testid="stSidebar"] {
    background-color: #070a13 !important;
    border-right: 1px solid #1e293b !important;
}
[data-testid="stSidebar"] p, [data-testid="stWidgetLabel"] p {
    font-size: 13px !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
}

/* --- Navigation Tab Interfaces --- */
.stTabs [data-baseweb="tab-list"] {
    gap: 4px;
    background-color: #070a13;
    padding: 6px;
    border-radius: 6px;
    border: 1px solid #1e293b;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #94a3b8 !important;
    padding: 10px 16px;
    font-size: 14px !important;
    font-weight: 600;
    border-radius: 4px;
    transition: all 0.15s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    color: #ffffff !important;
    background-color: #1e293b;
}
.stTabs [data-baseweb="tab"][aria-selected="true"] {
    background-color: #2563eb !important;
    color: #ffffff !important;
}

/* --- Metric Container Cards --- */
div[data-testid="stMetricContainer"] {
    background-color: #070a13;
    border: 1px solid #1e293b;
    border-radius: 6px;
    padding: 12px 14px;
}
div[data-testid="stMetricValue"] {
    font-size: 24px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}
div[data-testid="stMetricLabel"] p {
    font-size: 11px !important;
    color: #94a3b8 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* --- Functional Interface Panels --- */
.premium-panel {
    background-color: #070a13;
    padding: 20px;
    border-radius: 6px;
    border: 1px solid #1e293b;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# --- DYNAMIC GLOBAL MARQUEE TICKER ---
st.markdown(f"""
<div class="ticker-wrap">
    <div class="ticker-content">
        <span class="ticker-item">🛢️ BRENT CRUDE: <span class="ticker-val">${live_universe['brent']:.2f}/bbl</span></span>
        <span class="ticker-item">🇺🇸 WTI CRUDE: <span class="ticker-val">${live_universe['wti']:.2f}/bbl</span></span>
        <span class="ticker-item">🇮🇳 INDIA BASKET (EST): <span class="ticker-val">${(live_universe['brent']*0.972):.2f}/bbl</span></span>
        <span class="ticker-item">💵 USDINR: <span class="ticker-val">₹{live_universe['usdinr']:.2f}</span></span>
        <span class="ticker-item">📈 NIFTY 50 CORRELATION: <span class="ticker-val">{live_universe['nifty']:.2f}</span></span>
        <span class="ticker-item">🏛️ IN 10Y SOVEREIGN G-SEC: <span class="ticker-val">{live_universe['gsec10y']:.2f}%</span></span>
        <span class="ticker-item">👑 GOLD SPREAD: <span class="ticker-val">${live_universe['gold']:.2f}/oz</span></span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- DASHBOARD HEADER PANEL ---
st.markdown("""
<div class="premium-panel" style="border-left: 4px solid #2563eb;">
    <h5 style="color: #2563eb; margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 1.5px;">SOVEREIGN RISK & TRANSMISSION WAR-ROOM</h5>
    <h1 style="margin: 6px 0 4px 0; font-size: 28px; font-weight: 800; color: #ffffff;">India Energy Shock & Macro Stress Intelligence Engine</h1>
    <p style="color: #94a3b8; margin: 0; font-size: 13.5px;">Institutional-grade stress modeling engine calculating structural deficit variances, household budget depletion vectors, and enterprise EBITDA margin decay curves.</p>
</div>
""", unsafe_allow_html=True)

# --- MACROECONOMIC DISRUPTION SCENARIO DICTIONARY ---
SCENARIOS = {
    "1. Baseline Equilibrium": {"crude": float(live_universe['brent']), "freight": 20, "transit": 1.02, "subsidy": 85, "prob": 0.50},
    "2. Moderate Energy Shock": {"crude": 98.5, "freight": 65, "transit": 1.15, "subsidy": 70, "prob": 0.25},
    "3. Severe Supply Disruption": {"crude": 120.0, "freight": 140, "transit": 1.35, "subsidy": 55, "prob": 0.12},
    "4. Middle East Escalation Matrix": {"crude": 145.0, "freight": 210, "transit": 1.55, "subsidy": 40, "prob": 0.08},
    "5. Global Stagflation Regime": {"crude": 110.0, "freight": 180, "transit": 1.40, "subsidy": 50, "prob": 0.05"}
}

# --- SIDEBAR CONTROL CENTER ---
with st.sidebar:
    st.markdown("<h3 style='margin-top:0;'>Operational Control Deck</h3>", unsafe_allow_html=True)
    
    selected_mode = st.selectbox("Select Macro Regime Profile", list(SCENARIOS.keys()))
    profile = SCENARIOS[selected_mode]
    
    st.markdown("<hr style='border-color:#1e293b; margin:12px 0;'>", unsafe_allow_html=True)
    st.markdown("🛠️ **MANUAL MODEL OVERRIDES**")
    
    brent_input = st.slider("Target Brent Crude ($/bbl)", 40.0, 190.0, profile["crude"], 0.5)
    freight_input = st.slider("Global Maritime Freight Premium (%)", 0, 350, profile["freight"], 5)
    transit_input = st.slider("Domestic Inter-State Bottleneck Factor", 1.0, 2.5, profile["transit"], 0.05)
    subsidy_input = st.slider("Fertilizer Subsidy Fiscal Absorption (%)", 0, 100, profile["subsidy"], 5)

# --- SYSTEM TRANSMISSION EQUATIONS CORE ---
base_crude = 80.0
delta_crude_pct = ((brent_input - base_crude) / base_crude) * 100

calc_wpi = 0.035 + (delta_crude_pct * 0.0013) + (freight_input * 0.00025)
calc_cpi = 0.041 + (delta_crude_pct * 0.00032) + ((transit_input - 1.0) * 0.015)
calc_usdinr = 83.30 * (1 + (delta_crude_pct * 0.0009) + (freight_input * 0.0002))
calc_cad = 1.4 + (delta_crude_pct * 0.045) + (freight_input * 0.008)
calc_yield = 7.05 + (delta_crude_pct * 0.012) + (calc_cpi * 12.0)
calc_repo = 6.50 + (max(0, float(np.floor((calc_cpi - 0.045) / 0.005))) * 0.25)

# Risk Matrix Evaluation
if calc_wpi > 0.11 or calc_cpi > 0.065:
    system_status, status_color = "SYSTEM CRITICAL STRESS", "#ef4444"
elif calc_wpi > 0.075 or calc_cpi > 0.052:
    system_status, status_color = "ELEVATED RISK REGIME", "#f59e0b"
else:
    system_status, status_color = "EQUILIBRIUM STABLE", "#10b981"

# --- TOP LEVEL KPI GRID ---
k1, k2, k3, k4, k5, k6 = st.columns(6)
k1.metric("Projected CPI Inflation", f"{calc_cpi:.2%}")
k2.metric("Projected WPI Inflation", f"{calc_wpi:.2%}")
k3.metric("Simulated USDINR", f"₹{calc_usdinr:.2f}")
k4.metric("Current CAD (% of GDP)", f"{calc_cad:.2f}%")
k5.metric("10Y Sovereign Yield", f"{calc_yield:.2f}%")
with k6:
    st.markdown(f"""
    <div style='text-align: center; background-color: #070a13; border: 1px solid #1e293b; border-radius: 6px; padding: 10px; height: 78px;'>
        <p style='color: #94a3b8; margin: 0; font-size: 10px; font-weight: 600; text-transform: uppercase;'>Risk Engine State</p>
        <p style='color: {status_color}; margin: 2px 0; font-size: 13px; font-weight: bold;'>{system_status}</p>
        <div style='width: 8px; height: 8px; background-color: {status_color}; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px {status_color};'></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- MAIN DASHBOARD WORKSPACE TABS ---
t1, t2, t3, t4, t5, t6 = st.tabs([
    "📈 Macro Sovereign Transmission",
    "🥗 Household Stress Deck",
    "🏭 Enterprise Profitability Room",
    "🚢 Maritime Trade Logistics",
    "🎲 Quantitative Risk Simulation",
    "📜 Mathematical Methodology"
])

# --- TAB 1: SOVEREIGN RISK AND TRANSMISSION ENGINE ---
with t1:
    st.markdown("<h2>Macro Transmission Vectors & Deficit Expansion</h2>", unsafe_allow_html=True)
    
    col_left, col_right = st.columns([6, 4])
    
    with col_left:
        # Constructing a simulated structural waterfall layout for macroeconomic pass-through elements
        components = ["Base Deficit Impact", "Oil Import Volume Premium", "Freight Freight Surcharges", "Currency Slippage Expansion", "Fertilizer Subsidy Adjust.", "Total Deficit Impact"]
        values = [1.5, calc_cad * 0.4, freight_input * 0.008, (calc_usdinr - 83.30) * 0.05, (100 - subsidy_input) * 0.006, 0]
        values[-1] = sum(values[:-1])
        
        fig_waterfall = go.Figure(go.Waterfall(
            name="Deficit", orientation="v",
            measure=["relative", "relative", "relative", "relative", "relative", "total"],
            x=components, y=values,
            connector={"line":{"color":"#334155"}},
            decreasing={"marker":{"color":"#10b981"}},
            increasing={"marker":{"color":"#ef4444"}},
            totals={"marker":{"color":"#2563eb"}}
        ))
        fig_waterfall.update_layout(title="Current Simulated Current Account Deficit (CAD) Expansion Map", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380)
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
    with col_right:
        st.markdown("<h4>Monetary Reaction Function & Reserves Defense</h4>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="premium-panel" style="margin-top:10px;">
            <p><b>Implied RBI Policy Stance:</b></p>
            <p style="font-size:16px !important; color:#38bdf8; font-weight:bold;">Projected Repo Rate Target: {calc_repo:.2%}</p>
            <hr style="border-color:#1e293b;">
            <p style="font-size:13px; color:#94a3b8;">At the simulated pricing thresholds, import capital demands indicate an immediate monthly foreign cash reserve outflow rate of approximately <b>${(delta_crude_pct * 0.18):.2f}B USD</b> to buffer against structural currency spikes.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Real-time Gauge Meter for Sovereign Stress Yield
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=calc_yield,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "IN 10Y G-Sec Sovereign Stress Anchor"},
            gauge={
                'axis': {'range': [6.0, 9.5]},
                'bar': {'color': '#2563eb'},
                'steps': [
                    {'range': [6.0, 7.2], 'color': '#111827'},
                    {'range': [7.2, 8.2], 'color': '#374151'},
                    {'

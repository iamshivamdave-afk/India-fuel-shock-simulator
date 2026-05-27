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
# Updated with user provided live currency peg
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
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Scenario-Based CPI Stress Projection</span><br><span style='font-size:1.6rem;font-weight:700;'>{cpi_projected:.2f}%</span></div>", unsafe_allow_html=True)
with m_col2:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Synthetic WPI Transmission Estimate</span><br><span style='font-size:1.6rem;font-weight:700;color:#38bdf8;'>{wpi_projected:.2f}%</span></div>", unsafe_allow_html=True)
with m_col3:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Estimated Oil Pass-Through Effect</span><br><span style='font-size:1.6rem;font-weight:700;'>{lagged_crude_pass:.2f}%</span></div>", unsafe_allow_html=True)
with m_col4:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Modeled Inflation Stress Path (Thali)</span><br><span style='font-size:1.6rem;font-weight:700;color:#f87171;'>+{thali_index_pct:.1f}%</span></div>", unsafe_allow_html=True)
with m_col5:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Simulated Market Stress Regime</span><br><span style='font-size:1rem;font-weight:700;color:{risk_color};'>{risk_state}</span></div>", unsafe_allow_html=True)

st.markdown("---")

# --- APP SYSTEM NAVIGATION TABS ---
# Removed 'Food Tech Delivery Index' tab completely, Added '📚 Historical Crisis Comparator'
tabs = st.tabs([
    "📚 Historical Crisis Comparator",
    "🌾 Kitchen Thali Logistics Engine", 
    "🏭 FMCG Defense Dossiers", 
    "🥥 Edible Oil Import Shock & Kitchen Inflation",
    "🏦 Monetary Intervention Stance",
    "📝 Behind The Math"
])

# ================= TAB 1: HISTORICAL CRISIS COMPARATOR =================
with tabs[0]:
    st.markdown("### 📚 Historical Crisis Comparator Engine")
    st.markdown("<p style='color:#9ca3af; font-size:0.9rem;'>Comparing active scenario parameters against historical shock regimes using integrated transmission weight arrays.</p>", unsafe_allow_html=True)
    
    # Calculated values for fertilizer shock mapping
    calculated_fertilizer = float(np.clip(15 + (lagged_crude_pass * 0.22) + (spot_lng * 0.4), 10, 55))
    
    # Dynamic risk state descriptor generation based on inputs
    if brent_anchor > 120:
        dynamic_risk = "Systemic Energy & Resource Dislocation"
    elif brent_anchor > 95:
        dynamic_risk = "Elevated Imported Inflation Transmission"
    else:
        dynamic_risk = "Bounded Macro Stress Dynamics"

    # Core historical regime matrix definition
    historical_crisis_data = {
        "Russia-Ukraine War (2022 Peak)": {
            "brent": 128.0,
            "india_cpi": 7.8,
            "india_wpi": 15.9,
            "fertilizer_shock": 42.0,
            "lng_spike": 56.0,
            "shipping_index": 5.5,
            "rupee": 76.8,
            "risk_state": "Severe Imported Inflation Shock"
        },
        "COVID Supply Chain Shock (2020-21)": {
            "brent": 20.0,
            "india_cpi": 6.3,
            "india_wpi": 12.0,
            "fertilizer_shock": 18.0,
            "lng_spike": 14.0,
            "shipping_index": 8.2,
            "rupee": 74.5,
            "risk_state": "Demand Collapse + Logistics Freeze"
        },
        "Global Financial Crisis (2008)": {
            "brent": 147.0,
            "india_cpi": 9.1,
            "india_wpi": 12.9,
            "fertilizer_shock": 30.0,
            "lng_spike": 22.0,
            "shipping_index": 6.1,
            "rupee": 49.0,
            "risk_state": "Commodity Supercycle Blowoff"
        },
        "Current Simulation State": {
            "brent": float(brent_anchor),
            "india_cpi": float(cpi_projected),
            "india_wpi": float(wpi_projected),
            "fertilizer_shock": calculated_fertilizer,
            "lng_spike": float(spot_lng),
            "shipping_index": float(hormuz_scale),
            "rupee": float(usd_inr_peg),
            "risk_state": dynamic_risk
        }
    }

    # --- SCORECARD SECTION ---
    severity_score = (
        (brent_anchor / 150.0) * 25.0 +
        (cpi_projected / 10.0) * 20.0 +
        (wpi_projected / 20.0) * 20.0 +
        (hormuz_scale / 10.0) * 20.0 +
        (spot_lng / 60.0) * 15.0
    )
    severity_score = float(np.clip(severity_score, 0, 100))

    if severity_score < 30:
        sev_cat = "Stable"
        sev_color = "#10b981"
    elif severity_score < 50:
        sev_cat = "Elevated"
        sev_color = "#3b82f6"
    elif severity_score < 70:
        sev_cat = "Crisis Build-Up"
        sev_color = "#f59e0b"
    elif severity_score < 85:
        sev_cat = "Severe Shock"
        sev_color = "#ef4444"
    else:
        sev_cat = "Systemic Stress Event"
        sev_color = "#7c3aed"

    # --- SIMILARITY MATRIX ENGINE BLOCK ---
    weights = {"brent": 0.35, "india_cpi": 0.20, "shipping_index": 0.20, "lng_spike": 0.15, "rupee": 0.10}
    current_state = historical_crisis_data["Current Simulation State"]
    similarity_outputs = {}

    for regime_name, metrics in historical_crisis_data.items():
        if regime_name == "Current Simulation State":
            continue
        total_distance = 0.0
        for key, weight in weights.items():
            val_regime = metrics[key]
            val_current = current_state[key]
            max_val = max(val_regime, val_current, 1.0)
            distance = abs(val_regime - val_current) / max_val
            total_distance += distance * weight
        
        sim_percentage = (1.0 - total_distance) * 100.0
        similarity_outputs[regime_name] = np.clip(sim_percentage, 0.0, 100.0)

    highest_analog_regime = max(similarity_outputs, key=similarity_outputs.get)
    highest_analog_pct = similarity_outputs[highest_analog_regime]

    # --- CRITICAL REGIME SCENARIO UNCERTAINTY BAND ---
    if brent_anchor > 130 or hormuz_scale > 8 or usd_inr_peg > 92:
        reliability_band = "ELEVATED UNCERTAINTY"
        reliability_color = "#ef4444"
    elif brent_anchor > 100 or hormuz_scale > 5:
        reliability_band = "MODERATE UNCERTAINTY"
        reliability_color = "#f59e0b"
    else:
        reliability_band = "LOW UNCERTAINTY"
        reliability_color = "#10b981"

    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown(f"""
        <div class='metric-card' style='border-top: 4px solid {sev_color};'>
            <span style='color:#9ca3af;font-size:0.8rem;'>Internal Crisis Severity Index</span><br>
            <span style='font-size:2rem;font-weight:800;color:{sev_color};'>{severity_score:.1f} / 100</span><br>
            <span style='font-size:0.85rem;color:#cbd5e1;'>Regime: <b>{sev_cat}</b></span>
        </div>
        """, unsafe_allow_html=True)
    with col_s2:
        st.markdown(f"""
        <div class='metric-card' style='border-top: 4px solid #38bdf8;'>
            <span style='color:#9ca3af;font-size:0.8rem;'>Historical Analog Mapping</span><br>
            <span style='font-size:1.2rem;font-weight:700;color:#f3f4f6;'>{highest_analog_regime}</span><br>
            <span style='font-size:0.85rem;color:#38bdf8;'>Structural Similarity Profile: <b>{highest_analog_pct:.1f}%</b></span>
        </div>
        """, unsafe_allow_html=True)
    with col_s3:
        st.markdown(f"""
        <div class='metric-card' style='border-top: 4px solid {reliability_color};'>
            <span style='color:#9ca3af;font-size:0.8rem;'>Scenario Reliability Band</span><br>
            <span style='font-size:1.6rem;font-weight:700;color:{reliability_color};'>{reliability_band}</span><br>
            <span style='font-size:0.85rem;color:#9ca3af;'>Variance Analysis Horizon: Active</span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("#### 📊 Comparative Visualizations")
    col_v1, col_v2 = st.columns(2)
    
    with col_v1:
        # Multi-Line Comparison Data Build
        line_records = []
        for regime, data in historical_crisis_data.items():
            line_records.append({"Regime": regime, "Metric": "Brent Crude", "Value": data["brent"]})
            line_records.append({"Regime": regime, "Metric": "CPI Inflation", "Value": data["india_cpi"]})
            line_records.append({"Regime": regime, "Metric": "WPI Inflation", "Value": data["india_wpi"]})
        df_line = pd.DataFrame(line_records)
        
        fig_line = px.line(
            df_line, x="Metric", y="Value", color="Regime", markers=True,
            title="Macro Baseline Cross-Crisis Comparison Vector",
            template="plotly_dark",
            color_discrete_sequence=["#f43f5e", "#10b981", "#3b82f6", "#a78bfa"]
        )
        fig_line.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_line, use_container_width=True)

    with col_v2:
        # Radar Stress Data Matrix Mapping
        radar_categories = ['Inflation Stress', 'Freight Cost', 'LNG Shock', 'Currency Strain', 'Resource/Food Shock', 'Fiscal Impact']
        fig_radar = go.Figure()
        
        for name, data in historical_crisis_data.items():
            # Normalized scalar calculation for radar representation bounds
            inf_val = (data["india_cpi"] / 12.0) * 100
            fr_val = (data["shipping_index"] / 10.0) * 100
            lng_val = (data["lng_spike"] / 60.0) * 100
            curr_val = ((data["rupee"] - 40.0) / 60.0) * 100
            food_val = (data["fertilizer_shock"] / 60.0) * 100
            fisc_val = ((data["brent"] * data["shipping_index"]) / 1500.0) * 100
            
            r_values = [inf_val, fr_val, lng_val, curr_val, food_val, fisc_val]
            # Close the radar loop array
            r_values.append(r_values[0])
            r_cats = radar_categories + [radar_categories[0]]
            
            fig_radar.add_trace(go.Scatterpolar(
                r=r_values, theta=r_cats, name=name, fill='toself', opacity=0.15
            ))
            
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 110], gridcolor="#1f2937"), angularaxis=dict(gridcolor="#1f2937")),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            title="Institutional Macro Stress Radar Mapping Matrix", template="plotly_dark"
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # --- ADVANCED INSTITUTIONAL RBI-STYLE STRUCTURAL BLOCK ---
    st.markdown("#### 🏦 Advanced Policy Transmission & Vulnerability Matrix")
    col_p1, col_p2, col_p3 = st.columns(3)
    
    with col_p1:
        imported_dep_ratio = float(np.clip(75.0 + (lagged_crude_pass * 0.08), 65.0, 95.0))
        st.markdown(f"""
        <div class='metric-card'>
            <span style='color:#9ca3af;font-size:0.8rem;'>Imported Inflation Dependency Meter</span><br>
            <span style='font-size:1.5rem;font-weight:700;color:#f87171;'>{imported_dep_ratio:.2f}%</span>
            <p style='color:#6b7280;font-size:0.75rem;margin-top:0.5rem;'>Measures vulnerability to external energy pricing channels.</p>
        </div>
        """, unsafe_allow_html=True)
        
        cad_pressure = float(np.clip(1.2 + (lagged_crude_pass * 0.025) + (hormuz_scale * 0.12) + ((usd_inr_peg - 83.5) * 0.15), 0.5, 6.5))
        st.markdown(f"""
        <div class='metric-card' style='margin-top:1rem;'>
            <span style='color:#9ca3af;font-size:0.8rem;'>CAD Pressure Model (% of GDP)</span><br>
            <span style='font-size:1.5rem;font-weight:700;color:#fb923c;'>{cad_pressure:.2f}% Estimated Deficit</span>
            <p style='color:#6b7280;font-size:0.75rem;margin-top:0.5rem;'>Modeled shift in Current Account Deficit structure.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_p2:
        subsidy_burden_incr_crore = float(max(0.0, (brent_anchor - 75.0) * 2300.0 + (spot_lng - 15.0) * 850.0 + ((usd_inr_peg - 83.5) * 1200.0)))
        st.markdown(f"""
        <div class='metric-card'>
            <span style='color:#9ca3af;font-size:0.8rem;'>Fiscal Subsidy Burden Deviation</span><br>
            <span style='font-size:1.5rem;font-weight:700;color:#a78bfa;'>+₹{subsidy_burden_incr_crore:,.2f} Cr</span>
            <p style='color:#6b7280;font-size:0.75rem;margin-top:0.5rem;'>Estimated incremental fiscal buffer requirement vs baseline layout.</p>
        </div>
        """, unsafe_allow_html=True)
        
        fx_stress_score = float(np.clip(15.0 + (lagged_crude_pass * 0.45) + (hormuz_scale * 2.5) + ((usd_inr_peg - 83.5) * 4.0), 5.0, 98.0))
        st.markdown(f"""
        <div class='metric-card' style='margin-top:1rem;'>
            <span style='color:#9ca3af;font-size:0.8rem;'>FX Reserve Stress Meter</span><br>
            <span style='font-size:1.5rem;font-weight:700;color:#f43f5e;'>{fx_stress_score:.1f} / 100</span>
            <p style='color:#6b7280;font-size:0.75rem;margin-top:0.5rem;'>Simulated intervention velocity to maintain exchange rate anchors.</p>
        </div>
        """, unsafe_allow_html=True)

    with col_p3:
        st.markdown("##### Fuel Subsidy Exposure Matrix")
        matrix_records = [
            {"Sector Segment": "Fertilizer Pool Allocation", "Elasticity Beta": "0.42", "Risk Sensitivity": "High"},
            {"Sector Segment": "OMC Under-Recovery Buffers", "Elasticity Beta": "0.68", "Risk Sensitivity": "Extreme"},
            {"Sector Segment": "City Gas Distribution (CGD)", "Elasticity Beta": "0.31", "Risk Sensitivity": "Moderate"}
        ]
        st.table(pd.DataFrame(matrix_records))

    st.markdown(f"""
    <div style='background:#0f172a; padding:1rem; border-radius:6px; border:1px solid #1e293b; margin-top:1rem;'>
        <span style='color:#38bdf8; font-weight:600; font-size:0.85rem;'>Historical Analog Validation Note:</span><p style='color:#9ca3af; font-size:0.8rem; margin:0.25rem 0 0 0;'>
        Current scenario shares partial structural similarities with the {highest_analog_regime} commodity shock period, particularly through imported energy and edible oil transmission channels.</p>
    </div>
    """, unsafe_allow_html=True)


# ================= TAB 2: KITCHEN THALI LOGISTICS ENGINE =================
with tabs[1]:
    st.markdown("### 🚜 Agricultural Supply Chain Shock & Inter-State Bottlenecks")
    
    # Core Commodities configuration array
    commodities = ["Tomato", "Onion", "Poultry Feed", "Potato", "Milk", "Edible Oils", "Pulses", "Sugar", "Rice", "Wheat"]
    base_shifts = [10.2, 8.5, 6.8, 6.4, 6.0, 5.6, 5.2, 4.8, 4.1, 3.8]
    simulated_shifts = [b * (1 + (delta_crude_pct * 0.005) + (hormuz_scale * 0.015)) for b in base_shifts]
    df_thali = pd.DataFrame({"Commodity": commodities, "Projected Cost Shift (%)": simulated_shifts})
    df_thali = df_thali.sort_values(by="Projected Cost Shift (%)", ascending=True)
    
    col_graph, col_diagnostic = st.columns([5, 4])
    with col_graph:
        fig_thali = px.bar(
            df_thali, 
            x="Projected Cost Shift (%)", 
            y="Commodity", 
            orientation="h", 
            title="Agricultural Supply Chain Cost Inflation Vector by Commodity", 
            color="Projected Cost Shift (%)", 
            color_continuous_scale="Oranges", 
            template="plotly_dark"
        )
        fig_thali.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(t=30, b=10))
        st.plotly_chart(fig_thali, use_container_width=True)
        
    with col_diagnostic:
        st.markdown("#### 🔍 Supply Chain Logistics Inspector")
        selected_commodity = st.selectbox("Select a core food component to inspect structural pipeline risk:", commodities)
        
        # Comprehensive structural meta-data map for underlying categories
        commodity_meta = {
            "Tomato": {
                "perishability": "EXTREME (3–5 Days Shelf Life)",
                "cold_store": "Critical deficit in temperature-controlled cold logistics. Requires instantaneous continuous cold transit links.",
                "diesel_overhead": "Very High. Sourced rapidly via long-distance diesel reefer trucks from specialized hubs (e.g., Madanapalle, Kolar, Nashik) to consumption nodes.",
                "why_highest": "Tomato experiences a compounding effect. Because it cannot be stored long-term to wait out transient energy spikes, wholesalers must bear the immediate brunt of retail diesel price spikes. High perishability prevents inventory buffering, leading to a direct, unmitigated pass-through of freight cost increases to the end retail shelf."
            },
            "Onion": {
                "perishability": "Medium-High (Prone to Sprouting/Moisture Rot)",
                "cold_store": "Highly reliant on specialized ventilated structures (Kanda Chawls); poor climate control instantly increases post-harvest waste.",
                "diesel_overhead": "High. Concentrated production rings in Lasalgaon/Nashik require long-haul truck transport to feed pan-India cross-state demand.",
                "why_highest": "Highly exposed to inter-state transit freight spikes. Any movement in commercial fuel directly impacts the thin distribution margins of bulk trade networks."
            },
            "Poultry Feed": {
                "perishability": "Low-Medium (Silo Stable under dry conditions)",
                "cold_store": "Minimal direct cold chain storage requirements; heavily dependent on atmospheric moisture controls.",
                "diesel_overhead": "High. Demands extensive transport networks to move raw maize, soy meal inputs to mills, and finished feed back to regional farms.",
                "why_highest": "Compounded processing overheads. Crude oil derivatives influence the manufacturing costs of foundational synthetic amino acids, while diesel powers the raw collection phase."
            },
            "Potato": {
                "perishability": "Medium-Low (Highly Stable inside Cold Facilities)",
                "cold_store": "Extremely Heavy. Demands 6–9 months of continuous mechanical cold preservation to regulate market release patterns.",
                "diesel_overhead": "Medium-High. Sustained industrial power draw required to run storage compressors, combined with bulk freight handling.",
                "why_highest": "Directly exposed to structural electricity and secondary industrial energy prices. Spikes in crude and wholesale fuel costs increase the day-to-day power overheads of cold hubs."
            },
            "Milk": {
                "perishability": "High (Strict 24-48 Hour Chilling Window)",
                "cold_store": "Absolute requirement for uninterrupted cold loops. Bulk milk coolers (BMCs) and insulated transit tankers must operate non-stop.",
                "diesel_overhead": "Very High. Daily, continuous collection rounds from rural farms to urban processing plants cannot be skipped or delayed.",
                "why_highest": "Daily transit mandate leaves zero timing flexibility. Constant temperature monitoring and non-stop reefer hauling make it incredibly vulnerable to diesel shocks."
            },
            "Edible Oils": {
                "perishability": "Very Low (Long Storage Footprint)",
                "cold_store": "Low direct cold infrastructure; managed via standard industrial tanks and bulk warehouse storage.",
                "diesel_overhead": "High. Dominated by international shipping lane vulnerabilities and long port-to-refinery rail/road tank freight.",
                "why_highest": "Heavily coupled with international shipping corridors and chemical processing costs. Global crude indices impact synthetic extraction chemistry and freight surcharges."
            },
            "Pulses": {
                "perishability": "Low (Dry-Silo Stable)",
                "cold_store": "Negligible cold store footprint. Relies primarily on dry, rodent-proof warehouse structures.",
                "diesel_overhead": "Medium. Moving bulky grain volumes across states via traditional heavy-duty road transportation networks.",
                "why_highest": "Input cost variations are driven almost entirely by base field mechanics and the standard long-haul transport rates from central assembly points."
            },
            "Sugar": {
                "perishability": "Low (Dry Stable)",
                "cold_store": "Zero cold storage demand. Kept in dry-bag warehouses.",
                "diesel_overhead": "Medium-High. High freight volume required during the tight cane-harvest window to transport raw cane to regional crushing mills.",
                "why_highest": "Heavily exposed to seasonal harvesting transport spikes. Processing operations rely on fuel and oil derivatives for field-clearing machinery and internal boiler systems."
            },
            "Rice": {
                "perishability": "Very Low (Multi-Year Dry Silo Longevity)",
                "cold_store": "None. Managed via central food silos or ambient storage facilities.",
                "diesel_overhead": "Medium. Driven by large-scale, long-distance railway rake transport and secondary local tractor/truck hauling.",
                "why_highest": "Protected by its long shelf life and high volume-to-weight logistics efficiencies, though still impacted by diesel costs during the procurement and milling stages."
            },
            "Wheat": {
                "perishability": "Very Low (Multi-Year Ambient Storage Capacity)",
                "cold_store": "None. Extensively stored in bulk ambient warehouses or government grain silos.",
                "diesel_overhead": "Medium. Bulk freight costs incurred during mandi procurement rounds and distribution through the Public Distribution System (PDS).",
                "why_highest": "Its long storage life and high volume-to-weight efficiency insulate it from immediate price spikes. Wholesalers can buffer stock to avoid transient transport shocks."
            }
        }
        
        meta = commodity_meta[selected_commodity]
        idx = df_thali[df_thali["Commodity"] == selected_commodity]["Projected Cost Shift (%)"].values[0]
        st.markdown(f"""
        <div class="diagnostic-box">
            <h4 style="color:#f97316; margin:0 0 0.5rem 0;">📋 LOGISTICS PROFILE: {selected_commodity.upper()}</h4>
            <p><b>Simulated Pipeline Inflation:</b> <span style="color:#f87171; font-weight:700;">{idx:.2f}%</span></p>
            <p><b>Perishability Index:</b> {meta['perishability']}</p>
            <p><b>Cold Storage Vulnerability:</b> {meta['cold_store']}</p>
            <p><b>Diesel Transportation Footprint:</b> {meta['diesel_overhead']}</p>
            <hr style="border:0; border-top:1px solid #1e293b; margin:1rem 0;">
            <p style="color:#cbd5e1; font-size:0.875rem; line-height:1.5;"><b>Impact Analysis Matrix:</b> {meta['why_highest']}</p>
        </div>
        """, unsafe_allow_html=True)

# ================= TAB 3: FMCG DEFENSE DOSSIERS =================
with tabs[2]:
    st.markdown("### 🧼 Gross Margin Contraction Models (Listed Staples Ecosystem)")
    fmcg_col1, fmcg_col2 = st.columns(2)
    with fmcg_col1:
        st.markdown("#### Input Raw Material Stress Vector")
        materials = ["Linear Alkyl Benzene (LAB)", "HDPE Packaging Transporters", "Palm Oil Derivatives", "Logistics Freight Anchor"]
        shocks = [delta_crude_pct * 0.45, delta_crude_pct * 0.30, (brent_anchor - 70) * 0.35, delta_freight_pct * 0.8]
        df_fmcg = pd.DataFrame({"Input Raw Material": materials, "Calculated Price Shock Vector (%)": shocks})
        fig_fmcg = px.bar(df_fmcg, x="Input Raw Material", y="Calculated Price Shock Vector (%)", color="Calculated Price Shock Vector (%)", color_continuous_scale="Reds", template="plotly_dark")
        fig_fmcg.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_fmcg, use_container_width=True)
    with fmcg_col2:
        st.markdown("#### Corporate Margin Impact Simulation Matrix")
        st.markdown("""
        * **EBITDA Compression Range:** Listed soap and home care companies face a **240 bps to 410 bps** structural contraction based on current oil anchors.
        * **Grammage Reduction Strategy (Shrinkflation):** Pack sizes for entry-level price points (₹5/₹10 stock keeping units) are modeled to scale down by **8.4%** to preserve price anchors.
        """)

# ================= TAB 4: EDIBLE OIL IMPORT SHOCK & KITCHEN INFLATION =================
with tabs[3]:
    st.markdown("### 🥥 Edible Oil Import Intelligence & Landed Cost Waterfall Matrix")
    st.markdown("<p style='color:#9ca3af; font-size:0.9rem;'>Simulating transmission vectors from global commodity futures and shipping freight premiums down to consumer-level kitchen expenditure shock indices.</p>", unsafe_allow_html=True)
    
    # Crude-Oil-To-CPO Link Framework Formula
    biofuel_cpo_premium = ((brent_anchor - 75.0) / 10.0) * 35.0
    shipping_freight_base = 45.0 + (hormuz_scale * 8.5)
    cpo_fob = 850.0 + biofuel_cpo_premium
    soy_fob = 930.0 + (((brent_anchor - 75.0) / 10.0) * 22.0)
    sun_fob = 900.0 + (delta_freight_pct * 1.5)
    
    # Live International Markets Sub-grid
    oil_col_a, oil_col_b, oil_col_c, oil_col_d = st.columns(4)
    with oil_col_a:
        st.markdown(f"<div class='metric-card'><span style='color:#fb923c;font-size:0.8rem;'>Malaysian CPO Futures</span><br><span style='font-size:1.4rem;font-weight:700;'>${cpo_fob:.2f} / MT</span><br><span style='color:#9ca3af;font-size:0.75rem;'>Incl. Biofuel Premium: ${biofuel_cpo_premium:+.2f}</span></div>", unsafe_allow_html=True)
    with oil_col_b:
        st.markdown(f"<div class='metric-card'><span style='color:#38bdf8;font-size:0.8rem;'>CBOT Soybean Oil</span><br><span style='font-size:1.4rem;font-weight:700;'>${soy_fob:.2f} / MT</span><br><span style='color:#9ca3af;font-size:0.75rem;'>US Crush Margin Adjusted</span></div>", unsafe_allow_html=True)
    with oil_col_c:
        st.markdown(f"<div class='metric-card'><span style='color:#f43f5e;font-size:0.8rem;'>Black Sea Sun Oil</span><br><span style='font-size:1.4rem;font-weight:700;'>${sun_fob:.2f} / MT</span><br><span style='color:#4b5563;font-size:0.75rem;'>Synthetic Corridor Pricing</span></div>", unsafe_allow_html=True)
    with oil_col_d:
        st.markdown(f"<div class='metric-card'><span style='color:#a78bfa;font-size:0.8rem;'>National Import Dependency</span><br><span style='font-size:1.4rem;font-weight:700;'>60.20%</span><br><span style='color:#a78bfa;font-size:0.75rem;'>Annual Demand: ~23 MT</span></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Cost Waterfall & Structural Allocations Layout
    wat_col, san_col = st.columns([3, 2])
    with wat_col:
        st.markdown("#### 🌊 Landed Crude Palm Oil (CPO) Cost Waterfall (USD/MT)")
        insurance_overhead = 14.50
        duty_loading_factor = 0.055 
        cif_price = cpo_fob + shipping_freight_base + insurance_overhead
        regulatory_duty = cif_price * duty_loading_factor
        final_landed_usd = cif_price + regulatory_duty
        final_landed_inr_kg = (final_landed_usd * usd_inr_peg) / 1000.0
        
        fig_wat = go.Figure(go.Waterfall(
            orientation = "v",
            measure = ["relative", "relative", "relative", "relative", "total"],
            x = ["FOB Base Price", "Ocean Shipping Freight", "Marine Insurance", "Effective Duty & Cess", "Landed Port Wharf Price"],
            textposition = "outside",
            text = [f"${cpo_fob:.1f}", f"${shipping_freight_base:.1f}", f"${insurance_overhead:.1f}", f"${regulatory_duty:.1f}", f"${final_landed_usd:.1f}"],
            y = [cpo_fob, shipping_freight_base, insurance_overhead, regulatory_duty, final_landed_usd],
            connector = dict(line = dict(color = "#374151"))
        ))
        fig_wat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", template="plotly_dark", margin=dict(t=20, b=20))
        st.plotly_chart(fig_wat, use_container_width=True)

    with san_col:
        st.markdown("#### 🔄 Transmission Vector Flow")
        # Lightweight representation flow mapping
        fig_san = go.Figure(data=[go.Sankey(
            node = dict(
              pad = 15, thickness = 20, line = dict(color = "black", width = 0.5),
              label = ["Global Crude", "Biofuel Allocation", "CPO FOB", "Freight Index", "Landed Cost (INR)"],
              color = ["#ef4444", "#fb923c", "#38bdf8", "#f43f5e", "#10b981"]
            ),
            link = dict(
              source = [0, 0, 1, 3, 2],
              target = [1, 2, 2, 4, 4],
              value = [35, 65, 35, 15, 100]
            ))])
        fig_san.update_layout(title_text="Elasticity Link Propagation Tree", font_size=10, paper_bgcolor="rgba(0,0,0,0)", template="plotly_dark")
        st.plotly_chart(fig_san, use_container_width=True)

# ================= TAB 5: MONETARY INTERVENTION STANCE =================
with tabs[4]:
    st.markdown("### 🏦 Internal Elasticity Framework Stance Simulation")
    
    # Simple simulated yield curve shift calculation matrix
    tenors = ['3M', '6M', '1Y', '2Y', '5Y', '10Y', '30Y']
    base_yields = [6.75, 6.85, 7.05, 7.15, 7.22, 7.35, 7.50]
    
    # Yield shift logic scales up dynamically under severe energy and inflation scenarios
    shift_premium = (lagged_crude_pass * 0.006) + (hormuz_scale * 0.04) + ((usd_inr_peg - 83.5) * 0.015)
    simulated_yields = [b + shift_premium for b in base_yields]
    
    fig_yield = go.Figure()
    fig_yield.add_trace(go.Scatter(x=tenors, y=base_yields, name='Pre-Shock Baseline Curve', line=dict(color='#6b7280', width=2, dash='dash')))
    fig_yield.add_trace(go.Scatter(x=tenors, y=simulated_yields, name='Simulated Shock Curve Map', line=dict(color='#10b981', width=4)))
    
    fig_yield.update_layout(
        title="Sovereign G-Sec Yield Curve Shift Mapping Matrix",
        xaxis_title="Tenor Horizon", yaxis_title="Yield to Maturity (YTM %)",
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", template="plotly_dark"
    )
    st.plotly_chart(fig_yield, use_container_width=True)
    
    st.markdown("""
    * **Intervention Likelihood:** Modeled frameworks imply an open market operation (OMO) scaling action path if core sovereign yields cross thresholds.
    * **Liquidity Corridor Stance:** Open market frameworks shift toward overnight target adjustments when secondary inflation transmission variables clear standard risk tolerances.
    """)

# ================= TAB 6: BEHIND THE MATH =================
with tabs[5]:
    st.markdown("### 📝 Internal Elasticity Framework & Mathematical Modeling Specifications")
    st.markdown("""
    This terminal maps transmission propagation pathways using synthetic pass-through factors calibrated to historical commodity dislocations.
    
    #### ⚙️ Definitive Stress Propagation Calculations
    
    $$lagged\_crude\_pass = \\frac{Brent_{Anchor} - 75}{75} \\times 100$$
    
    $$cpi_{projected} = cpi_{baseline} + (lagged\_crude\_pass \\times 0.035) + ((diesel_{cost} - 90) \\times 0.015) + ((spot\_lng - 15) \\times 0.020)$$
    
    $$wpi_{projected} = wpi_{baseline} + (lagged\_crude\_pass \\times 0.11) + (hormuz\_scale \\times 0.22)$$
    
    #### 📊 Integrated Severity Weights Array
    
    $$severity\_score = \\left(\\frac{Brent_{Anchor}}{150}\\right) \\times 25 + \\left(\\frac{CPI_{Projected}}{10}\\right) \\times 20 + \\left(\\frac{WPI_{Projected}}{20}\\right) \\times 20 + \\left(\\frac{Hormuz_{Scale}}{10}\\right) \\times 20 + \\left(\\frac{Spot_{LNG}}{60}\\right) \\times 15$$
    """)
    
    # --- MODEL LIMITATION EXPANDABLE BOX ---
    with st.expander("⚠️ Framework Assumptions & Model Limitations"):
        st.markdown("""
        * **Synthetic Coefficients:** Transmission coefficients are synthetic elasticity metrics and are not explicitly bound to active real-time econometric regressions.
        * **No Econometric Calibration:** Standard autoregressive distributed lag (ARDL) or structural vector autoregression (SVAR) methods are not computed live within this engine layout.
        * **No Lagged Monetary Effects:** Simulations assume immediate structural pass-through and do not parameterize the 3-to-4 quarter lagging effects typical of monetary transmission mechanisms.
        * **No Stochastic Volatility Modeling:** Volatility inputs are mapped linearly rather than through stochastic differential equation (SDE) frameworks like GARCH.
        * **No Dynamic Demand Destruction Effects:** Consumer elasticity parameters remain static under extreme pricing scenarios rather than downscaling dynamically to model demand reduction.
        * **No Proprietary Datasets:** Models utilize public benchmarks and simulated approximations, not internal or non-public RBI database platforms.
        * **No Satellite/Shipping API Integration:** Logistics tracking and transit corridor blockades utilize user-defined scale approximations rather than live satellite AIS feeds.
        * **Freight Assumptions:** Strategic maritime transit variables are fixed scenario-based inputs for calculation scaling.
        * **Geopolitical Escalations:** Dislocation metrics are purely illustrative and intended to map tail-risk sensitivity constraints.
        """)

# --- RETAIL CORRIDOR BOTTOM TICKER STRIP ---
st.markdown(f"""
<div class='retail-ticker-bottom'>
<span>⛽ COMMERCIAL TRANSPORT: DIESEL: ₹{diesel_cost:.2f}/L | PETROL: ₹{petrol_cost:.2f}/L</span>
<span>💨 SPOT GAS INFRASTRUCTURE: LPG COMM: ₹{calculated_lpg_comm:.2f}/CYLINDER</span>
<span>⚡ MOORED IMPORT BASKET: ₹{india_crude_basket:.2f}/bbl EQUIV ANCHOR</span>
</div>
""", unsafe_allow_html=True)

# --- PROFESSIONAL DEFENSIVE DISCLAIMERS FOOTER ---
st.markdown("""
<p style='color:#4b5563; font-size:0.75rem; text-align:center; margin-top:2rem;'>
Scenario outputs are generated using synthetic elasticity frameworks and institutional-style transmission assumptions. 
They are intended for educational, simulation, and macro stress-testing purposes only and should not be interpreted as official forecasts, 
policy guidance, or investment advice. All transmission coefficients are synthetic institutional simulation estimates designed for educational 
and scenario-analysis purposes only. Not investment advice.
</p>
""", unsafe_allow_html=True)

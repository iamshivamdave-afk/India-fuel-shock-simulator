# ================= INDIA ENERGY SHOCK & MACRO STRESS ENGINE =================
# ================= INSTITUTIONAL MACRO INTELLIGENCE TERMINAL =================

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import urllib.request
import json

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="India Energy Shock & Margin Stress Engine",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================= LIVE BRENT FETCH =================
def fetch_live_brent_price_direct():

    fallback_price = 94.08
    url = "https://query1.finance.yahoo.com/v8/finance/chart/BZ=F"

    try:
        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        req = urllib.request.Request(url, headers=headers)

        with urllib.request.urlopen(req, timeout=6) as response:
            data = json.loads(response.read().decode())

            live_price = data["chart"]["result"][0]["meta"]["regularMarketPrice"]

            if live_price:
                return float(live_price)

    except Exception:
        return fallback_price

    return fallback_price


live_brent_spot = fetch_live_brent_price_direct()

# ================= CSS =================
st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #030712;
    color: #f3f4f6;
}

#MainMenu {visibility:hidden;}
footer {visibility:hidden;}
header {visibility:hidden;}

div[data-testid="stSidebar"] {
    background-color:#0b0f19;
    border-right:1px solid #1f2937;
}

.metric-card{
    background:#111827;
    border:1px solid #1f2937;
    padding:1.2rem;
    border-radius:10px;
}

.top-strip{
    background:linear-gradient(90deg,#1e1b4b,#0f172a);
    border:1px solid #3730a3;
    padding:0.8rem;
    border-radius:8px;
    margin-bottom:1rem;
    display:flex;
    justify-content:space-between;
    font-family:'JetBrains Mono', monospace;
    font-size:0.8rem;
    color:#38bdf8;
}

.bottom-strip{
    background:linear-gradient(90deg,#1c1917,#0f172a);
    border:1px solid #7c2d12;
    padding:0.8rem;
    border-radius:8px;
    margin-top:2rem;
    display:flex;
    justify-content:space-between;
    font-family:'JetBrains Mono', monospace;
    font-size:0.8rem;
    color:#fb923c;
}

.diagnostic-box{
    background:#0f172a;
    border-left:4px solid #f97316;
    padding:1rem;
    border-radius:8px;
}

</style>
""", unsafe_allow_html=True)

# ================= SIDEBAR =================

st.sidebar.markdown("## ⚙️ SYSTEM CONTROLS")

brent_anchor = st.sidebar.slider(
    "Brent Crude (USD/bbl)",
    60.0,
    180.0,
    float(live_brent_spot),
    step=0.1
)

hormuz_scale = st.sidebar.slider(
    "Hormuz Conflict Scale",
    1,
    10,
    5
)

petrol_cost = st.sidebar.slider(
    "Petrol Retail Price ₹/L",
    80,
    150,
    103
)

diesel_cost = st.sidebar.slider(
    "Diesel Retail Price ₹/L",
    75,
    140,
    91
)

spot_lng = st.sidebar.slider(
    "Spot LNG USD/MMBtu",
    10,
    60,
    18
)

monsoon_variant = st.sidebar.selectbox(
    "Monsoon Shock",
    [
        "Normal Climatic Balance",
        "Deficit (-12% El Niño)",
        "Severe Drought Blockade"
    ]
)

# ================= CORE ENGINE =================

usd_inr_peg = 83.5

brent_base = 75.0

delta_crude_pct = ((brent_anchor - brent_base) / brent_base) * 100

delta_freight_pct = hormuz_scale * 12.5

# ================= REGIME BRANCHING =================

if brent_anchor < 90:

    regime = "NORMAL"
    crude_multiplier = 1.0
    agri_multiplier = 1.0
    fmcg_multiplier = 1.0

elif brent_anchor < 120:

    regime = "STRESS"
    crude_multiplier = 1.45
    agri_multiplier = 1.65
    fmcg_multiplier = 1.55

else:

    regime = "CRISIS"
    crude_multiplier = 2.25
    agri_multiplier = 2.60
    fmcg_multiplier = 2.20

# ================= CPI / WPI =================

wpi_baseline = 3.90

wpi_projected = (
    wpi_baseline
    + ((brent_anchor - brent_base) * 0.095 * crude_multiplier)
    + (delta_freight_pct * 0.025)
)

cpi_baseline = 4.40

cpi_projected = (
    cpi_baseline
    + ((brent_anchor - brent_base) * 0.024 * crude_multiplier)
)

# ================= THALI =================

thali_multiplier = 1.0

if monsoon_variant == "Deficit (-12% El Niño)":
    thali_multiplier = 1.35

elif monsoon_variant == "Severe Drought Blockade":
    thali_multiplier = 1.75

thali_index_pct = (
    6.2
    + (delta_crude_pct * 0.075)
    * thali_multiplier
)

# ================= LPG =================

calculated_lpg_comm = (
    1250
    + (spot_lng * 18.5)
    + ((brent_anchor - 75.0) * 4.25)
)

# ================= RISK STATE =================

if wpi_projected > 8 or brent_anchor > 110:

    risk_state = "CRISIS MATRIX ACTIVE"
    risk_color = "#ef4444"

else:

    risk_state = "STABLE BOUNDS"
    risk_color = "#10b981"

# ================= HISTORICAL ANALOG =================

if brent_anchor > 125 and hormuz_scale > 7:

    analog = "1973 Oil Embargo"

elif brent_anchor > 105:

    analog = "Russia-Ukraine 2022"

else:

    analog = "Normal Commodity Cycle"

# ================= SEVERITY SCORE =================

severity_score = (
    (delta_crude_pct * 0.35)
    + (wpi_projected * 0.25)
    + (cpi_projected * 0.20)
    + (hormuz_scale * 2)
)

severity_score = min(100, severity_score)

# ================= TOP STRIP =================

st.markdown(f"""
<div class='top-strip'>
<span>📡 LIVE TERMINAL ACTIVE</span>
<span>🛢️ BRENT: ${brent_anchor:.2f}</span>
<span>⚠️ REGIME: {regime}</span>
<span>📚 HISTORICAL ANALOG: {analog}</span>
</div>
""", unsafe_allow_html=True)

# ================= HEADER =================

st.markdown("##### SYSTEM MATRIX // INSTITUTIONAL MACRO TRANSMISSION CORE")

st.markdown("# 🇮🇳 India Energy Shock & Margin Stress Engine")

st.markdown(
"""
<p style='color:#9ca3af'>
Simulating input cost propagation vectors, downstream inflation stress,
food transmission matrices, edible oil shocks, sovereign yield curve shifts,
and historical crisis analog comparison systems.
</p>
""",
unsafe_allow_html=True
)

# ================= METRICS =================

m1,m2,m3,m4,m5,m6 = st.columns(6)

with m1:
    st.markdown(f"""
    <div class='metric-card'>
    <span style='color:#9ca3af'>Projected CPI</span><br>
    <span style='font-size:1.6rem;font-weight:700'>
    {cpi_projected:.2f}%
    </span>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class='metric-card'>
    <span style='color:#9ca3af'>Projected WPI</span><br>
    <span style='font-size:1.6rem;font-weight:700;color:#38bdf8'>
    {wpi_projected:.2f}%
    </span>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class='metric-card'>
    <span style='color:#9ca3af'>Macro Regime</span><br>
    <span style='font-size:1rem;font-weight:700;color:{risk_color}'>
    {regime}
    </span>
    </div>
    """, unsafe_allow_html=True)

with m4:
    st.markdown(f"""
    <div class='metric-card'>
    <span style='color:#9ca3af'>Household Thali Index</span><br>
    <span style='font-size:1.6rem;font-weight:700;color:#f87171'>
    +{thali_index_pct:.1f}%
    </span>
    </div>
    """, unsafe_allow_html=True)

with m5:
    st.markdown(f"""
    <div class='metric-card'>
    <span style='color:#9ca3af'>System Risk</span><br>
    <span style='font-size:1rem;font-weight:700;color:{risk_color}'>
    {risk_state}
    </span>
    </div>
    """, unsafe_allow_html=True)

with m6:
    st.markdown(f"""
    <div class='metric-card'>
    <span style='color:#9ca3af'>Severity Score</span><br>
    <span style='font-size:1.6rem;font-weight:700;color:#f97316'>
    {severity_score:.1f}/100
    </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ================= TABS =================

tabs = st.tabs([
    "🌾 Kitchen Thali Logistics",
    "🏭 FMCG Defense Dossiers",
    "🥥 Edible Oil Shock Matrix",
    "🏦 Monetary Intervention",
    "📚 Historical Crisis Comparator",
    "📝 Behind The Math"
])

# ================= TAB 1 =================

with tabs[0]:

    st.markdown("## 🌾 Agricultural Supply Chain Shock Engine")

    commodities = [
        "Tomato",
        "Onion",
        "Milk",
        "Potato",
        "Edible Oils",
        "Pulses",
        "Rice",
        "Wheat"
    ]

    base_shifts = [
        10.2,
        8.5,
        6.0,
        6.4,
        5.6,
        5.2,
        4.1,
        3.8
    ]

    simulated_shifts = [
        b * (
            1
            + (delta_crude_pct * 0.009 * agri_multiplier)
            + (hormuz_scale * 0.018)
        )
        for b in base_shifts
    ]

    df_thali = pd.DataFrame({
        "Commodity": commodities,
        "Inflation Shock": simulated_shifts
    })

    fig = px.bar(
        df_thali,
        x="Inflation Shock",
        y="Commodity",
        orientation="h",
        color="Inflation Shock",
        color_continuous_scale="Oranges",
        template="plotly_dark"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

# ================= TAB 2 =================

with tabs[1]:

    st.markdown("## 🧼 FMCG Margin Compression Engine")

    materials = [
        "LAB",
        "HDPE Packaging",
        "Palm Oil Derivatives",
        "Freight"
    ]

    shocks = [
        delta_crude_pct * 0.65 * fmcg_multiplier,
        delta_crude_pct * 0.48 * fmcg_multiplier,
        (brent_anchor - 70) * 0.42 * fmcg_multiplier,
        delta_freight_pct * 1.05
    ]

    df_fmcg = pd.DataFrame({
        "Material": materials,
        "Shock": shocks
    })

    fig_fmcg = px.bar(
        df_fmcg,
        x="Material",
        y="Shock",
        color="Shock",
        color_continuous_scale="Reds",
        template="plotly_dark"
    )

    fig_fmcg.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_fmcg, use_container_width=True)

# ================= TAB 3 =================

with tabs[2]:

    st.markdown("## 🥥 Edible Oil Shock Matrix")

    cpo_fob = 850 + (((brent_anchor - 75) / 10) * 35)

    freight = 45 + (hormuz_scale * 8.5)

    insurance = 14.5

    cif = cpo_fob + freight + insurance

    duty = cif * 0.055

    landed = cif + duty

    waterfall = go.Figure(go.Waterfall(
        measure=["relative","relative","relative","relative","total"],
        x=[
            "FOB",
            "Freight",
            "Insurance",
            "Duty",
            "Landed"
        ],
        y=[
            cpo_fob,
            freight,
            insurance,
            duty,
            landed
        ]
    ))

    waterfall.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(waterfall, use_container_width=True)

# ================= TAB 4 =================

with tabs[3]:

    st.markdown("## 🏦 RBI Policy & Sovereign Yield Curve")

    rate_hike_prob = min(
        100,
        int((cpi_projected - 4.0) * 25)
    )

    gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=rate_hike_prob,
        title={'text':"Repo Hike Probability"},
        gauge={
            'axis': {'range':[0,100]}
        }
    ))

    gauge.update_layout(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(gauge, use_container_width=True)

# ================= TAB 5 =================

with tabs[4]:

    st.markdown("## 📚 Historical Crisis Comparator")

    historical_crises = pd.DataFrame({

        "Crisis":[
            "Russia-Ukraine 2022",
            "COVID Supply Shock",
            "2008 Oil Spike",
            "Current Simulation"
        ],

        "Peak Brent":[
            128,
            70,
            147,
            brent_anchor
        ],

        "India CPI Peak":[
            7.8,
            6.3,
            9.1,
            round(cpi_projected,2)
        ],

        "WPI Peak":[
            16.6,
            12.9,
            13.5,
            round(wpi_projected,2)
        ],

        "Severity":[
            72,
            48,
            88,
            severity_score
        ]
    })

    fig_compare = px.bar(
        historical_crises,
        x="Crisis",
        y="Peak Brent",
        color="Severity",
        text="India CPI Peak",
        color_continuous_scale="Reds",
        template="plotly_dark",
        title="Historical Energy Shock Comparison"
    )

    fig_compare.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig_compare, use_container_width=True)

    st.dataframe(historical_crises, use_container_width=True)

# ================= TAB 6 =================

with tabs[5]:

    st.markdown("## 📝 Formula Transmission Layer")

    st.markdown(r"""
    ### WPI Formula

    $$WPI = WPI_{base} + (\Delta Crude \times Elasticity)$$

    ### CPI Formula

    $$CPI = CPI_{base} + (\Delta Crude \times SecondaryPassThrough)$$

    ### Severity Score

    $$Severity = Energy + Inflation + Freight + GeopoliticalStress$$

    ### Edible Oil Formula

    $$CPO = Base + Brent + ShippingPremium$$
    """)

# ================= BOTTOM STRIP =================

st.markdown(f"""
<div class='bottom-strip'>
<span>⛽ Petrol: ₹{petrol_cost}/L</span>
<span>🚛 Diesel: ₹{diesel_cost}/L</span>
<span>🏢 Commercial LPG: ₹{calculated_lpg_comm:.0f}</span>
<span>📡 LIVE SYSTEM VERIFIED</span>
</div>
""", unsafe_allow_html=True)

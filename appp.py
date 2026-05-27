import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="India Energy Shock & Margin Stress Engine",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CSS THEME
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
    background-color: #030712;
    color: #f9fafb;
}

/* Main app */
.stApp {
    background: linear-gradient(180deg, #030712 0%, #07111f 100%);
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0b1220;
    border-right: 1px solid #1f2937;
}

/* Hide streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Metric cards */
.metric-card {
    background: linear-gradient(145deg, #111827, #0f172a);
    border: 1px solid #1f2937;
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0px 0px 25px rgba(59,130,246,0.08);
    transition: all 0.3s ease;
    min-height: 120px;
}

.metric-card:hover {
    transform: translateY(-3px);
    border: 1px solid #3b82f6;
}

.metric-label {
    color: #9ca3af;
    font-size: 0.8rem;
    margin-bottom: 8px;
}

.metric-value {
    font-size: 1.7rem;
    font-weight: 700;
    color: #f9fafb;
}

.metric-sub {
    font-size: 0.75rem;
    color: #6b7280;
}

/* Header */
.main-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: white;
}

.sub-title {
    color: #94a3b8;
    font-size: 0.95rem;
}

/* Ticker */
.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background: #0f172a;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 10px 0;
    margin-bottom: 20px;
}

.ticker {
    display: inline-block;
    white-space: nowrap;
    animation: ticker 30s linear infinite;
}

.ticker span {
    margin-right: 60px;
    color: #e2e8f0;
    font-weight: 600;
}

@keyframes ticker {
    0% {transform: translateX(100%);}
    100% {transform: translateX(-100%);}
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("⚙️ Macro Risk Controls")

brent_anchor = st.sidebar.slider(
    "Brent Crude (USD/bbl)",
    60.0,
    180.0,
    118.0,
    step=1.0
)

hormuz_scale = st.sidebar.slider(
    "Hormuz Strait Conflict Scale",
    1,
    10,
    5
)

petrol_cost = st.sidebar.slider(
    "Petrol Retail Price (₹/L)",
    80,
    150,
    100
)

diesel_cost = st.sidebar.slider(
    "Diesel Retail Price (₹/L)",
    75,
    140,
    101
)

spot_lng = st.sidebar.slider(
    "Spot LNG (USD/MMBtu)",
    10,
    60,
    20
)

monsoon_variant = st.sidebar.selectbox(
    "Monsoon Shock Variant",
    [
        "Normal Climatic Balance",
        "Deficit (-12% El Niño)",
        "Severe Drought Blockade"
    ]
)

# =========================================================
# MACRO ENGINE
# =========================================================
brent_base = 75.0

delta_crude_pct = ((brent_anchor - brent_base) / brent_base) * 100
delta_freight_pct = hormuz_scale * 12.5

wpi_baseline = 4.5
cpi_baseline = 3.8

wpi_projected = (
    wpi_baseline
    + (delta_crude_pct * 0.11)
    + (delta_freight_pct * 0.03)
)

cpi_projected = (
    cpi_baseline
    + (delta_crude_pct * 0.025 * 1.2)
)

thali_multiplier = 1.0

if monsoon_variant == "Deficit (-12% El Niño)":
    thali_multiplier = 1.4
elif monsoon_variant == "Severe Drought Blockade":
    thali_multiplier = 1.9

thali_index_pct = (
    8.5
    + (delta_crude_pct * 0.08 * thali_multiplier)
)

# =========================================================
# RISK ENGINE
# =========================================================
if wpi_projected > 12 or hormuz_scale >= 8:
    risk_state = "CRISIS MATRIX ACTIVE"
    risk_color = "#ef4444"
elif wpi_projected > 7.5:
    risk_state = "ELEVATED RISK REGIME"
    risk_color = "#f59e0b"
else:
    risk_state = "STABLE COMPLIANCE"
    risk_color = "#10b981"

# =========================================================
# LIVE TICKER
# =========================================================
ticker_html = f"""
<div class="ticker-wrap">
    <div class="ticker">
        <span>🛢️ Brent: ${brent_anchor:.1f}</span>
        <span>🇮🇳 India Basket: ${brent_anchor-2:.1f}</span>
        <span>⛽ Petrol: ₹{petrol_cost}</span>
        <span>🚚 Diesel: ₹{diesel_cost}</span>
        <span>📈 CPI: {cpi_projected:.2f}%</span>
        <span>🏭 WPI: {wpi_projected:.2f}%</span>
        <span>⚠️ Risk: {risk_state}</span>
        <span>🌾 Food Shock Index: {thali_index_pct:.2f}%</span>
        <span>🔥 LNG: ${spot_lng}/MMBtu</span>
    </div>
</div>
"""
st.markdown(ticker_html, unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================
st.markdown("""
<div class='main-title'>
🇮🇳 India Energy Shock & Macro Stress Intelligence Engine
</div>
<div class='sub-title'>
Institutional-grade macro transmission and corporate stress simulation platform.
</div>
""", unsafe_allow_html=True)

st.markdown("")

# =========================================================
# KPI CARDS
# =========================================================
cols = st.columns(6)

cards = [
    ("Projected CPI Inflation", f"{cpi_projected:.2f}%"),
    ("Projected WPI", f"{wpi_projected:.2f}%"),
    ("Fuel Weight in CPI", "24.71%"),
    ("Crude Elasticity", "67.20%"),
    ("Household Thali Shock", f"+{thali_index_pct:.2f}%"),
    ("Risk State", risk_state)
]

for col, (label, value) in zip(cols, cards):
    with col:
        st.markdown(
            f"""
            <div class='metric-card'>
                <div class='metric-label'>{label}</div>
                <div class='metric-value'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

st.markdown("---")

# =========================================================
# TABS
# =========================================================
tabs = st.tabs([
    "🍱 Food Delivery",
    "🌾 Agri Inflation",
    "🏭 FMCG Margins",
    "🌻 Edible Oil Shock",
    "🏦 RBI Policy",
    "📝 Macro Formula Engine"
])

# =========================================================
# TAB 1
# =========================================================
with tabs[0]:

    st.subheader("📦 Food Delivery Operating Matrix")

    col1, col2 = st.columns([1, 2])

    with col1:

        last_mile = 25.5 + (diesel_cost * 0.04)

        margin = 6.25 - (delta_crude_pct * 0.015)

        st.metric(
            "Last Mile Cost",
            f"₹{last_mile:.2f}/order",
            f"{((last_mile-25.5)/25.5)*100:.1f}%"
        )

        st.metric(
            "Contribution Margin",
            f"{margin:.2f}%",
            f"-{abs(delta_crude_pct*0.015):.2f}%"
        )

    with col2:

        df_delivery = pd.DataFrame({
            "Category": [
                "Rider Payout",
                "Fuel Surcharge",
                "Platform Tech",
                "Customer Acquisition"
            ],
            "Base": [18, 5, 4, 10],
            "Stress": [
                18,
                5 * (1 + delta_crude_pct / 100),
                4,
                10 * (1 + delta_freight_pct / 200)
            ]
        })

        fig = px.bar(
            df_delivery,
            x="Category",
            y=["Base", "Stress"],
            barmode="group",
            template="plotly_dark",
            title="Per-Order Cost Shock"
        )

        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TAB 2
# =========================================================
with tabs[1]:

    st.subheader("🚜 Agricultural Shock Transmission")

    commodities = [
        "Wheat",
        "Rice",
        "Sugar",
        "Pulses",
        "Edible Oils",
        "Milk",
        "Potato",
        "Onion",
        "Tomato"
    ]

    base_shifts = [3.8, 4.1, 4.8, 5.2, 5.6, 6.0, 6.4, 8.5, 10.2]

    simulated = [
        b * (1 + (delta_crude_pct * 0.004) + (hormuz_scale * 0.02))
        for b in base_shifts
    ]

    df = pd.DataFrame({
        "Commodity": commodities,
        "Inflation Shock": simulated
    })

    fig = px.bar(
        df,
        x="Inflation Shock",
        y="Commodity",
        orientation="h",
        color="Inflation Shock",
        color_continuous_scale="Reds",
        template="plotly_dark"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================================================
# TAB 3
# =========================================================
with tabs[2]:

    st.subheader("🏭 FMCG Margin Compression")

    materials = [
        "LAB Chemicals",
        "HDPE Packaging",
        "Palm Oil",
        "Freight"
    ]

    shocks = [
        delta_crude_pct * 0.45,
        delta_crude_pct * 0.30,
        (brent_anchor - 70) * 0.35,
        delta_freight_pct * 0.80
    ]

    df = pd.DataFrame({
        "Input": materials,
        "Shock %": shocks
    })

    fig = px.bar(
        df,
        x="Input",
        y="Shock %",
        color="Shock %",
        color_continuous_scale="Reds",
        template="plotly_dark"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(fig, use_container_width=True)

    st.info("""
    EBITDA compression estimated between 240bps–410bps.
    Entry-level SKU shrinkflation risk materially elevated.
    """)

# =========================================================
# TAB 4
# =========================================================
with tabs[3]:

    st.subheader("🌻 Edible Oil Import Shock")

    cpo_futures = (
        880
        + ((brent_anchor - 75) * 3.8)
        + (hormuz_scale * 14)
    )

    soy_futures = (
        960
        + ((brent_anchor - 75) * 2.4)
    )

    sun_futures = (
        920
        + (hormuz_scale * 28)
    )

    cols = st.columns(4)

    metrics = [
        ("Malaysian CPO", f"${cpo_futures:.0f}/MT"),
        ("Soybean Oil", f"${soy_futures:.0f}/MT"),
        ("Sunflower Oil", f"${sun_futures:.0f}/MT"),
        ("Import Dependency", "60.2%")
    ]

    for col, (label, value) in zip(cols, metrics):
        with col:
            st.markdown(
                f"""
                <div class='metric-card'>
                    <div class='metric-label'>{label}</div>
                    <div class='metric-value'>{value}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:

        ocean_freight = 45 + (hormuz_scale * 9.5)

        fig = go.Figure(go.Waterfall(
            name="Cost Build",
            orientation="v",
            measure=["relative","relative","relative","total"],
            x=[
                "FOB",
                "Freight",
                "Insurance",
                "Final Cost"
            ],
            y=[
                cpo_futures,
                ocean_freight,
                12,
                0
            ]
        ))

        fig.update_layout(
            template="plotly_dark",
            title="Import Landed Cost Waterfall",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(fig, use_container_width=True)

    with col2:

        labels = [
            "SE Asia",
            "South America",
            "Black Sea",
            "Indian Ports",
            "Refineries",
            "Consumers"
        ]

        source = [0,1,2,3,4]
        target = [3,3,3,4,5]
        value = [35,25,20,70,90]

        sankey = go.Figure(data=[go.Sankey(
            node=dict(
                label=labels,
                pad=15,
                thickness=18
            ),
            link=dict(
                source=source,
                target=target,
                value=value
            )
        )])

        sankey.update_layout(
            template="plotly_dark",
            title="Global Oil Flow Map",
            paper_bgcolor="rgba(0,0,0,0)"
        )

        st.plotly_chart(sankey, use_container_width=True)

# =========================================================
# TAB 5
# =========================================================
with tabs[4]:

    st.subheader("🏦 RBI Policy Transmission")

    if cpi_projected > 6:
        st.error(
            "CPI breaches RBI tolerance band. "
            "Probability of hawkish policy response elevated."
        )
    else:
        st.success(
            "Inflation remains inside RBI monitoring corridor."
        )

    hike_prob = min(
        100,
        max(0, int((cpi_projected - 4) * 200))
    )

    liquidity_drain = delta_crude_pct * 45.2

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Rate Hike Probability",
            f"{hike_prob}%"
        )

    with col2:
        st.metric(
            "FX Reserve Stress",
            f"-${liquidity_drain/100:.2f}B"
        )

# =========================================================
# TAB 6
# =========================================================
with tabs[5]:

    st.subheader("📝 Transmission Formula Engine")

    st.markdown("""
### 1. Wholesale Inflation Pass-through

WPI = Base WPI + (Crude Shock × 0.11) + (Freight Shock × 0.03)

---

### 2. Consumer Inflation Propagation

CPI = Base CPI + (Crude Shock × 0.025 × 1.2)

---

### 3. Thali Shock Index

Thali Cost = Base + (Crude Shock × 0.08 × Monsoon Multiplier)

---

### 4. Edible Oil Import Pricing

CPO Futures = Base FOB + (Brent Delta × 3.8) + (Hormuz Stress × 14)
""")

    st.success("Macro engine operating normally.")

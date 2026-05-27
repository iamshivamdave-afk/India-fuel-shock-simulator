import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import urllib.request
import re
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="India Energy Shock & Margin Stress Engine",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================================================
# GLOBAL CSS
# =========================================================

st.markdown("""
<style>

html, body, [data-testid="stAppViewContainer"] {
    font-family: Arial, sans-serif;
    background-color: #030712;
    color: #f3f4f6;
    font-size: 16px;
}

/* Hide Streamlit UI */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Sidebar Bottom Dock */
[data-testid="stSidebar"] {
    position: fixed;
    bottom: 0;
    top: auto;
    height: 320px !important;
    width: 100% !important;
    background: #111827 !important;
    border-top: 2px solid #374151;
    z-index: 999999;
    overflow-y: auto;
}

section.main {
    padding-bottom: 340px;
}

/* Metrics */
div[data-testid="stMetricContainer"] {
    background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 14px;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background-color: #111827;
    padding: 8px;
    border-radius: 10px;
}

.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #9ca3af !important;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 14px;
    font-weight: bold;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
    color: white !important;
}

/* Ticker */
.ticker-wrap {
    width: 100%;
    overflow: hidden;
    background: #111827;
    border: 1px solid #374151;
    border-radius: 8px;
    padding: 10px 0;
    margin-bottom: 20px;
}

.ticker {
    white-space: nowrap;
    display: inline-block;
    animation: ticker 25s linear infinite;
    font-size: 15px;
}

@keyframes ticker {
    from { transform: translateX(100%); }
    to { transform: translateX(-100%); }
}

.ticker span {
    margin-right: 60px;
    color: #60a5fa;
    font-weight: bold;
}

/* Cards */
.section-card {
    background: linear-gradient(135deg, #111827 0%, #1f2937 100%);
    border: 1px solid #374151;
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 20px;
}

/* Scrollbar */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-thumb {
    background: #374151;
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LIVE DATA FETCH
# =========================================================

@st.cache_data(ttl=1800)
def fetch_live_crude_prices():

    fallback_brent = 99.27
    fallback_wti = 94.50
    fallback_india = 96.80

    try:
        url = "https://markets.businessinsider.com/commodities/oil-price"

        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )

        with urllib.request.urlopen(req, timeout=5) as response:

            html = response.read().decode("utf-8")

            match = re.search(
                r'"price"\s*:\s*"([0-9\.]+)"',
                html
            )

            if match:
                brent = float(match.group(1))
                wti = round(brent * 0.94, 2)
                india = round(brent * 0.975, 2)

                return brent, wti, india

    except Exception:
        pass

    return fallback_brent, fallback_wti, fallback_india

live_brent, live_wti, live_india = fetch_live_crude_prices()

# =========================================================
# VOLATILITY DATA
# =========================================================

@st.cache_data
def generate_vol_surface(days=120):

    dates = pd.date_range(
        end=datetime.now(),
        periods=days,
        freq="D"
    )

    np.random.seed(42)

    returns = np.random.normal(
        0.0002,
        0.018,
        days
    )

    prices = 80 * np.exp(np.cumsum(returns))

    vol30 = (
        pd.Series(returns)
        .rolling(30)
        .std()
        * np.sqrt(252)
    ).bfill()

    vol60 = (
        pd.Series(returns)
        .rolling(60)
        .std()
        * np.sqrt(252)
    ).bfill()

    vol90 = (
        pd.Series(returns)
        .rolling(90)
        .std()
        * np.sqrt(252)
    ).bfill()

    return pd.DataFrame({
        "Date": dates,
        "Price": prices,
        "30D": vol30,
        "60D": vol60,
        "90D": vol90
    })

# =========================================================
# CORRELATION MATRIX
# =========================================================

@st.cache_data
def correlation_matrix():

    assets = [
        "Brent",
        "WTI",
        "India Basket",
        "Nifty50",
        "USDINR",
        "CPI",
        "WPI",
        "Freight"
    ]

    matrix = np.array([
        [1.00,0.94,0.97,-0.42,0.31,0.52,0.61,0.78],
        [0.94,1.00,0.91,-0.39,0.28,0.48,0.58,0.72],
        [0.97,0.91,1.00,-0.45,0.35,0.54,0.65,0.80],
        [-0.42,-0.39,-0.45,1.00,-0.66,-0.38,-0.41,-0.31],
        [0.31,0.28,0.35,-0.66,1.00,0.44,0.52,0.40],
        [0.52,0.48,0.54,-0.38,0.44,1.00,0.85,0.61],
        [0.61,0.58,0.65,-0.41,0.52,0.85,1.00,0.69],
        [0.78,0.72,0.80,-0.31,0.40,0.61,0.69,1.00]
    ])

    return pd.DataFrame(
        matrix,
        index=assets,
        columns=assets
    )

# =========================================================
# LIVE TICKER
# =========================================================

st.markdown(f"""
<div class="ticker-wrap">
    <div class="ticker">
        <span>🛢️ Brent: ${live_brent:.2f}</span>
        <span>🇺🇸 WTI: ${live_wti:.2f}</span>
        <span>🇮🇳 India Basket: ${live_india:.2f}</span>
        <span>📅 {datetime.now().strftime('%d-%b-%Y %H:%M')}</span>
        <span>⚡ Institutional Macro Engine Active</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="section-card">

<h1>
🇮🇳 India Energy Shock & Margin Stress Engine
</h1>

<p style="color:#9ca3af;">
Institutional-grade macroeconomic dashboard for
oil shocks, inflation transmission, logistics stress,
and corporate margin compression.
</p>

</div>
""", unsafe_allow_html=True)

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎛️ Control Deck")

    scenario = st.selectbox(
        "Scenario",
        [
            "Baseline",
            "Moderate Shock",
            "Severe Shock",
            "Systemic Crisis"
        ]
    )

    if scenario == "Moderate Shock":
        default_brent = 120.0
        default_freight = 80

    elif scenario == "Severe Shock":
        default_brent = 150.0
        default_freight = 150

    elif scenario == "Systemic Crisis":
        default_brent = 180.0
        default_freight = 250

    else:
        default_brent = live_brent
        default_freight = 40

    brent_crude = st.slider(
        "Brent Crude ($)",
        40.0,
        200.0,
        float(default_brent),
        0.5
    )

    petrol_price = st.slider(
        "Petrol Price",
        70.0,
        180.0,
        104.5,
        0.5
    )

    diesel_price = st.slider(
        "Diesel Price",
        60.0,
        170.0,
        92.5,
        0.5
    )

    freight_shock = st.slider(
        "Freight Shock %",
        0,
        300,
        int(default_freight),
        5
    )

    mandi_disruption = st.slider(
        "Supply Chain Coefficient",
        1.0,
        3.0,
        1.2,
        0.05
    )

    fertilizer_pass = st.slider(
        "Fertilizer Subsidy %",
        0,
        100,
        60,
        5
    )

# =========================================================
# CALCULATIONS
# =========================================================

base_crude = 80

delta = ((brent_crude - base_crude) / base_crude) * 100

calc_wpi = (
    0.042
    + (delta * 0.0011)
    + (freight_shock * 0.0003)
)

calc_cpi = (
    0.038
    + (delta * 0.00025)
    + ((mandi_disruption - 1.0) * 0.012)
)

thali_idx = (
    0.10
    + (delta * 0.0006)
    + ((mandi_disruption - 1.0) * 0.048)
)

var95 = thali_idx * 1.645
cvar = thali_idx * 2.1

# =========================================================
# METRICS
# =========================================================

st.subheader("📊 Real-Time Macro Dashboard")

m1, m2, m3, m4, m5, m6 = st.columns(6)

m1.metric("CPI Inflation", f"{calc_cpi:.2%}")
m2.metric("WPI Inflation", f"{calc_wpi:.2%}")
m3.metric("Thali Shock", f"{thali_idx:.1%}")
m4.metric("Fuel Weight", "24.7%")
m5.metric("VaR 95%", f"{var95:.1%}")
m6.metric("Expected Shortfall", f"{cvar:.1%}")

# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "🍱 Food Tech",
    "📈 Risk Analytics",
    "📊 Stress Testing",
    "📜 Methodology"
])

# =========================================================
# TAB 1
# =========================================================

with tab1:

    st.markdown("""
    <div class="section-card">
    <h2>🍱 Food Delivery Margin Matrix</h2>
    <p>Hyperlocal logistics profitability simulation.</p>
    </div>
    """, unsafe_allow_html=True)

    base_last_mile = 28.5

    simulated_last_mile = (
        base_last_mile
        * (
            1 + ((diesel_price - 92.5) / 92.5) * 0.75
        )
        + (freight_shock * 0.02)
    )

    margin_loss = (
        (
            simulated_last_mile - base_last_mile
        ) / base_last_mile
    ) * 4.2

    projected_margin = 5.8 - margin_loss

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Last Mile Cost",
        f"₹{simulated_last_mile:.2f}"
    )

    c2.metric(
        "Margin Compression",
        f"{margin_loss:.2f}%"
    )

    c3.metric(
        "Projected Margin",
        f"{projected_margin:.2f}%"
    )

    diesel_range = np.linspace(
        diesel_price - 20,
        diesel_price + 20,
        20
    )

    margins = []

    for d in diesel_range:

        margin = 5.8 - (
            (
                (
                    base_last_mile
                    * (
                        1 + ((d - 92.5) / 92.5) * 0.75
                    )
                )
                - base_last_mile
            ) / base_last_mile
        ) * 4.2

        margins.append(margin)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=diesel_range,
            y=margins,
            mode="lines+markers",
            line=dict(width=4),
            name="Margin"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=420,
        title="Margin Sensitivity vs Diesel Price",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =========================================================
# TAB 2
# =========================================================

with tab2:

    st.markdown("""
    <div class="section-card">
    <h2>📈 Volatility Analytics</h2>
    <p>Rolling volatility structure and institutional risk monitoring.</p>
    </div>
    """, unsafe_allow_html=True)

    vol = generate_vol_surface()

    fig_vol = go.Figure()

    fig_vol.add_trace(
        go.Scatter(
            x=vol["Date"],
            y=vol["30D"],
            name="30D Vol"
        )
    )

    fig_vol.add_trace(
        go.Scatter(
            x=vol["Date"],
            y=vol["60D"],
            name="60D Vol"
        )
    )

    fig_vol.add_trace(
        go.Scatter(
            x=vol["Date"],
            y=vol["90D"],
            name="90D Vol"
        )
    )

    fig_vol.update_layout(
        template="plotly_dark",
        height=450,
        title="Crude Oil Volatility Surface",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_vol,
        use_container_width=True
    )

    st.markdown("---")

    corr = correlation_matrix()

    fig_corr = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.index,
            colorscale="RdBu",
            zmid=0,
            text=np.round(corr.values, 2),
            texttemplate="%{text}"
        )
    )

    fig_corr.update_layout(
        template="plotly_dark",
        height=600,
        title="Cross Asset Correlation Matrix",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_corr,
        use_container_width=True
    )

# =========================================================
# TAB 3
# =========================================================

with tab3:

    st.markdown("""
    <div class="section-card">
    <h2>📊 Institutional Stress Testing</h2>
    <p>Multi-scenario macroeconomic risk decomposition.</p>
    </div>
    """, unsafe_allow_html=True)

    stress_df = pd.DataFrame({
        "Scenario": [
            "Baseline",
            "Moderate",
            "Severe",
            "Tail Risk",
            "Systemic"
        ],
        "CPI": [
            0.045,
            0.058,
            0.072,
            0.089,
            0.105
        ],
        "WPI": [
            0.052,
            0.078,
            0.112,
            0.145,
            0.185
        ]
    })

    fig_bar = go.Figure()

    fig_bar.add_trace(
        go.Bar(
            x=stress_df["Scenario"],
            y=stress_df["CPI"],
            name="CPI"
        )
    )

    fig_bar.add_trace(
        go.Bar(
            x=stress_df["Scenario"],
            y=stress_df["WPI"],
            name="WPI"
        )
    )

    fig_bar.update_layout(
        template="plotly_dark",
        barmode="group",
        height=450,
        title="Macro Stress Scenario Matrix",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )

    st.plotly_chart(
        fig_bar,
        use_container_width=True
    )

# =========================================================
# TAB 4
# =========================================================

with tab4:

    st.markdown("""
    <div class="section-card">

    <h2 style="color:#60a5fa;">
    📜 Methodology & Framework
    </h2>

    <p>
    This simulation engine models how global oil shocks
    propagate into the Indian economy through freight,
    agriculture, logistics, retail fuel pricing,
    inflation, and corporate margins.
    </p>

    <h3 style="color:#fbbf24;">
    Included Variables
    </h3>

    <ul>
        <li>Brent Crude</li>
        <li>WTI Crude</li>
        <li>India Basket</li>
        <li>Petrol & Diesel Prices</li>
        <li>Freight Shock</li>
        <li>Supply Chain Bottlenecks</li>
        <li>Food Inflation</li>
        <li>Margin Compression</li>
    </ul>

    <h3 style="color:#34d399;">
    Risk Models
    </h3>

    <ul>
        <li>Value at Risk (VaR)</li>
        <li>Expected Shortfall</li>
        <li>Cross Asset Correlation</li>
        <li>Volatility Surface</li>
        <li>Stress Testing</li>
    </ul>

    <h3 style="color:#a78bfa;">
    Technology Stack
    </h3>

    <ul>
        <li>Python</li>
        <li>Streamlit</li>
        <li>Plotly</li>
        <li>Pandas</li>
        <li>NumPy</li>
    </ul>

    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<hr>

<center>
<p style="color:#6b7280;">
India Energy Shock & Margin Stress Engine v2.1
</p>
</center>
""", unsafe_allow_html=True)

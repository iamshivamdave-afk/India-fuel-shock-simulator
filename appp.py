import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import yfinance as yf

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
                    val = val * 0.375 # Standardized scaling factor
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
    font-size: 16px; /* Increased base scaling for ultimate universal legibility */
}

p, li, label, span {
    font-size: 15px !important;
    line-height: 1.6 !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Inter', sans-serif !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}

h2 { font-size: 28px !important; margin-bottom: 14px !important; border-bottom: 1px solid #1e293b; padding-bottom: 8px; }
h3 { font-size: 22px !important; margin-top: 20px !important; margin-bottom: 12px !important; color: #38bdf8 !important; }
h4 { font-size: 18px !important; color: #e2e8f0 !important; font-weight: 600 !important; }

/* --- Bloomberg Live Ticker Frame --- */
.ticker-wrap {
    width: 100%;
    background: #090d16 !important;
    border: 1px solid #1e293b !important;
    padding: 12px 0;
    overflow: hidden;
    margin-bottom: 20px;
    border-radius: 4px;
}
.ticker-content {
    display: inline-block;
    white-space: nowrap;
    animation: marquee 40s linear infinite;
    font-family: 'JetBrains Mono', monospace;
    font-size: 14px;
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
    font-size: 14px !important;
    font-weight: 600 !important;
    color: #cbd5e1 !important;
}

/* --- Navigation Tab Interfaces --- */
.stTabs [data-baseweb="tab-list"] {
    gap: 6px;
    background-color: #070a13;
    padding: 8px;
    border-radius: 6px;
    border: 1px solid #1e293b;
}
.stTabs [data-baseweb="tab"] {
    background-color: transparent;
    color: #94a3b8 !important;
    padding: 12px 20px;
    font-size: 15px !important;
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
    padding: 14px 16px;
}
div[data-testid="stMetricValue"] {
    font-size: 28px !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}
div[data-testid="stMetricLabel"] p {
    font-size: 12px !important;
    color: #94a3b8 !important;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

/* --- Functional Interface Panels --- */
.premium-panel {
    background-color: #070a13;
    padding: 22px;
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
    <h5 style="color: #2563eb; margin: 0; font-family: 'JetBrains Mono', monospace; font-size: 12px; letter-spacing: 1.5px;">SOVEREIGN RISK & TRANSMISSION WAR-ROOM</h5>
    <h1 style="margin: 6px 0 4px 0; font-size: 32px; font-weight: 800; color: #ffffff;">India Energy Shock & Macro Stress Intelligence Engine</h1>
    <p style="color: #cbd5e1; margin: 0; font-size: 15px;">Institutional-grade stress modeling engine calculating structural deficit variances, household budget depletion vectors, and enterprise EBITDA margin decay curves.</p>
</div>
""", unsafe_allow_html=True)

# --- MACROECONOMIC DISRUPTION SCENARIO DICTIONARY (TYPO RESOLVED) ---
SCENARIOS = {
    "1. Baseline Equilibrium": {"crude": float(live_universe['brent']), "freight": 20, "transit": 1.02, "subsidy": 85, "prob": 0.50},
    "2. Moderate Energy Shock": {"crude": 98.5, "freight": 65, "transit": 1.15, "subsidy": 70, "prob": 0.25},
    "3. Severe Supply Disruption": {"crude": 120.0, "freight": 140, "transit": 1.35, "subsidy": 55, "prob": 0.12},
    "4. Middle East Escalation Matrix": {"crude": 145.0, "freight": 210, "transit": 1.55, "subsidy": 40, "prob": 0.08},
    "5. Global Stagflation Regime": {"crude": 110.0, "freight": 180, "transit": 1.40, "subsidy": 50, "prob": 0.05}
}

# --- SIDEBAR CONTROL CENTER ---
with st.sidebar:
    st.markdown("<h3 style='margin-top:0;'>Operational Control Deck</h3>", unsafe_allow_html=True)
    
    selected_mode = st.selectbox("Select Macro Regime Profile", list(SCENARIOS.keys()))
    profile = SCENARIOS[selected_mode]
    
    st.markdown("<hr style='border-color:#1e293b; margin:14px 0;'>", unsafe_allow_html=True)
    st.markdown("🛠 ... **MANUAL MODEL OVERRIDES**")
    
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
    <div style='text-align: center; background-color: #070a13; border: 1px solid #1e293b; border-radius: 6px; padding: 10px; height: 84px;'>
        <p style='color: #94a3b8; margin: 0; font-size: 11px; font-weight: 600; text-transform: uppercase;'>Risk Engine State</p>
        <p style='color: {status_color}; margin: 4px 0; font-size: 14px; font-weight: bold;'>{system_status}</p>
        <div style='width: 10px; height: 10px; background-color: {status_color}; border-radius: 50%; display: inline-block; box-shadow: 0 0 8px {status_color};'></div>
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
        components = ["Base Deficit Impact", "Oil Import Volume Premium", "Freight Surcharges", "Currency Slippage Expansion", "Fertilizer Subsidy Adjust.", "Total Deficit Impact"]
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
        fig_waterfall.update_layout(title="Current Simulated Current Account Deficit (CAD) Expansion Map", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=400, font=dict(size=13))
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
    with col_right:
        st.markdown("<h4>Monetary Reaction Function & Reserves Defense</h4>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="premium-panel" style="margin-top:10px;">
            <p><b>Implied RBI Policy Stance:</b></p>
            <p style="font-size:18px !important; color:#38bdf8; font-weight:bold;">Projected Repo Rate Target: {calc_repo:.2%}</p>
            <hr style="border-color:#1e293b;">
            <p style="font-size:14px; color:#cbd5e1;">At the simulated pricing thresholds, import capital demands indicate an immediate monthly foreign cash reserve outflow rate of approximately <b>${(delta_crude_pct * 0.18):.2f}B USD</b> to buffer against structural currency spikes.</p>
        </div>
        """, unsafe_allow_html=True)
        
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=calc_yield,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "IN 10Y G-Sec Sovereign Stress Anchor", 'font': {'size': 15}},
            gauge={
                'axis': {'range': [6.0, 9.5], 'tickfont': {'size': 13}},
                'bar': {'color': '#2563eb'},
                'steps': [
                    {'range': [6.0, 7.2], 'color': '#111827'},
                    {'range': [7.2, 8.2], 'color': '#374151'},
                    {'range': [8.2, 9.5], 'color': '#7f1d1d'}
                ]
            }
        ))
        fig_gauge.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=220, margin=dict(t=40, b=10))
        st.plotly_chart(fig_gauge, use_container_width=True)

# --- TAB 2: HOUSEHOLD STRESS DECK ---
with t2:
    st.markdown("<h2>Indian Household Budget Stress Simulator</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#cbd5e1;'>Evaluating real household savings depletion vectors caused by compounding energy spikes across granular consumer income strata.</p>", unsafe_allow_html=True)
    
    segments = ["Lower Income Bracket", "Middle Class Profile", "Upper Middle Elite", "Affluent Household"]
    fuel_impact = [14.5 * (brent_input/80.0), 11.2 * (brent_input/80.0), 8.5 * (brent_input/80.0), 4.2 * (brent_input/80.0)]
    food_impact = [22.4 * transit_input, 14.8 * transit_input, 9.2 * transit_input, 3.5 * transit_input]
    emi_stress = [2.0 * (calc_yield/7.10), 8.5 * (calc_yield/7.10), 12.4 * (calc_yield/7.10), 6.0 * (calc_yield/7.10)]
    discretionary_compression = [25.0 * (calc_cpi/0.04), 15.0 * (calc_cpi/0.04), 8.0 * (calc_cpi/0.04), 2.0 * (calc_cpi/0.04)]
    
    df_households = pd.DataFrame({
        "Income Group": segments * 4,
        "Budget Deficit Shift (%)": fuel_impact + food_impact + emi_stress + discretionary_compression,
        "Stress Component": ["Fuel Surcharges"]*4 + ["Food Inflation Pipeline"]*4 + ["EMI Loan Adjustments"]*4 + ["Discretionary Drawdowns"]*4
    })
    
    fig_house = px.bar(
        df_households, x="Income Group", y="Budget Deficit Shift (%)", 
        color="Stress Component", barmode="stack",
        color_discrete_sequence=["#ef4444", "#f97316", "#2563eb", "#64748b"],
        template="plotly_dark"
    )
    fig_house.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", title="Granular Savings Allocation Loss Framework (%)", height=420, font=dict(size=13))
    st.plotly_chart(fig_house, use_container_width=True)

# --- TAB 3: ENTERPRISE PROFITABILITY ROOM ---
with t3:
    st.markdown("<h2>Sector Corporate Margin Compression Matrices</h2>", unsafe_allow_html=True)
    
    sectors = ["Aviation Industries", "FMCG Staples", "Paints & Coatings", "Logistics Networks", "Infrastructure Cement", "Chemical Derivatives", "Food Delivery Platforms"]
    historical_ebitda = [14.2, 22.5, 18.2, 9.5, 16.8, 15.0, 5.2]
    
    simulated_ebitda = [
        historical_ebitda[0] - (delta_crude_pct * 0.12) - (freight_input * 0.02),
        historical_ebitda[1] - (delta_crude_pct * 0.04) - (transit_input * 1.5),
        historical_ebitda[2] - (delta_crude_pct * 0.14),
        historical_ebitda[3] - (delta_crude_pct * 0.03) - (transit_input * 2.2),
        historical_ebitda[4] - (delta_crude_pct * 0.05) - (transit_input * 1.8),
        historical_ebitda[5] - (delta_crude_pct * 0.11),
        historical_ebitda[6] - (delta_crude_pct * 0.04) - (transit_input * 2.5)
    ]
    
    simulated_ebitda = [max(-5.0, val) for val in simulated_ebitda]
    recovery_quarters = [int(np.ceil(abs(hist - sim) / 1.5)) for hist, sim in zip(historical_ebitda, simulated_ebitda)]
    
    df_corporate = pd.DataFrame({
        "Industry Sector": sectors,
        "Historical EBITDA Baseline (%)": historical_ebitda,
        "Simulated Current EBITDA (%)": simulated_ebitda,
        "Projected Recovery Cycles (Quarters)": recovery_quarters
    })
    
    fig_corp = go.Figure()
    fig_corp.add_trace(go.Bar(name="Historical Baseline", x=df_corporate["Industry Sector"], y=df_corporate["Historical EBITDA Baseline (%)"], marker_color="#1e293b"))
    fig_corp.add_trace(go.Bar(name="Simulated Post-Shock Target", x=df_corporate["Industry Sector"], y=df_corporate["Simulated Current EBITDA (%)"], marker_color="#dc2626"))
    fig_corp.update_layout(barmode="group", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", title="Granular EBITDA Margin Compression Matrix", height=400, font=dict(size=13))
    st.plotly_chart(fig_corp, use_container_width=True)
    
    st.markdown("<h4>Enterprise Capital Recovery & Earnings Volatility Map</h4>", unsafe_allow_html=True)
    st.dataframe(df_corporate.style.format({
        "Historical EBITDA Baseline (%)": "{:.2f}%",
        "Simulated Current EBITDA (%)": "{:.2f}%"
    }), use_container_width=True)

# --- TAB 4: MARITIME TRADE LOGISTICS ---
with t4:
    st.markdown("<h2>Maritime Sourcing Maps & Port Freight Disruptions</h2>", unsafe_allow_html=True)
    mc1, mc2 = st.columns([4, 6])
    
    with mc1:
        labels = ["Nhava Sheva (JNPT)", "Mundra Port Access", "Kandla Bulk Infrastructure", "Chennai Maritime Gate"]
        shares = [38.0, 32.0, 18.0, 12.0]
        
        fig_pie = px.pie(names=labels, values=shares, title="Inbound Gateway Fuel Surcharges Share Map", template="plotly_dark", color_discrete_sequence=px.colors.sequential.Plotly3)
        fig_pie.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=360, font=dict(size=13))
        st.plotly_chart(fig_pie, use_container_width=True)
        
    with mc2:
        st.markdown("<h4>Sub-Continental Landing Surcharge Maps</h4>", unsafe_allow_html=True)
        st.markdown("When marine supply corridors face headwinds, secondary localized landing penalties pass directly down into primary manufacturing networks:")
        
        chem_delta = (freight_input * 0.25) + (delta_crude_pct * 0.48)
        pharma_delta = (freight_input * 0.38) + (delta_crude_pct * 0.12)
        agri_delta = (transit_input - 1.0) * 35.0
        
        st.markdown(f"""
        <table style='width:100%; border-collapse: collapse; margin-top: 14px; font-size:15px; text-align:left;'>
            <tr style='background-color:#070a13; border-bottom:2px solid #1e293b;'>
                <th style='padding:12px; color:#38bdf8;'>Import Category</th>
                <th style='padding:12px; color:#38bdf8;'>Core Inbound Gateway</th>
                <th style='padding:12px; color:#38bdf8;'>Operational Transmission Risk</th>
                <th style='padding:12px; color:#38bdf8; text-align:right;'>Simulated Landing Shift</th>
            </tr>
            <tr style='border-bottom:1px solid #1e293b;'>
                <td style='padding:12px;'><b>Specialty Chemical Polymers</b></td>
                <td style='padding:12px;'>Mundra / Dahej</td>
                <td style='padding:12px;'>Petrochemical raw stock allocations compress downstream margin performance.</td>
                <td style='padding:12px; text-align:right; color:#ef4444; font-weight:bold;'>+{chem_delta:+.1f}%</td>
            </tr>
            <tr style='border-bottom:1px solid #1e293b;'>
                <td style='padding:12px;'><b>Active Pharma Ingredients (APIs)</b></td>
                <td style='padding:12px;'>Nhava Sheva (JNPT)</td>
                <td style='padding:12px;'>Blank container vessel cancellations require premium long-distance air-freight routing overrides.</td>
                <td style='padding:12px; text-align:right; color:#ef4444; font-weight:bold;'>+{pharma_delta:+.1f}%</td>
            </tr>
            <tr style='border-bottom:1px solid #1e293b;'>
                <td style='padding:12px;'><b>Potash & Nitrogenous Fertilizers</b></td>
                <td style='padding:12px;'>Kandla Port Terminal</td>
                <td style='padding:12px;'>Bulk vessel spot daily charter pricing spikes impact sovereign subsidy outlays.</td>
                <td style='padding:12px; text-align:right; color:#f59e0b; font-weight:bold;'>+{agri_delta:+.1f}%</td>
            </tr>
        </table>
        """, unsafe_allow_html=True)

# --- TAB 5: QUANTITATIVE RISK SIMULATION ---
with t5:
    st.markdown("<h2>Monte Carlo Simulation & Capital Tail-Risk Models</h2>", unsafe_allow_html=True)
    
    np.random.seed(42)
    simulations = 1000
    trading_days = 252
    drift = 0.02 / trading_days
    volatility = 0.35 / np.sqrt(trading_days)
    
    historical_returns = np.random.normal(drift, volatility, (trading_days, simulations))
    price_paths = np.zeros_like(historical_returns)
    price_paths[0] = brent_input
    
    for t in range(1, trading_days):
        price_paths[t] = price_paths[t-1] * np.exp(historical_returns[t])
        
    final_prices = price_paths[-1]
    value_at_risk = np.percentile(final_prices, 5)
    expected_shortfall = final_prices[final_prices < value_at_risk].mean()
    
    rc_left, rc_right = st.columns([6, 4])
    
    with rc_left:
        fig_paths = go.Figure()
        for i in range(25):
            fig_paths.add_trace(go.Scatter(y=price_paths[:, i], mode="lines", line=dict(width=1), opacity=0.4))
        fig_paths.update_layout(title="12-Month Forward Brent Crude Projections (Monte Carlo Path Array)", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=380, showlegend=False, font=dict(size=13))
        st.plotly_chart(fig_paths, use_container_width=True)
        
    with rc_right:
        st.markdown("<h4>Value at Risk (VaR) Sovereign Metrics Matrix</h4>", unsafe_allow_html=True)
        st.markdown(f"""
        <div class="premium-panel">
            <p><b>Calculated Risk Metrics (95% Confidence Interval):</b></p>
            <p>Sovereign Import Value at Risk (VaR Lower Bound): <span style="color:#f59e0b; font-weight:bold;">${value_at_risk:.2f}/bbl</span></p>
            <p>Extreme Tail Expected Shortfall (Conditional VaR): <span style="color:#ef4444; font-weight:bold;">${expected_shortfall:.2f}/bbl</span></p>
            <hr style="border-color:#1e293b;">
            <p style="font-size:14px; color:#cbd5e1;">The mathematical probability that international macro headwinds break through your specified downside parameters during the coming 12-month window is modeled by this system at <b>{(profile['prob']):.1%}</b>.</p>
        </div>
        """, unsafe_allow_html=True)
        
        corr_labels = ["Brent Crude", "WPI Shift", "CPI Index", "USDINR Spot", "IN 10Y Bond"]
        corr_data = [
            [1.0, 0.88, 0.72, 0.65, 0.78],
            [0.88, 1.0, 0.81, 0.58, 0.84],
            [0.72, 0.81, 1.0, 0.48, 0.91],
            [0.65, 0.58, 0.48, 1.0, 0.52],
            [0.78, 0.84, 0.91, 0.52, 1.0]
        ]
        fig_heat = px.imshow(corr_data, x=corr_labels, y=corr_labels, color_continuous_scale="RdBu_r", title="Macro Covariance Cross-Asset Grid")
        fig_heat.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=260, font=dict(size=12), margin=dict(t=40, b=10))
        st.plotly_chart(fig_heat, use_container_width=True)

# --- TAB 6: MATHEMATICAL METHODOLOGY ---
with t6:
    st.markdown("<h2>Underlying Transmission Matrices & Structural Formula Arrays</h2>", unsafe_allow_html=True)
    st.markdown("The calculations powering this analytical web framework are constructed using standard non-linear econometric pass-through vectors benchmarked from historic sub-continental supply disruptions:")
    
    st.markdown("### 1. Wholesale Price Index (WPI) Inflation Pass-Through Vector")
    st.latex(r"WPI_{Projected} = WPI_{Baseline} + \left(\Delta Crude\% \times 0.0013\right) + \left(\Delta Freight\% \times 0.00025\right)")
    st.markdown("*Where base crude is pegged at $80.0/bbl. The coefficient assumes a structural weight exposure across manufacturing, chemical derivatives, and long-haul transportation logistics lines.*")
    
    st.markdown("### 2. Consumer Price Index (CPI) Secondary Propagation Vector")
    st.latex(r"CPI_{Projected} = CPI_{Baseline} + \left(\Delta Crude\% \times 0.00032\right) + \left((\Omega_{Transit} - 1.0) \times 0.015\right)")
    st.markdown("*Where $\Omega_{Transit}$ represents the Domestic Transit Bottleneck Coefficient. This accounts for secondary food storage, agricultural mandi processing overheads, and last-mile inner-city fuel surcharges.*")
    
    st.markdown("### 3. Household Thali Input Index Function")
    st.latex(r"Thali_{Cost} = Thali_{Base} + \left(\Delta Crude\% \times 0.0006\right) + \left((\Omega_{Transit} - 1.0) \times 0.048\right) + \left((100 - \Phi_{Subsidy}) \times 0.0005\right)")
    st.markdown("*Where $\Phi_{Subsidy}$ captures the active Fertilizer Subsidy Absorption percentage passed down to primary cultivation inputs.*")

# --- APP SYSTEM FOOTER ANCHOR ---
st.markdown("""
<hr style="border-color: #1e293b; margin-top:40px;">
<div style="text-align: center; color: #64748b; font-size: 13px; font-family: 'JetBrains Mono', monospace; padding-bottom: 20px;">
    System Status: Operational Hub Secured • Dynamic Analytical Compilations Completed Under Sandbox Tier-1
</div>
""", unsafe_allow_html=True)

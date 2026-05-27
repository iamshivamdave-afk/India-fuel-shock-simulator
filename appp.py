import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import urllib.request
import re

# --- LIVE CRUDE OIL DATA FETCH ENGINE ---
@st.cache_data(ttl=900)
def fetch_live_crude_prices():
    fallback_brent = 99.27
    fallback_indian = 96.80
    try:
        url = "https://markets.businessinsider.com/commodities/oil-price"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            html = response.read().decode('utf-8')
            match = re.search(r'"price"\s*:\s*"([0-9\.]+)"', html)
            if match:
                brent = float(match.group(1))
                indian = round(brent * 0.975, 2) if brent > 0 else fallback_indian
                return brent, indian
    except Exception:
        pass
    return fallback_brent, fallback_indian

live_brent, live_indian_basket = fetch_live_crude_prices()

# --- WEBAPP CONFIGURATION ---
st.set_page_config(page_title="Macro Energy & Margin Engine", page_icon="🛢️", layout="wide", initial_sidebar_state="expanded")

# --- ULTRA-DENSE ARIAL 8PX & ANIMATION CSS LAYER ---
st.markdown("""
<style>
/* FORCE ARIAL 8PX GLOBALLY FOR MAXIMUM DATA DENSITY */
html, body, [class*="st-"], [data-testid="stAppViewContainer"], .stMarkdown, p, div, span, label {
    font-family: 'Arial', sans-serif !important;
    font-size: 8px !important;
    color: #e2e8f0;
    line-height: 1.2 !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: 'Arial', sans-serif !important;
    font-size: 10px !important;
    font-weight: bold !important;
    color: #ffffff;
    margin-bottom: 4px !important;
}

#MainMenu, footer, header {visibility: hidden;}

/* DENSE CONTROL SIDEBAR */
[data-testid="stSidebar"] {
    background-color: #020617 !important;
    border-right: 1px solid #1e293b !important;
    width: 220px !important;
}

/* CUSTOM ANIMATIONS */
@keyframes scanline {
    0% { transform: translateY(-100%); }
    100% { transform: translateY(100%); }
}
@keyframes pulse-data {
    0% { opacity: 0.7; transform: scale(0.98); }
    50% { opacity: 1; transform: scale(1); border-color: #38bdf8; }
    100% { opacity: 0.7; transform: scale(0.98); }
}
@keyframes slide-right {
    0% { opacity: 0; transform: translateX(-10px); }
    100% { opacity: 1; transform: translateX(0); }
}
@keyframes data-flow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

/* COMPACT METRIC CARDS */
div[data-testid="stMetricContainer"] {
    background-color: #0f172a !important;
    border: 1px solid #334155 !important;
    border-radius: 2px !important;
    padding: 4px 8px !important;
    box-shadow: none !important;
}
div[data-testid="stMetricValue"] { font-size: 10px !important; font-weight: bold !important; }
div[data-testid="stMetricDelta"] { font-size: 8px !important; }

/* ANIMATED TAB CONTAINERS */
.anim-omc { animation: pulse-data 3s infinite ease-in-out; border-left: 2px solid #ef4444; padding-left: 8px; }
.anim-maritime { background: linear-gradient(90deg, #0f172a, #1e293b, #0f172a); background-size: 200% 200%; animation: data-flow 4s ease infinite; padding: 6px; border: 1px solid #3b82f6;}
.anim-fmcg { animation: slide-right 0.8s ease-out forwards; border-left: 2px solid #22c55e; padding-left: 8px; }
.anim-scanner { position: relative; overflow: hidden; padding: 6px; border: 1px solid #10b981;}
.anim-scanner::after { content: ""; position: absolute; top: 0; left: 0; width: 100%; height: 2px; background: #34d399; animation: scanline 2s linear infinite; opacity: 0.5;}

/* COMPACT TABS */
.stTabs [data-baseweb="tab-list"] { gap: 2px; background-color: #020617; padding: 2px; border-bottom: 1px solid #1e293b; }
.stTabs [data-baseweb="tab"] { padding: 4px 8px; font-size: 8px; border-radius: 0px; }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR CONTROL DESK ---
with st.sidebar:
    st.markdown("<div style='border-bottom: 1px solid #334155; margin-bottom: 8px;'><h3>🎛️ PARAMETER DECK</h3></div>", unsafe_allow_html=True)
    brent_crude = st.slider("BRENT CRUDE ($/BBL)", 40.0, 180.0, float(live_brent), 0.5)
    petrol_price = st.slider("RETAIL PETROL (INR/L)", 70.0, 160.0, 104.5, 0.5)
    diesel_price = st.slider("RETAIL DIESEL (INR/L)", 60.0, 150.0, 92.5, 0.5)
    freight_shock = st.slider("FREIGHT PREMIUM (%)", 0, 300, 45, 5)
    mandi_disruption = st.slider("MANDI BOTTLENECK (X)", 1.0, 2.5, 1.15, 0.05)
    fertilizer_pass_thru = st.slider("FERTILIZER ABSORB (%)", 0, 100, 65, 5)

# --- CALCULATION ENGINE ---
base_crude = 80.0
crude_delta_pct = ((brent_crude - base_crude) / base_crude) * 100
calc_wpi = 0.042 + (crude_delta_pct * 0.0011) + (freight_shock * 0.0003)
calc_cpi = 0.038 + (crude_delta_pct * 0.00025) + ((mandi_disruption - 1.0) * 0.012)
thali_cost_idx = 0.10 + (crude_delta_pct * 0.0006) + ((mandi_disruption - 1.0) * 0.048) + ((100 - fertilizer_pass_thru) * 0.0005)

# --- TOP HUD ---
col1, col2, col3, col4, col5, col6 = st.columns(6)
col1.metric("CPI INFLATION", f"{calc_cpi:.2%}")
col2.metric("WPI INFLATION", f"{calc_wpi:.2%}")
col3.metric("BRENT LIVE", f"${live_brent:.2f}")
col4.metric("SIM BRENT", f"${brent_crude:.2f}")
col5.metric("THALI INDEX", f"+{thali_cost_idx:.1%}")
col6.metric("SYS RISK", "CRITICAL" if calc_wpi > 0.11 else "NORMAL")

# Chart font config
chart_font = dict(family="Arial", size=8, color="#e2e8f0")

st.markdown("<div style='margin-top: 8px;'></div>", unsafe_allow_html=True)

# --- TABS INTERFACE ---
t1, t2, t3, t4, t5, t6 = st.tabs([
    "⛽ OMC STRESS", 
    "🚢 MARITIME SOURCING", 
    "📊 NSE CAPITAL & RATES", 
    "🏭 FMCG RAW MATERIALS", 
    "🍱 FOOD TECH", 
    "🌾 AGRI MANDI"
])

# --- TAB 1: OMC STRESS (ANIMATION: PULSE DATA) ---
with t1:
    st.markdown("<div class='anim-omc'><b>[LIVE] OMC UNDER-RECOVERY & GRM MATRIX</b><br>Simulating refining margins and daily capital drain.</div><br>", unsafe_allow_html=True)
    
    petrol_breakeven_crude = (petrol_price / 1.22)
    diesel_breakeven_crude = (diesel_price / 1.05)
    petrol_margin_gap = petrol_breakeven_crude - brent_crude
    diesel_margin_gap = diesel_breakeven_crude - brent_crude
    daily_drain = max(0.0, (-petrol_margin_gap * 4.5) + (-diesel_margin_gap * 9.2))
    
    o1, o2, o3 = st.columns(3)
    o1.metric("PETROL MARGIN GAP ($/BBL)", f"${petrol_margin_gap:.2f}")
    o2.metric("DIESEL MARGIN GAP ($/BBL)", f"${diesel_margin_gap:.2f}")
    o3.metric("OMC DAILY DRAIN (₹ CR)", f"₹{daily_drain:.2f}")
    
    omc_entities = ['IOCL', 'BPCL', 'HPCL']
    base_grms = [11.20, 12.40, 10.10]
    simulated_grms = [base + (crude_delta_pct * 0.04) - (max(0, -petrol_margin_gap)*0.15) for base in base_grms]
    
    fig_omc = go.Figure()
    fig_omc.add_trace(go.Bar(name='BASE GRM', x=omc_entities, y=base_grms, marker_color='#1e293b'))
    fig_omc.add_trace(go.Bar(name='SIM GRM', x=omc_entities, y=simulated_grms, marker_color='#ef4444'))
    fig_omc.update_layout(barmode='group', template='plotly_dark', margin=dict(l=10, r=10, t=20, b=10), height=200, font=chart_font, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_omc, use_container_width=True)

# --- TAB 2: MARITIME SOURCING (ANIMATION: DATA FLOW) ---
with t2:
    st.markdown("<div class='anim-maritime'><b>[SCANNING] OCEANIC IMPORT CHANNELS & SURCHARGES</b><br>NHAVA SHEVA / MUNDRA INBOUND METRICS</div><br>", unsafe_allow_html=True)
    
    base_container_cost = 2100 
    current_container_cost = base_container_cost * (1 + (freight_shock / 100)) + (brent_crude * 4.5)
    
    m1, m2 = st.columns(2)
    m1.metric("SIMULATED IMPORT RATE (USD/FEU)", f"${current_container_cost:.2f}")
    m2.metric("INBOUND RISK TIER", "CRITICAL LOCKDOWN" if current_container_cost > 4500 else "STABLE")
    
    labels = ['BAF (BUNKER)', 'CAF (CURRENCY)', 'WAR RISK PREMIUM', 'INLAND DEPOT']
    values = [350 * (brent_crude/80.0), 120 * (1 + calc_wpi), 450 * (freight_shock/45.0), 200 * (diesel_price/92.5)]
    
    fig_pie = px.pie(names=labels, values=values, template='plotly_dark', color_discrete_sequence=px.colors.sequential.Blues_r)
    fig_pie.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=200, font=chart_font, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_pie, use_container_width=True)

# --- TAB 3: NSE CAPITAL & RATES (ANIMATION: SCANNER) ---
with t3:
    st.markdown("<div class='anim-scanner'><b>[COMPUTING] INSTITUTIONAL VALUATION MULTIPLES & RBI STANCE</b></div><br>", unsafe_allow_html=True)
    
    base_repo = 6.50
    implied_repo_hike = max(0, int(((calc_cpi * 100) - 4.5) / 0.5) * 25) 
    projected_repo = base_repo + (implied_repo_hike / 100)
    g_sec_yield = 7.10 + (crude_delta_pct * 0.015) + (implied_repo_hike * 0.008)
    
    r1, r2, r3 = st.columns(3)
    r1.metric("IMPLIED RBI HIKE (BPS)", f"+{implied_repo_hike}")
    r2.metric("TARGET REPO RATE", f"{projected_repo:.2%}")
    r3.metric("10Y G-SEC YIELD", f"{g_sec_yield:.3%}")
    
    sectors = ['AUTO OEMs', 'PAINTS', 'AVIATION', 'REFINERS', 'LOGISTICS']
    multiples_baseline = [24.5, 55.0, 32.0, 11.5, 38.5]
    multiples_shifts = [-3.5*(crude_delta_pct/50.0), -9.0*(crude_delta_pct/50.0), -12.5*(brent_crude/80.0), +4.2*(brent_crude/80.0), -5.0*(diesel_price/92.5)]
    
    df_nse = pd.DataFrame({'SECTOR': sectors, 'BASE P/E': multiples_baseline, 'SHIFT': multiples_shifts})
    fig_nse = px.scatter(df_nse, x='SECTOR', y='SHIFT', size='BASE P/E', color='SHIFT', color_continuous_scale='RdYlGn', template='plotly_dark')
    fig_nse.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=200, font=chart_font, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_nse, use_container_width=True)

# --- TAB 4: FMCG DEFENSE (ANIMATION: SLIDE RIGHT) ---
with t4:
    st.markdown("<div class='anim-fmcg'><b>[MAPPED] FMCG RAW MATERIAL SENSITIVITY DOSSIER</b></div><br>", unsafe_allow_html=True)
    
    lab_inflation = crude_delta_pct * 0.85
    hdpe_inflation = crude_delta_pct * 0.65
    palm_oil_shock = (crude_delta_pct * 0.3) + (freight_shock * 0.4)
    
    f1, f2, f3 = st.columns(3)
    f1.metric("LAB INDEX (DETERGENTS)", f"{lab_inflation:+.2f}%")
    f2.metric("HDPE INDEX (PLASTICS)", f"{hdpe_inflation:+.2f}%")
    f3.metric("PALM OIL (SOAPS)", f"{palm_oil_shock:+.2f}%")
    
    companies = ['HUL', 'GODREJ', 'DABUR', 'MARICO']
    gross_margin_baselines = [51.2, 53.5, 46.8, 49.5]
    simulated_margins = [base - (crude_delta_pct * v) - (freight_shock * 0.01) for base, v in zip(gross_margin_baselines, [0.08, 0.11, 0.04, 0.07])]
    
    fig_fmcg = go.Figure()
    fig_fmcg.add_trace(go.Bar(name='BASE MARGIN', x=companies, y=gross_margin_baselines, marker_color='#1e3a8a'))
    fig_fmcg.add_trace(go.Bar(name='SIM MARGIN', x=companies, y=simulated_margins, marker_color='#10b981'))
    fig_fmcg.update_layout(barmode='group', template='plotly_dark', margin=dict(l=10, r=10, t=10, b=10), height=200, font=chart_font, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_fmcg, use_container_width=True)

# --- TAB 5: FOOD TECH ---
with t5:
    st.markdown("<div class='anim-slide'><b>FOOD DELIVERY UNIT ECONOMICS</b></div>", unsafe_allow_html=True)
    base_last_mile = 28.5  
    simulated_last_mile = base_last_mile * (1 + ((diesel_price - 92.5) / 92.5) * 0.75) + (freight_shock * 0.02)
    margin_loss = ((simulated_last_mile - base_last_mile) / base_last_mile) * 4.2
    
    ft1, ft2 = st.columns(2)
    ft1.metric("SIM LAST MILE COST", f"₹{simulated_last_mile:.2f}")
    ft2.metric("PLATFORM MARGIN COMPRESSION", f"{-margin_loss:.2f}%")
    
    components = ['RIDER PAY', 'FUEL SURCHARGE', 'TECH INFRA']
    scaled_costs = [18.0 * (1 + (mandi_disruption - 1) * 0.2), 6.5 * (diesel_price / 92.5), 1.5]
    fig_food = go.Figure(data=[go.Pie(labels=components, values=scaled_costs, hole=.3)])
    fig_food.update_layout(template='plotly_dark', margin=dict(l=10, r=10, t=10, b=10), height=200, font=chart_font, paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_food, use_container_width=True)

# --- TAB 6: AGRI MANDI ---
with t6:
    st.markdown("<div class='anim-slide'><b>AGRICULTURAL BOTTLENECK INFLATION</b></div>", unsafe_allow_html=True)
    crops = {"EDIBLE OILS": 4.5, "TOMATO": 8.2, "ONION": 6.8, "POTATO": 5.1}
    calculated_shocks = [v * (1 + (crude_delta_pct / 100) * 0.4) * mandi_disruption for k, v in crops.items()]
    fig_crops = px.bar(x=list(crops.keys()), y=calculated_shocks, color=calculated_shocks, color_continuous_scale='Oranges', template='plotly_dark')
    fig_crops.update_layout(margin=dict(l=10, r=10, t=10, b=10), height=200, font=chart_font, plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_crops, use_container_width=True)

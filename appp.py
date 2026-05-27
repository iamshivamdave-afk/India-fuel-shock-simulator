import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# --- HARDENED WEBAPP FRAMEWORK OVERRIDES ---
st.set_page_config(
    page_title="India Energy Shock & Margin Stress Engine",
    page_icon="🛢️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SECURITY ENHANCED APPLICATION STYLE LAYER ---
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;700&display=swap');

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

html, body, [class*="css"]  {
    font-family: 'Inter', sans-serif;
    background-color: #030712;
    color: #f3f4f6;
    font-size: 13px;
}
.stApp {
    background: linear-gradient(180deg, #030712, #0b1528);
}
section[data-testid="stSidebar"] {
    background: #090f1c !important;
    border-right: 1px solid #1f2937;
}
.block-container {
    padding: 1.5rem 2rem 0rem 2rem !important;
}
h1 {
    font-size: 2.3rem !important;
    font-weight: 800 !important;
    letter-spacing: -0.03em;
    color: #ffffff !important;
    margin: 0;
}
h2 {
    font-size: 1.4rem !important;
    font-weight: 700 !important;
    color: #ffffff !important;
}
h3 {
    font-size: 1.1rem !important;
    color: #38bdf8 !important;
}
div[data-testid="metric-container"] {
    background: #0f172a;
    border: 1px solid #1e293b;
    padding: 0.8rem;
    border-radius: 8px;
    box-shadow: 0 4px 6px -1px rgba(0,0,0,0.3);
}
div[data-testid="stMetricValue"] {
    font-size: 1.5rem !important;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 700;
}
.dossier-card {
    background: #0b1324;
    border: 1px solid #1e293b;
    border-left: 4px solid #38bdf8;
    padding: 1.25rem;
    border-radius: 6px;
    margin-top: 1rem;
}
.math-card {
    background: #090f1c;
    border: 1px solid #1f2937;
    padding: 1.2rem;
    border-radius: 8px;
    margin-bottom: 1rem;
}
.terminal-box {
    background: #090f1c;
    padding: 22px;
    border-radius: 10px;
    border: 1px solid #1f2937;
    border-left: 5px solid #38bdf8;
    margin-bottom: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR FACTOR INPUT MATRIX ---
st.sidebar.markdown("### ⚙️ STRATEGIC CONTROLS")

petrol_price = st.sidebar.slider("Current Petrol Price (₹/Litre)", 90, 150, 110)
brent = st.sidebar.slider("Brent Crude Oil (USD/Barrel)", 75, 160, 120)
lng_price = st.sidebar.slider("Spot LNG Shock (USD/MMBtu)", 10, 45, 22)
hormuz = st.sidebar.slider("Hormuz Shipping Disruption Scale", 0, 10, 6)
inr_depr = st.sidebar.slider("INR Depreciation vs USD (%)", 0, 20, 8)

st.sidebar.markdown("---")
monsoon = st.sidebar.selectbox("Monsoon/Climate Scenario Vector", ["Normal Monsoon Conditions", "Deficient Monsoon El Niño Shock"])

st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 INTERACTIVE PUBLIC TRACTION")
st.sidebar.markdown(
    '<div style="background:#0f172a; border:1px solid #1e293b; padding:10px; border-radius:6px; text-align:center;">'
    '<p style="color:#38bdf8; font-family:\'JetBrains Mono\'; font-weight:700; margin:0; font-size:12px;">🛡️ LINK TRACKING LIVE</p>'
    '<p style="color:#94a3b8; margin:4px 0 0 0; font-size:11px;">Monitor live unique click statistics via your Streamlit Cloud panel.</p>'
    '</div>',
    unsafe_allow_html=True
)

# --- ANCHORED STATISTICAL BASELINES ---
BASE_CPI = 3.48
BASE_WPI = 8.30
BASE_PETROL = 98.0
BASE_BRENT = 85.0

# --- PARAMETRIC TRANSMISSION MATH ---
petrol_shock = petrol_price - BASE_PETROL
crude_shock = brent - BASE_BRENT
freight_surcharge = (crude_shock * 0.05) + (hormuz * 0.25) + (inr_depr * 0.15)
climate_premium = 1.65 if "Deficient" in monsoon else 0.0

projected_cpi = max(1.2, round(BASE_CPI + (petrol_shock * 0.02) + (freight_surcharge * 0.10) + climate_premium, 2))
projected_wpi = max(1.8, round(BASE_WPI + (crude_shock * 0.08) + (hormuz * 0.35) + (inr_depr * 0.20), 2))
rbi_hawkishness = min(100, max(5, int((projected_cpi * 12.0) + (crude_shock * 0.18))))
thali_index = max(1.0, round(12.5 + (petrol_shock * 0.12) + (freight_surcharge * 0.4) + (climate_premium * 3.5), 1))

macro_regime = "CRISIS ZONE 🚨" if projected_cpi >= 5.2 else ("ALERT MODE 🟡" if projected_cpi >= 4.4 else "NORMAL REGIME 🟢")

# --- MASTER DISPLAY HEADER ---
st.markdown("""
<div class="terminal-box">
    <p style="color:#38bdf8; font-weight:700; font-family:'JetBrains Mono'; margin:0;">SYSTEM MATRIX // INSTITUTIONAL MACRO TRANSMISSION CORE</p>
    <h1 style="margin: 0.3rem 0;">🇮🇳 India Energy Shock & Margin Stress Engine</h1>
    <p style="font-size:13px; color:#94a3b8; margin:0;">
        Simulating input cost propagation vectors, retail food shocks, and listed equity margin compression maps across sub-continental trade networks.
    </p>
</div>
""", unsafe_allow_html=True)

# --- ALIGNED KPI DASHBOARD ---
m1, m2, m3, m4, m5, m6 = st.columns(6)
m1.metric("Projected CPI Inflation", f"{projected_cpi:.2f}%")
m2.metric("Projected Wholesale WPI", f"{projected_wpi:.2f}%")
m3.metric("Baseline Fuel Weight", "24.71%")
m4.metric("Crude Elasticity Anchor", "67.20%")
m5.metric("Household Thali Index", f"+{thali_index}%")
m6.metric("System Risk Matrix State", macro_regime)

st.markdown("---")

# --- PRODUCTION TABS INTERFACE ---
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "🍱 Food Tech Delivery Index",
    "🌾 Kitchen Thali Logistics Engine",
    "🏢 FMCG Defense Dossiers",
    "🗺️ Maritime Sourcing Maps",
    "📊 NSE Capital Realization",
    "🏦 Monetary Intervention Stance",
    "🧮 Behind The Math"
])

# --- TAB 1: FOOD TECH DELIVERY INDEX ---
with tab1:
    st.subheader("🛵 Food Tech & Quick Commerce Last-Mile Shock Matrix")
    st.markdown("""
    Simulating the impact of fuel surges on last-mile delivery economics, gig-worker payouts, and immediate contribution margin compressions.
    """)
    
    rider_payout_delta = round((petrol_shock * 0.45) + (inr_depr * 0.1), 2)
    delivery_burn = round(2.1 + (petrol_shock * 0.08), 2)
    
    ft_companies = ["Zomato (Food Delivery)", "Swiggy (Food Delivery)", "Blinkit (Quick Commerce)", "Instamart (Quick Commerce)"]
    gig_inflation = [rider_payout_delta, rider_payout_delta * 0.95, rider_payout_delta * 1.15, rider_payout_delta * 1.10]
    margin_impact = [delivery_burn, delivery_burn * 1.05, delivery_burn * 1.30, delivery_burn * 1.25]
    
    ft_df = pd.DataFrame({
        "Platform Segment": ft_companies,
        "Rider Fuel Payout Escalation (%)": np.clip(gig_inflation, 0.0, 40.0).round(2),
        "Contribution Margin Drag (% of AOV)": np.clip(margin_impact, 0.0, 15.0).round(2)
    })
    
    col_ft1, col_ft2 = st.columns([5, 4])
    with col_ft1:
        fig_ft = px.bar(
            ft_df, x="Platform Segment", y="Rider Fuel Payout Escalation (%)",
            color="Contribution Margin Drag (% of AOV)", text="Rider Fuel Payout Escalation (%)",
            template="plotly_dark", color_continuous_scale="Reds"
        )
        fig_ft.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_ft, width='stretch')
        
    with col_ft2:
        st.markdown("#### 📊 Delivery Operational Breakdown")
        st.dataframe(ft_df, width='stretch', hide_index=True)
        st.markdown(f"""
        <div class="dossier-card" style="border-left-color: #ef4444;">
            <h3 style="margin-top:0; color:#ef4444;">⚠️ QUICK COMMERCE INFLATION SQUEEZE</h3>
            <p style="color:#e2e8f0; font-size:13px; line-height:1.5;">
                Quick Commerce networks (Blinkit / Instamart) display a significantly higher fuel shock vulnerability than traditional food delivery segments due to higher hyper-local route density and strict delivery runtime timelines.
            </p>
            <hr style="border-color:#1e293b; margin:12px 0;">
            <p style="margin:0;"><b>Est. Delivery Payout Surge Per Order:</b> <span style="color:#ef4444; font-weight:bold;">₹{(petrol_shock * 0.18):.2f}</span></p>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 2: KITCHEN THALI LOGISTICS ---
with tab2:
    st.subheader("🌾 Agricultural Supply Chain Shock & Inter-State Bottlenecks")
    
    commodities = ["Tomato", "Edible Oils", "Onion", "Potato", "Poultry Feed", "Milk", "Pulses", "Sugar", "Rice", "Wheat"]
    base_shifts = np.array([6.1, 5.89, 5.68, 5.25, 5.04, 4.82, 4.40, 4.18, 3.87, 3.70])
    dynamic_surcharge = base_shifts + (crude_shock * 0.04) + (freight_surcharge * 0.15) + (climate_premium * 1.5)
    
    agri_df = pd.DataFrame({
        "Commodity": commodities,
        "Projected Cost Shift (%)": np.clip(dynamic_surcharge, 1.0, 45.0).round(2)
    })
    
    col_ag1, col_ag2 = st.columns([5, 4])
    with col_ag1:
        fig_agri = px.bar(
            agri_df.sort_values("Projected Cost Shift (%)"),
            x="Projected Cost Shift (%)", y="Commodity", orientation="h",
            color="Projected Cost Shift (%)", text="Projected Cost Shift (%)",
            template="plotly_dark", color_continuous_scale="Oranges"
        )
        fig_agri.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_agri, width='stretch')
        
    with col_ag2:
        st.markdown("🔍 **Mandi Supply Chain Inspector**")
        selected_agri = st.selectbox("Select a core food component to inspect structural pipeline risk:", commodities)
        
        profiles = {
            "Tomato": "Primary Logistics Sourcing Hubs: Nashik & Kolar. Vector: Extreme perishability. Relies entirely on prompt trucking operations.",
            "Edible Oils": "Primary Logistics Ports: Kandla & Mundra. Vector: High maritime exposure combined with domestic bulk dispatch lines.",
            "Onion": "Primary Logistics Mandis: Lasalgaon & Ahmednagar. Vector: Storage evaporation elements coupled with transport friction.",
            "Potato": "Primary Storage Infrastructure: Agra & Hooghly. Vector: Cold chain electricity load coupled with highway freight freightage.",
            "Poultry Feed": "Primary Logistics Processing: Guntur & Indore. Vector: Coarse grain transit expenses moving over long haul channels.",
            "Milk": "Primary Logistics Sheds: Anand & Western UP. Vector: Daily refrigerated runtime operations requiring constant fuel inputs.",
            "Pulses": "Primary Logistics Trade Nodes: Latur & Indore. Vector: Commercial dry terminal operations linked directly to artery freights.",
            "Sugar": "Primary Refinery Clusters: Meerut & Kolhapur. Vector: Massive seasonal transport logistics during crush parameters.",
            "Rice": "Primary Processing Clusters: Karnal & Burdwan. Vector: High-volume bulk shipments moving toward coastal export corridors.",
            "Wheat": "Primary Storage Mandis: Khanna & Indore. Vector: Public distribution haulage operations executing on road-rail integrations."
        }
        
        st.markdown(f"""
        <div class="dossier-card" style="border-left-color: #f97316;">
            <h3 style="margin-top:0; color:#f97316;">📋 LOGISTICS PROFILE: {selected_agri.upper()}</h3>
            <p style="color:#e2e8f0; font-size:13px; line-height:1.5;">{profiles[selected_agri]}</p>
            <hr style="border-color:#1e293b; margin:12px 0;">
            <p style="margin:0;"><b>Current Simulated Pipeline Inflation:</b> <span style="color:#f97316; font-weight:bold;">{agri_df.loc[agri_df['Commodity'] == selected_agri, 'Projected Cost Shift (%)'].values[0]}%</span></p>
        </div>
        """, unsafe_allow_html=True)

# --- TAB 3: FMCG DEFENSE DOSSIERS ---
with tab3:
    st.subheader("📋 Listed FMCG Corporate Matrix & Structural Actions")
    
    companies = ["HUL", "Nestle India", "Britannia", "Dabur", "Marico", "ITC FMCG"]
    rural_exp = [42, 28, 55, 60, 52, 35]
    pack_sens = [68, 52, 74, 58, 63, 49]
    
    margin_comp = 2.5 + (crude_shock * 0.02) + (freight_surcharge * 0.03) + (np.array(rural_exp) * 0.01)
    price_hikes = margin_comp * 0.62
    
    fmcg_df = pd.DataFrame({
        "Company": companies,
        "Rural Exposure (%)": rural_exp,
        "Packaging Sensitivity (%)": pack_sens,
        "Margin Compression (%)": margin_comp.round(2),
        "Direct Price Hikes (%)": price_hikes.round(2)
    })
    st.dataframe(fmcg_df, width='stretch', hide_index=True)

# --- TAB 4: MARITIME SOURCING MAPS ---
with tab4:
    st.subheader("⚓ Global Maritime Strategic Chokepoints & Insurance Add-ons")
    st.markdown(f"""
    <div class="dossier-card">
        <h3>📍 Strait of Hormuz Risk Multiplier</h3>
        <p>Current Conflict/Disruption Scale: <b>{hormuz}/10</b></p>
        <p>Simulated Freight Surcharge Squeeze: <b>+{freight_surcharge:.2f}%</b> across Arabian Sea trade lanes.</p>
        <p>War Risk Insurance Premium Delta: <b>+{hormuz * 14.5}%</b> for India-bound tankers navigating West Asian corridors.</p>
    </div>
    """, unsafe_allow_html=True)

# --- TAB 5: NSE CAPITAL REALIZATION ---
with tab5:
    st.subheader("📊 Sectoral Equity Revisions & Structural Outflows")
    
    market_df = pd.DataFrame({
        "Listed Corporation": ["ONGC (Upstream)", "Oil India (Upstream)", "Reliance Industries", "IndiGo Airlines", "Asian Paints", "Britannia FMCG"],
        "EPS Revision Trajectory (%)": [16.4, 12.8, 4.2, -18.5, -12.1, -7.4]
    })
    
    fig_market = px.bar(
        market_df, x="Listed Corporation", y="EPS Revision Trajectory (%)",
        color="EPS Revision Trajectory (%)", template="plotly_dark",
        color_continuous_scale="RdBu", text="EPS Revision Trajectory (%)"
    )
    fig_market.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_market, width='stretch')

# --- TAB 6: MONETARY INTERVENTION STANCE ---
with tab6:
    st.subheader("Reserve Bank of India Monetary Policy Transmission Framework")
    col_cb1, col_cb2 = st.columns([4, 5])
    
    with col_cb1:
        st.markdown("#### Systemic Stance Trigger Parameters")
        rbi_stance_data = {
            "Retail CPI Target Range (%)": ["<4.0", "4.0-4.8", "4.8-5.5", "5.5-6.5", ">6.5"],
            "Inferred Stance Action Matrix": ["Status Quo Accommodative", "Calibrated tightening", "Withdrawal of accommodation", "Aggressive inflation focus", "Emergency inflation defense"],
            "Projected Bond Impact": ["None", "+25bps", "+50bps", "+75bps", "+100bps+"]
        }
        st.dataframe(pd.DataFrame(rbi_stance_data), width='stretch', hide_index=True)
        
        st.markdown("##### System Action Node Status:")
        if projected_cpi < 4.0: st.info("🎯 Stance: Accommodative Matrix Online (0 bps)")
        elif projected_cpi < 4.8: st.warning("⚠️ Stance: Calibrated Tightening Engaged (+25 bps)")
        elif projected_cpi < 5.2: st.warning("⚡ Stance: Withdrawal of Accommodation Enabled (+50 bps)")
        else: st.error("🚨 Stance: Aggressive Inflation Intercept Active (+75 bps+)")

    with col_cb2:
        st.markdown("#### Dynamic Macro Sovereign Risk Scenario Curve")
        scenarios, g_bonds, cad_gdp = ["$90", "$110", "$130", "$150+"], [7.1, 7.6, 8.2, 9.1], [1.8, 2.5, 3.2, 4.7]
        
        fig_rbi = make_subplots(specs=[[{"secondary_y": True}]])
        fig_rbi.add_trace(go.Bar(x=scenarios, y=cad_gdp, name="Projected CAD (% of GDP)", marker_color="#f97316"), secondary_y=False)
        fig_rbi.add_trace(go.Scatter(x=scenarios, y=g_bonds, name="India 10Y GBOND Yield (%)", mode='lines+markers', line=dict(color='#38bdf8', width=3)), secondary_y=True)
        
        fig_rbi.update_layout(
            template="plotly_dark", plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig_rbi.update_xaxes(title_text="Brent Crude Scenario")
        fig_rbi.update_yaxes(title_text="Projected CAD (% of GDP)", secondary_y=False, showgrid=False)
        fig_rbi.update_yaxes(title_text="India 10Y GBOND Yield (%)", secondary_y=True, showgrid=False)
        st.plotly_chart(fig_rbi, width='stretch')

# --- TAB 7: PROPAGATION EQUATION SCHEMAS ---
with tab7:
    st.subheader("🧮 Integrated Logistical Transmission Formulas")
    st.markdown("""
    <div class="math-card">
        <h4 style="color:#38bdf8; margin:0;">1. Composite CPI Inflation Transmission Engine</h4>
        <code>Projected CPI = Base Baseline (3.48%) + (Petrol Shock × 0.02) + (Freight Surcharge × 0.10) + Climate Premium</code>
    </div>
    <div class="math-card">
        <h4 style="color:#38bdf8; margin:0;">2. Freight Surcharge Squeeze Function</h4>
        <code>Freight Surcharge = (Crude Shock × 0.05) + (Hormuz Risk Scale × 0.25) + (INR Depreciation × 0.15)</code>
    </div>
    """, unsafe_allow_html=True)

# --- SYSTEM LEVEL FOOTER ---
st.markdown("""
<hr style="border-color:#1f2937;">
<p style='color:#6b7280; font-size:11px; text-align:center; font-family:"JetBrains Mono";'>
    🇮🇳 India Fuel Shock Regime Engine • Verification Tier 1 Secured (Cloud Sandboxed) • Built using Streamlit Core
</p>
""", unsafe_allow_html=True)

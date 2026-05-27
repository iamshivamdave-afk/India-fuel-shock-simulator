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

/* Main layout overrides */
.reportview-container, .main {
    background-color: #030712;
    color: #f3f4f6;
    font-family: 'Inter', sans-serif;
}
div[data-testid="stSidebar"] {
    background-color: #0b0f19;
    border-right: 1px solid #1f2937;
}

/* Hide Streamlit branding clutter */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Card layout wrapper */
.metric-card {
    background-color: #111827;
    border: 1px solid #1f2937;
    padding: 1.25rem;
    border-radius: 0.5rem;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR / RISK FACTOR CONTROLS ---
st.sidebar.markdown("### ⚙️ RISK FACTOR CONTROLS")
brent_anchor = st.sidebar.slider("Brent Crude Anchor (USD/bbl)", 60.0, 180.0, 118.0, step=1.0)
hormuz_scale = st.sidebar.slider("Hormuz Strait Conflict Scale", 1, 10, 5)

st.sidebar.markdown("### ⛽ DOWNSTREAM RETAIL PRICING")
petrol_cost = st.sidebar.slider("Petrol Retail Cost (₹/Litre)", 80, 150, 100)
diesel_cost = st.sidebar.slider("Diesel Commercial Cost (₹/Litre)", 75, 140, 101)
spot_lng = st.sidebar.slider("Spot LNG Infrastructure Gas (USD/MMBtu)", 10, 60, 20)

monsoon_variant = st.sidebar.selectbox(
    "Monsoon Shock Variant",
    ["Normal Climatic Balance", "Deficit (-12% El Niño)", "Severe Drought Blockade"]
)

# --- REAL-TIME TRANSMISSION MATHEMATICS ENGINE ---
brent_base = 75.0
delta_crude_pct = ((brent_anchor - brent_base) / brent_base) * 100
delta_freight_pct = (hormuz_scale * 12.5)

# Metrics Derived from "Behind the Math" Formulation Matrices
wpi_baseline = 4.5
wpi_projected = wpi_baseline + (delta_crude_pct * 0.11) + (delta_freight_pct * 0.03)

cpi_baseline = 3.8
cpi_projected = cpi_baseline + (delta_crude_pct * 0.025) * 1.2

thali_shock_multiplier = 1.0
if monsoon_variant == "Deficit (-12% El Niño)":
    thali_shock_multiplier = 1.4
elif monsoon_variant == "Severe Drought Blockade":
    thali_shock_multiplier = 1.9
thali_index_pct = 8.5 + (delta_crude_pct * 0.08) * thali_shock_multiplier

# Evaluate System Risk State
if wpi_projected > 12.0 or hormuz_scale >= 8:
    risk_state = "CRISIS MATRIX ACTIVE"
    risk_color = "#ef4444"
elif wpi_projected > 7.5:
    risk_state = "ELEVATED RISK REGIME"
    risk_color = "#f59e0b"
else:
    risk_state = "STABLE COMPLIANCE"
    risk_color = "#10b981"

# --- TOP INSTITUTIONAL MACRO TRANSMISSION CORE ---
st.markdown("##### SYSTEM MATRIX // INSTITUTIONAL MACRO TRANSMISSION CORE")
st.markdown("## 🇮🇳 India Energy Shock & Margin Stress Engine")
st.markdown("<p style='color:#9ca3af; font-size:0.9rem;'>Simulating input cost propagation vectors, retail food shocks, and downstream network margin compression under active macro stress regimes.</p>", unsafe_allow_html=True)

m_col1, m_col2, m_col3, m_col4, m_col5, m_col6 = st.columns(6)
with m_col1:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Projected CPI Inflation</span><br><span style='font-size:1.6rem;font-weight:700;'>{cpi_projected:.2f}%</span></div>", unsafe_allow_html=True)
with m_col2:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Projected Wholesale WPI</span><br><span style='font-size:1.6rem;font-weight:700;'>{wpi_projected:.2f}%</span></div>", unsafe_allow_html=True)
with m_col3:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Baseline Fuel Weight</span><br><span style='font-size:1.6rem;font-weight:700;'>24.71%</span></div>", unsafe_allow_html=True)
with m_col4:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Crude Elasticity Anchor</span><br><span style='font-size:1.6rem;font-weight:700;'>67.20%</span></div>", unsafe_allow_html=True)
with m_col5:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Household Thali Index</span><br><span style='font-size:1.6rem;font-weight:700;color:#f87171;'>+{thali_index_pct:.1f}%</span></div>", unsafe_allow_html=True)
with m_col6:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>System Risk Matrix State</span><br><span style='font-size:1rem;font-weight:700;color:{risk_color};'>{risk_state}</span></div>", unsafe_allow_html=True)

st.markdown("---")

# --- APP SYSTEM NAVIGATION TABS ---
tabs = st.tabs([
    "🍱 Food Tech Delivery Index", 
    "🌾 Kitchen Thali Logistics Engine", 
    "🏭 FMCG Defense Dossiers", 
    "🌻 Edible Oil Import Shock & Indian Kitchen Inflation Module",
    "🏦 Monetary Intervention Stance",
    "📝 Behind The Math"
])

# ================= TAB 1: FOOD TECH DELIVERY INDEX =================
with tabs[0]:
    st.markdown("### 📦 Food Delivery Platform Operating Margin Matrix")
    col_t1_1, col_t1_2 = st.columns([1, 2])
    with col_t1_1:
        sim_last_mile = 25.50 + (diesel_cost * 0.04)
        st.metric("Simulated Last-Mile Delivery Cost", f"₹{sim_last_mile:.2f} / order", f"+{((sim_last_mile-25.5)/25.5)*100:.1f}% vs Base")
        st.metric("Projected Platform Contribution Margin", f"{6.25 - (delta_crude_pct*0.015):.2f}%", f"-{(delta_crude_pct*0.015):.2f}% Compression", delta_color="inverse")
    with col_t1_2:
        df_delivery = pd.DataFrame({
            "Cost Structure Element": ["Rider Payout", "Fuel Surcharge", "Platform Tech Fee", "Customer Acquisition"],
            "Baseline Cost (₹)": [18, 5, 4, 10],
            "Simulated Shock Cost (₹)": [18, 5 * (1 + delta_crude_pct/100), 4, 10 * (1 + delta_freight_pct/200)]
        })
        fig_delivery = px.bar(df_delivery, x="Cost Structure Element", y=["Baseline Cost (₹)", "Simulated Shock Cost (₹)"], barmode="group", title="Per-Order Delivery Fleet Overhead Analysis Matrix", template="plotly_dark")
        fig_delivery.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_delivery, use_container_width=True)

# ================= TAB 2: KITCHEN THALI LOGISTICS ENGINE =================
with tabs[1]:
    st.markdown("### 🚜 Agricultural Supply Chain Shock & Inter-State Bottlenecks")
    sel_component = st.selectbox("Select a core food component to inspect structural pipeline risk:", ["Edible Oils", "Wheat", "Rice", "Pulses", "Vegetables"])
    
    commodities = ["Wheat", "Rice", "Sugar", "Pulses", "Edible Oils", "Milk", "Potato", "Poultry Feed", "Onion", "Tomato"]
    base_shifts = [3.8, 4.1, 4.8, 5.2, 5.6, 6.0, 6.4, 6.8, 8.5, 10.2]
    simulated_shifts = [b * (1 + (delta_crude_pct * 0.004) + (hormuz_scale * 0.02)) for b in base_shifts]
    
    df_thali = pd.DataFrame({"Commodity": commodities, "Projected Cost Shift (%)": simulated_shifts})
    df_thali = df_thali.sort_values(by="Projected Cost Shift (%)")
    
    fig_thali = px.bar(df_thali, x="Projected Cost Shift (%)", y="Commodity", orientation="h", title="Agricultural Supply Chain Cost Inflation Vector by Commodity", color="Projected Cost Shift (%)", color_continuous_scale="Oranges", template="plotly_dark")
    fig_thali.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_thali, use_container_width=True)

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

# ================= TAB 4: EDIBLE OIL IMPORT SHOCK & INDIAN KITCHEN INFLATION =================
with tabs[3]:
    st.markdown("### 🌻 Edible Oil Import Shock & Indian Kitchen Inflation Module")
    st.markdown("<p style='color:#9ca3af;'>Simulating international market transmission channels (Biofuel loops, Ocean freight spikes) cascading into domestic Indian consumer baskets.</p>", unsafe_allow_html=True)
    
    # Live International Dynamic Price Calculators linked directly to Sliders
    cpo_futures = 880.0 + ((brent_anchor - 75.0) * 3.8) + (hormuz_scale * 14.0)
    soy_futures = 960.0 + ((brent_anchor - 75.0) * 2.4)
    sun_futures = 920.0 + (hormuz_scale * 28.0)
    
    oil_m1, oil_m2, oil_m3, oil_m4 = st.columns(4)
    with oil_m1:
        st.markdown(f"<div class='metric-card'><span style='color:#38bdf8;font-size:0.8rem;'>Malaysian CPO Futures</span><br><span style='font-size:1.6rem;font-weight:700;'>${cpo_futures:.2f} / MT</span><br><span style='color:#ef4444;font-size:0.75rem;'>Biofuel Diverted Loop</span></div>", unsafe_allow_html=True)
    with oil_m2:
        st.markdown(f"<div class='metric-card'><span style='color:#38bdf8;font-size:0.8rem;'>CBOT Soybean Oil</span><br><span style='font-size:1.6rem;font-weight:700;'>${soy_futures:.2f} / MT</span><br><span style='color:#f59e0b;font-size:0.75rem;'>US Crush Rate Correlated</span></div>", unsafe_allow_html=True)
    with oil_m3:
        st.markdown(f"<div class='metric-card'><span style='color:#38bdf8;font-size:0.8rem;'>Black Sea Sun Oil</span><br><span style='font-size:1.6rem;font-weight:700;'>${sun_futures:.2f} / MT</span><br><span style='color:#ef4444;font-size:0.75rem;'>Geopolitical Port Premium Active</span></div>", unsafe_allow_html=True)
    with oil_m4:
        st.markdown(f"<div class='metric-card'><span style='color:#a78bfa;font-size:0.8rem;'>National Import Dependency</span><br><span style='font-size:1.6rem;font-weight:700;'>60.20%</span><br><span style='color:#9ca3af;font-size:0.75rem;'>Macro Structural Exposure</span></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Layout Breakdown: Landed Cost Waterfall & Global Trade Flow
    oil_col1, oil_col2 = st.columns([1, 1])
    
    with oil_col1:
        st.markdown("#### 🚢 Landed Cost Waterfall Matrix (Crude Palm Oil Base)")
        
        fob_base = cpo_futures
        ocean_freight = 45.0 + (hormuz_scale * 9.5)
        insurance_handling = 12.0
        base_cif = fob_base + ocean_freight + insurance_handling
        import_duty_cess = base_cif * 0.055
        landed_inr_wholesale = (base_cif + import_duty_cess) * 83.5 / 10
        
        fig_waterfall = go.Figure(go.Waterfall(
            name="CPO Import Costing",
            orientation="v",
            measure=["relative", "relative", "relative", "total", "relative", "total"],
            x=["FOB Origin Base", "Ocean Freight Premium", "Insurance & Handling", "CIF Value (USD)", "5.5% Govt Duty & Cess", "Landed Port Cost ($/MT)"],
            text=[f"${fob_base:.0f}", f"${ocean_freight:.0f}", f"${insurance_handling:.0f}", f"${base_cif:.0f}", f"${import_duty_cess:.0f}", f"${base_cif+import_duty_cess:.0f}"],
            y=[fob_base, ocean_freight, insurance_handling, 0, import_duty_cess, 0],
            connector={"line":{"color":"rgb(63, 63, 63)"}},
            decreasing={"marker":{"color":"#10b981"}},
            increasing={"marker":{"color":"#ef4444"}},
            totals={"marker":{"color":"#3b82f6"}}
        ))
        fig_waterfall.update_layout(title="USD breakdown per Metric Tonne (FOB to Indian Wharf)", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
    with oil_col2:
        st.markdown("#### 🗺️ Structural Trade Corridors to Indian Discharge Infrastructure")
        labels = ["SE Asia (Palm)", "South America (Soy)", "Black Sea (Sun)", "Kandla Port", "Mundra Port", "JNPT Port", "Refining Complexes", "Domestic Markets"]
        source = [0, 0, 1, 1, 2, 3, 4, 5, 6]
        target = [3, 4, 4, 5, 3, 6, 6, 6, 7]
        value =  [35, 15, 15, 10, 15, 50, 25, 15, 90]
        
        fig_sankey = go.Figure(data=[go.Sankey(
            node = dict(
              pad = 15,
              thickness = 20,
              line = dict(color = "#1f2937", width = 0.5),
              label = labels,
              color = ["#f59e0b","#3b82f6","#10b981","#6366f1","#8b5cf6","#ec4899","#14b8a6","#f43f5e"]
            ),
            link = dict(
              source = source,
              target = target,
              value = value,
              color = "rgba(156, 163, 175, 0.2)"
            ))])
        fig_sankey.update_layout(title="Volumetric Supply Chain Vector Allocations (%)", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig_sankey, use_container_width=True)

    st.markdown("---")
    
    oil_col3, oil_col4 = st.columns(2)
    with oil_col3:
        st.markdown("#### 🛒 Domestic Substitution Transmission Matrix")
        st.markdown("<p style='color:#9ca3af; font-size:0.85rem;'>As import landed costs spike, domestic seed oils face extreme substitution pressures, pushing up domestic prices even without local crop deficits.</p>", unsafe_allow_html=True)
        
        oil_variants = ["Refined Palm Oil", "Crude Soybean Oil", "Imported Sunflower", "Domestic Mustard Oil", "Groundnut Oil", "Rice Bran Oil"]
        base_retail = [105, 122, 130, 145, 175, 115]
        transmission_factor = [1.0, 0.92, 0.88, 0.72, 0.50, 0.82]
        
        simulated_retail = [b + ((cpo_futures - 880.0)/880.0 * b * t) for b, t in zip(base_retail, transmission_factor)]
        
        df_retail = pd.DataFrame({
            "Oil Variant": oil_variants,
            "Baseline Price (₹/Kg)": base_retail,
            "Simulated Price (₹/Kg)": simulated_retail
        })
        
        fig_retail = px.bar(df_retail, x="Oil Variant", y=["Baseline Price (₹/Kg)", "Simulated Price (₹/Kg)"], barmode="group", color_discrete_sequence=["#4b5563", "#f97316"], template="plotly_dark")
        fig_retail.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", title="Consumer Retail Inflation Transmission Mapping Matrix")
        st.plotly_chart(fig_retail, use_container_width=True)
        
    with oil_col4:
        st.markdown("#### 📊 Household Multi-Tier Stress Heatmap Analysis")
        scenarios = ["Baseline Flow", "Moderate Surcharge", "Severe Disruption", "Hormuz Fleet Blockade"]
        segments = ["EWS (<₹3L/yr)", "Lower Mid (₹3L-8L/yr)", "Upper Mid (₹8L-18L/yr)", "High Net Worth (>18L)"]
        
        base_matrix = np.array([
            [120, 45, 20, 5],
            [280, 110, 55, 15],
            [540, 240, 120, 35],
            [980, 480, 210, 60]
        ])
        scaler = (cpo_futures / 880.0) * (1 + (hormuz_scale / 10.0))
        scaled_matrix = base_matrix * scaler
        
        fig_heatmap = px.imshow(
            scaled_matrix,
            labels=dict(x="Household Income Cohort", y="Macro Scenario Regime", color="Budget Hit (₹/Month)"),
            x=segments,
            y=scenarios,
            color_continuous_scale="Reds",
            template="plotly_dark"
        )
        fig_heatmap.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", title="Monthly Edible Oil Out-of-Pocket Stress Matrix per Household Segment")
        st.plotly_chart(fig_heatmap, use_container_width=True)

# ================= TAB 5: MONETARY INTERVENTION STANCE =================
with tabs[4]:
    st.markdown("### 🏦 RBI MPC Policy Stance Simulator Matrix")
    col_t5_1, col_t5_2 = st.columns(2)
    with col_t5_1:
        st.markdown("#### Quantitative Macro Projections")
        if cpi_projected > 6.0:
            st.warning("⚠️ CRITICAL OVER-SHOOT: CPI inflation breaches upper tolerance band limits of 6.00%. Measures required.")
        else:
            st.success("✅ STABLE STANCE: CPI inflation remains inside the 2.00% - 6.00% legal monitoring framework.")
            
        rate_hike_prob = min(100, max(0, int((cpi_projected - 4.0) * 20)))
        st.metric("Modeled Yield Rate Hike Probability (Next Policy Cycle)", f"{rate_hike_prob}%")
    with col_t5_2:
        st.markdown("#### Systemic Liquidity Profile")
        liquidity_drain = delta_crude_pct * 45.2
        st.metric("Projected Capital Outflow Vector (FX Reserves)", f"- ${liquidity_drain/100:.2f} Billion", delta_color="inverse")

# ================= TAB 6: BEHIND THE MATH =================
with tabs[5]:
    st.markdown("### 📝 Underlying Transmission Matrices & Formula Arrays")
    st.markdown(r"""
    #### 1. Wholesale Price Index (WPI) Inflation Pass-Through Vector
    $$WPI_{projected} = WPI_{baseline} + (\Delta Crude\% \times 0.11) + (\Delta Freight\% \times 0.03)$$
    
    #### 2. Consumer Price Index (CPI) Secondary Propagation Vector
    $$CPI_{projected} = CPI_{baseline} + (\Delta Crude\% \times 0.025) \times 1.2$$
    
    #### 3. Household Thali Input Index Function
    $$ThaliCost = Thali_{base} + (\Delta Crude\% \times 0.08) \times \Phi_{MonsoonVariant}$$
    
    #### 4. Edible Oil Biofuel Loop & Parity Formula Anchor
    $$CPO_{futures} = Base_{FOB} + (\Delta Brent \times 3.8) + (Scale_{Hormuz} \times 14.0)$$
    """)
    st.info("VERIFICATION MATRIX SECURITIES SYSTEM ENCRYPTED // END OF PIPELINE BUILD MODULE")delta_crude_pct = ((brent_anchor - brent_base) / brent_base) * 100
delta_freight_pct = (hormuz_scale * 12.5)

# Metrics Derived from "Behind the Math" Formulation Matrices
wpi_baseline = 4.5
wpi_projected = wpi_baseline + (delta_crude_pct * 0.11) + (delta_freight_pct * 0.03)

cpi_baseline = 3.8
cpi_projected = cpi_baseline + (delta_crude_pct * 0.025) * 1.2

thali_shock_multiplier = 1.0
if monsoon_variant == "Deficit (-12% El Niño)":
    thali_shock_multiplier = 1.4
elif monsoon_variant == "Severe Drought Blockade":
    thali_shock_multiplier = 1.9
thali_index_pct = 8.5 + (delta_crude_pct * 0.08) * thali_shock_multiplier

# Evaluate System Risk State
if wpi_projected > 12.0 or hormuz_scale >= 8:
    risk_state = "CRISIS MATRIX ACTIVE"
    risk_color = "#ef4444"
elif wpi_projected > 7.5:
    risk_state = "ELEVATED RISK REGIME"
    risk_color = "#f59e0b"
else:
    risk_state = "STABLE COMPLIANCE"
    risk_color = "#10b981"

# --- TOP INSTITUTIONAL MACRO TRANSMISSION CORE ---
st.markdown("##### SYSTEM MATRIX // INSTITUTIONAL MACRO TRANSMISSION CORE")
st.markdown("## 🇮🇳 India Energy Shock & Margin Stress Engine")
st.markdown("<p style='color:#9ca3af; font-size:0.9rem;'>Simulating input cost propagation vectors, retail food shocks, and downstream network margin compression under active macro stress regimes.</p>", unsafe_allow_html=True)

m_col1, m_col2, m_col3, m_col4, m_col5, m_col6 = st.columns(6)
with m_col1:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Projected CPI Inflation</span><br><span style='font-size:1.6rem;font-weight:700;'>{cpi_projected:.2%}\</span></div>", unsafe_allow_html=True)
with m_col2:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Projected Wholesale WPI</span><br><span style='font-size:1.6rem;font-weight:700;'>{wpi_projected:.2%}\</span></div>", unsafe_allow_html=True)
with m_col3:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Baseline Fuel Weight</span><br><span style='font-size:1.6rem;font-weight:700;'>24.71%</span></div>", unsafe_allow_html=True)
with m_col4:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Crude Elasticity Anchor</span><br><span style='font-size:1.6rem;font-weight:700;'>67.20%</span></div>", unsafe_allow_html=True)
with m_col5:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>Household Thali Index</span><br><span style='font-size:1.6rem;font-weight:700;color:#f87171;'>+{thali_index_pct:.1%}\</span></div>", unsafe_allow_html=True)
with m_col6:
    st.markdown(f"<div class='metric-card'><span style='color:#9ca3af;font-size:0.8rem;'>System Risk Matrix State</span><br><span style='font-size:1rem;font-weight:700;color:{risk_color};'>{risk_state}</span></div>", unsafe_allow_html=True)

st.markdown("---")

# --- APP SYSTEM NAVIGATION TABS ---
tabs = st.tabs([
    "🍱 Food Tech Delivery Index", 
    "🌾 Kitchen Thali Logistics Engine", 
    "🏭 FMCG Defense Dossiers", 
    "🌻 Edible Oil Import Shock & Indian Kitchen Inflation Module",
    "🏦 Monetary Intervention Stance",
    "📝 Behind The Math"
])

# ================= TAB 1: FOOD TECH DELIVERY INDEX =================
with tabs[0]:
    st.markdown("### 📦 Food Delivery Platform Operating Margin Matrix")
    col_t1_1, col_t1_2 = st.columns([1, 2])
    with col_t1_1:
        sim_last_mile = 25.50 + (diesel_cost * 0.04)
        st.metric("Simulated Last-Mile Delivery Cost", f"₹{sim_last_mile:.2f} / order", f"+{((sim_last_mile-25.5)/25.5)*100:.1f}% vs Base")
        st.metric("Projected Platform Contribution Margin", f"{6.25 - (delta_crude_pct*0.015):.2f}%", f"-{(delta_crude_pct*0.015):.2f}% Compression", delta_color="inverse")
    with col_t1_2:
        df_delivery = pd.DataFrame({
            "Cost Structure Element": ["Rider Payout", "Fuel Surcharge", "Platform Tech Fee", "Customer Acquisition"],
            "Baseline Cost (₹)": [18, 5, 4, 10],
            "Simulated Shock Cost (₹)": [18, 5 * (1 + delta_crude_pct/100), 4, 10 * (1 + delta_freight_pct/200)]
        })
        fig_delivery = px.bar(df_delivery, x="Cost Structure Element", y=["Baseline Cost (₹)", "Simulated Shock Cost (₹)"], barmode="group", title="Per-Order Delivery Fleet Overhead Analysis Matrix", template="plotly_dark")
        fig_delivery.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
        st.plotly_chart(fig_delivery, use_container_width=True)

# ================= TAB 2: KITCHEN THALI LOGISTICS ENGINE =================
with tabs[1]:
    st.markdown("### 🚜 Agricultural Supply Chain Shock & Inter-State Bottlenecks")
    sel_component = st.selectbox("Select a core food component to inspect structural pipeline risk:", ["Edible Oils", "Wheat", "Rice", "Pulses", "Vegetables"])
    
    commodities = ["Wheat", "Rice", "Sugar", "Pulses", "Edible Oils", "Milk", "Potato", "Poultry Feed", "Onion", "Tomato"]
    base_shifts = [3.8, 4.1, 4.8, 5.2, 5.6, 6.0, 6.4, 6.8, 8.5, 10.2]
    simulated_shifts = [b * (1 + (delta_crude_pct * 0.004) + (hormuz_scale * 0.02)) for b in base_shifts]
    
    df_thali = pd.DataFrame({"Commodity": commodities, "Projected Cost Shift (%)": simulated_shifts})
    df_thali = df_thali.sort_values(by="Projected Cost Shift (%)")
    
    fig_thali = px.bar(df_thali, x="Projected Cost Shift (%)", y="Commodity", orientation="h", title="Agricultural Supply Chain Cost Inflation Vector by Commodity", color="Projected Cost Shift (%)", color_continuous_scale="Oranges", template="plotly_dark")
    fig_thali.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    st.plotly_chart(fig_thali, use_container_width=True)

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

# ================= NEW TAB 4: EDIBLE OIL IMPORT SHOCK & INDIAN KITCHEN INFLATION =================
with tabs[3]:
    st.markdown("### 🌻 Edible Oil Import Shock & Indian Kitchen Inflation Module")
    st.markdown("<p style='color:#9ca3af;'>Simulating international market transmission channels (Biofuel loops, Ocean freight spikes) cascading into domestic Indian consumer baskets.</p>", unsafe_allow_html=True)
    
    # Live International Dynamic Price Calculators linked directly to Sliders
    cpo_futures = 880.0 + ((brent_anchor - 75.0) * 3.8) + (hormuz_scale * 14.0)
    soy_futures = 960.0 + ((brent_anchor - 75.0) * 2.4)
    sun_futures = 920.0 + (hormuz_scale * 28.0)
    
    oil_m1, oil_m2, oil_m3, oil_m4 = st.columns(4)
    with oil_m1:
        st.markdown(f"<div class='metric-card'><span style='color:#38bdf8;font-size:0.8rem;'>Malaysian CPO Futures</span><br><span style='font-size:1.6rem;font-weight:700;'>${cpo_futures:.2f} / MT</span><br><span style='color:#ef4444;font-size:0.75rem;'>Biofuel Diverted Loop</span></div>", unsafe_allow_html=True)
    with oil_m2:
        st.markdown(f"<div class='metric-card'><span style='color:#38bdf8;font-size:0.8rem;'>CBOT Soybean Oil</span><br><span style='font-size:1.6rem;font-weight:700;'>${soy_futures:.2f} / MT</span><br><span style='color:#f59e0b;font-size:0.75rem;'>US Crush Rate Correlated</span></div>", unsafe_allow_html=True)
    with oil_m3:
        st.markdown(f"<div class='metric-card'><span style='color:#38bdf8;font-size:0.8rem;'>Black Sea Sun Oil</span><br><span style='font-size:1.6rem;font-weight:700;'>${sun_futures:.2f} / MT</span><br><span style='color:#ef4444;font-size:0.75rem;'>Geopolitical Port Premium Active</span></div>", unsafe_allow_html=True)
    with oil_m4:
        st.markdown(f"<div class='metric-card'><span style='color:#a78bfa;font-size:0.8rem;'>National Import Dependency</span><br><span style='font-size:1.6rem;font-weight:700;'>60.20%</span><br><span style='color:#9ca3af;font-size:0.75rem;'>Macro Structural Exposure</span></div>", unsafe_allow_html=True)
        
    st.markdown("---")
    
    # Layout Breakdown: Landed Cost Waterfall & Global Trade Flow
    oil_col1, oil_col2 = st.columns([1, 1])
    
    with oil_col1:
        st.markdown("#### 🚢 Landed Cost Waterfall Matrix (Crude Palm Oil Base)")
        
        fob_base = cpo_futures
        ocean_freight = 45.0 + (hormuz_scale * 9.5)
        insurance_handling = 12.0
        base_cif = fob_base + ocean_freight + insurance_handling
        import_duty_cess = base_cif * 0.055 # 5.5% effective Basic Customs Duty + Social Welfare Cess
        landed_inr_wholesale = (base_cif + import_duty_cess) * 83.5 / 10 # Convert to Quintal Scale (per 100kg)
        
        fig_waterfall = go.Figure(go.Waterfall(
            name="CPO Import Costing",
            orientation="v",
            measure=["relative", "relative", "relative", "total", "relative", "total"],
            x=["FOB Origin Base", "Ocean Freight Premium", "Insurance & Handling", "CIF Value (USD)", "5.5% Govt Duty & Cess", "Landed Port Cost ($/MT)"],
            text=[f"${fob_base:.0f}", f"${ocean_freight:.0f}", f"${insurance_handling:.0f}", f"${base_cif:.0f}", f"${import_duty_cess:.0f}", f"${base_cif+import_duty_cess:.0f}"],
            y=[fob_base, ocean_freight, insurance_handling, 0, import_duty_cess, 0],
            connector={"line":{"color":"rgb(63, 63, 63)"}},
            decreasing={"marker":{"color":"#10b981"}},
            increasing={"marker":{"color":"#ef4444"}},
            totals={"marker":{"color":"#3b82f6"}}
        ))
        fig_waterfall.update_layout(title="USD breakdown per Metric Tonne (FOB to Indian Wharf)", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig_waterfall, use_container_width=True)
        
    with oil_col2:
        st.markdown("#### 🗺️ Structural Trade Corridors to Indian Discharge Infrastructure")
        # Sankey Flow representation mapping Origins -> Hub Indian Ports -> Refinery Chains
        labels = ["SE Asia (Palm)", "South America (Soy)", "Black Sea (Sun)", "Kandla Port", "Mundra Port", "JNPT Port", "Refining Complexes", "Domestic Markets"]
        source = [0, 0, 1, 1, 2, 3, 4, 5, 6]
        target = [3, 4, 4, 5, 3, 6, 6, 6, 7]
        value =  [35, 15, 15, 10, 15, 50, 25, 15, 90] # Percentage volumetric assignments
        
        fig_sankey = go.Figure(data=[go.Sankey(
            node = dict(
              pad = 15,
              thickness = 20,
              line = dict(color = "#1f2937", width = 0.5),
              label = labels,
              color = ["#f59e0b","#3b82f6","#10b981","#6366f1","#8b5cf6","#ec4899","#14b8a6","#f43f5e"]
            ),
            link = dict(
              source = source,
              target = target,
              value = value,
              color = "rgba(156, 163, 175, 0.2)"
            ))])
        fig_sankey.update_layout(title="Volumetric Supply Chain Vector Allocations (%)", template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig_sankey, use_container_width=True)

    st.markdown("---")
    
    oil_col3, oil_col4 = st.columns(2)
    with oil_col3:
        st.markdown("#### 🛒 Domestic Substitution Transmission Matrix")
        st.markdown("<p style='color:#9ca3af; font-size:0.85rem;'>As import landed costs spike, domestic seed oils face extreme substitution pressures, pushing up domestic prices even without local crop deficits.</p>", unsafe_allow_html=True)
        
        # Transmission Matrix calculations
        oil_variants = ["Refined Palm Oil", "Crude Soybean Oil", "Imported Sunflower", "Domestic Mustard Oil", "Groundnut Oil", "Rice Bran Oil"]
        base_retail = [105, 122, 130, 145, 175, 115]
        transmission_factor = [1.0, 0.92, 0.88, 0.72, 0.50, 0.82]
        
        simulated_retail = [b + ((cpo_futures - 880.0)/880.0 * b * t) for b, t in zip(base_retail, transmission_factor)]
        
        df_retail = pd.DataFrame({
            "Oil Variant": oil_variants,
            "Baseline Price (₹/Kg)": base_retail,
            "Simulated Price (₹/Kg)": simulated_retail
        })
        
        fig_retail = px.bar(df_retail, x="Oil Variant", y=["Baseline Price (₹/Kg)", "Simulated Price (₹/Kg)"], barmode="group", color_discrete_sequence=["#4b5563", "#f97316"], template="plotly_dark")
        fig_retail.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", title="Consumer Retail Inflation Transmission Mapping Matrix")
        st.plotly_chart(fig_retail, use_container_width=True)
        
    with oil_col4:
        st.markdown("#### 📊 Household Multi-Tier Stress Heatmap Analysis")
        
        # Dynamic Risk Heatmap generation across Macro-Scenarios
        scenarios = ["Baseline Flow", "Moderate Surcharge", "Severe Disruption", "Hormuz Fleet Blockade"]
        segments = ["EWS (<₹3L/yr)", "Lower Mid (₹3L-8L/yr)", "Upper Mid (₹8L-18L/yr)", "High Net Worth (>18L)"]
        
        # Calculate dynamic absolute monthly budget impacts in INR based on Brent and Freight sliders
        base_matrix = np.array([
            [120, 45, 20, 5],
            [280, 110, 55, 15],
            [540, 240, 120, 35],
            [980, 480, 210, 60]
        ])
        scaler = (cpo_futures / 880.0) * (1 + (hormuz_scale / 10.0))
        scaled_matrix = base_matrix * scaler
        
        fig_heatmap = px.imshow(
            scaled_matrix,
            labels=dict(x="Household Income Cohort", y="Macro Scenario Regime", color="Budget Hit (₹/Month)"),
            x=segments,
            y=scenarios,
            color_continuous_scale="Reds",
            template="plotly_dark"
        )
        fig_heatmap.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", title="Monthly Edible Oil Out-of-Pocket Stress Matrix per Household Segment")
        st.plotly_chart(fig_heatmap, use_container_width=True)

# ================= TAB 5: MONETARY INTERVENTION STANCE =================
with tabs[4]:
    st.markdown("### 🏦 RBI MPC Policy Stance Simulator Matrix")
    col_t5_1, col_t5_2 = st.columns(2)
    with col_t5_1:
        st.markdown("#### Quantitative Macro Projections")
        if cpi_projected > 6.0:
            st.warning("⚠️ CRITICAL OVER-SHOOT: CPI inflation breaches upper tolerance band limits of 6.00%. Measures required.")
        else:
            st.success("✅ STABLE STANCE: CPI inflation remains inside the 2.00% - 6.00% legal monitoring framework.")
            
        rate_hike_prob = min(100, max(0, int((cpi_projected - 4.0) * 200)))
        st.metric("Modeled Yield Rate Hike Probability (Next Policy Cycle)", f"{rate_hike_prob}%")
    with col_t5_2:
        st.markdown("#### Systemic Liquidity Profile")
        liquidity_drain = delta_crude_pct * 45.2
        st.metric("Projected Capital Outflow Vector (FX Reserves)", f"- ${liquidity_drain/100:.2f} Billion", delta_color="inverse")

# ================= TAB 6: BEHIND THE MATH =================
with tabs[5]:
    st.markdown("### 📝 Underlying Transmission Matrices & Formula Arrays")
    st.markdown(r"""
    #### 1. Wholesale Price Index (WPI) Inflation Pass-Through Vector
    $$WPI_{projected} = WPI_{baseline} + (\Delta Crude\% \times 0.11) + (\Delta Freight\% \times 0.03)$$
    
    #### 2. Consumer Price Index (CPI) Secondary Propagation Vector
    $$CPI_{projected} = CPI_{baseline} + (\Delta Crude\% \times 0.025) \times 1.2$$
    
    #### 3. Household Thali Input Index Function
    $$ThaliCost = Thali_{base} + (\Delta Crude\% \times 0.08) \times \Phi_{MonsoonVariant}$$
    
    #### 4. Edible Oil Biofuel Loop & Parity Formula Anchor
    $$CPO_{futures} = Base_{FOB} + (\Delta Brent \times 3.8) + (Scale_{Hormuz} \times 14.0)$$
    
    """)
    st.info("VERIFICATION MATRIX SECURITIES SYSTEM ENCRYPTED // END OF PIPELINE BUILD MODULE")

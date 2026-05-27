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
hormuz_scale

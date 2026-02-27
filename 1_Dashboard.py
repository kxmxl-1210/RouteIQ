import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Dashboard — RouteIQ", page_icon="📊", layout="wide")

# ── Auth Guard ─────────────────────────────────────────────────────────────────
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.session_state.logged_in = False
    st.rerun()

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'lang' not in st.session_state:
    st.session_state.lang = "EN"

def get_theme():
    if st.session_state.dark_mode:
        return {"bg":"#0f1117","card":"#1a1d27","border":"#2a2d3e","text":"#ffffff",
                "subtext":"#8b92a5","accent":"#4f46e5","accent2":"#06b6d4",
                "success":"#10b981","warning":"#f59e0b","danger":"#ef4444","input_bg":"#1e2130"}
    else:
        return {"bg":"#f8fafc","card":"#ffffff","border":"#e2e8f0","text":"#0f172a",
                "subtext":"#64748b","accent":"#4f46e5","accent2":"#0891b2",
                "success":"#059669","warning":"#d97706","danger":"#dc2626","input_bg":"#f1f5f9"}

T = get_theme()

CITY_COORDS = {
    'Chennai':(13.0827,80.2707),'Mumbai':(19.0760,72.8777),'Delhi':(28.6139,77.2090),
    'Bangalore':(12.9716,77.5946),'Hyderabad':(17.3850,78.4867),'Kolkata':(22.5726,88.3639),
    'Pune':(18.5204,73.8567),'Ahmedabad':(23.0225,72.5714),'Coimbatore':(11.0168,76.9558),
    'Madurai':(9.9252,78.1198),'Jaipur':(26.9124,75.7873),'Surat':(21.1702,72.8311),
    'Lucknow':(26.8467,80.9462),'Nagpur':(21.1458,79.0882),'Visakhapatnam':(17.6868,83.2185),
}

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');
* {{ font-family: 'Plus Jakarta Sans', sans-serif !important; }}
.stApp {{ background: {T['bg']} !important; }}
.block-container {{ padding: 24px 32px !important; max-width: 100% !important; }}
div[data-testid="stToolbar"] {{ display: none; }}
footer {{ display: none; }}
#MainMenu {{ display: none; }}
section[data-testid="stSidebar"] > div {{
    background: {T['card']} !important;
    border-right: 1px solid {T['border']} !important;
}}
.metric-card {{
    background: {T['card']};
    border: 1px solid {T['border']};
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
}}
.metric-card::before {{
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, #4f46e5, #06b6d4);
}}
.metric-value {{
    font-size: 2rem;
    font-weight: 800;
    color: {T['text']};
    line-height: 1;
    margin-bottom: 4px;
}}
.metric-label {{
    font-size: 0.8rem;
    color: {T['subtext']};
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
}}
.metric-delta-pos {{ color: #10b981; font-size: 0.85rem; font-weight: 600; margin-top: 6px; }}
.metric-delta-neg {{ color: #ef4444; font-size: 0.85rem; font-weight: 600; margin-top: 6px; }}
.section-title {{
    font-size: 1.1rem;
    font-weight: 700;
    color: {T['text']};
    margin: 24px 0 16px 0;
}}
.delivery-row {{
    display: flex;
    align-items: center;
    padding: 14px 16px;
    border-bottom: 1px solid {T['border']};
    gap: 16px;
}}
.delivery-row:last-child {{ border-bottom: none; }}
.status-badge {{
    padding: 4px 12px;
    border-radius: 100px;
    font-size: 0.75rem;
    font-weight: 700;
}}
.badge-green {{ background: #10b98120; color: #10b981; }}
.badge-yellow {{ background: #f59e0b20; color: #f59e0b; }}
.badge-red {{ background: #ef444420; color: #ef4444; }}
.topbar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 28px;
    padding-bottom: 20px;
    border-bottom: 1px solid {T['border']};
}}
.nav-link {{
    display: block;
    padding: 10px 16px;
    border-radius: 10px;
    color: {T['subtext']};
    text-decoration: none;
    font-size: 0.9rem;
    font-weight: 500;
    margin-bottom: 4px;
    transition: all 0.2s;
}}
.nav-link:hover, .nav-link.active {{
    background: {T['accent']}20;
    color: {T['accent']};
}}
</style>
""", unsafe_allow_html=True)

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown(f"""
    <div style="padding: 16px 8px 24px 8px;">
        <div style="font-size:1.5rem;font-weight:800;color:{T['text']};margin-bottom:4px;">🚚 RouteIQ</div>
        <div style="font-size:0.8rem;color:{T['subtext']};">Smart Logistics Platform</div>
    </div>
    """, unsafe_allow_html=True)

    st.page_link("pages/1_Dashboard.py", label="📊  Dashboard", )
    st.page_link("pages/2_Route_Optimizer.py", label="🗺️  Route Optimizer")
    st.page_link("pages/3_Delay_Predictor.py", label="⚠️  Delay Predictor")
    st.page_link("pages/4_Demand_Forecast.py", label="📈  Demand Forecast")
    st.page_link("pages/5_Tracker.py", label="📍  Live Tracker")
    st.page_link("pages/6_Account.py", label="👤  Account")
    st.page_link("pages/7_About.py", label="ℹ️  About")

    st.divider()
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🌙 Dark" if not st.session_state.dark_mode else "☀️ Light", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode
            st.rerun()
    with col2:
        if st.button("🌐 " + st.session_state.lang, use_container_width=True):
            st.session_state.lang = "TA" if st.session_state.lang == "EN" else "EN"
            st.rerun()

    st.divider()
    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.session_state.logged_in = False
    st.rerun()

# ── Top Bar ────────────────────────────────────────────────────────────────────
username = st.session_state.get('username', 'User')
lang = st.session_state.lang

greet = "வணக்கம்" if lang == "TA" else "Good morning"
today = datetime.now().strftime("%A, %d %B %Y")

st.markdown(f"""
<div class="topbar">
    <div>
        <div style="font-size:1.6rem;font-weight:800;color:{T['text']};">{greet}, {username} 👋</div>
        <div style="font-size:0.85rem;color:{T['subtext']};margin-top:2px;">{today}</div>
    </div>
    <div style="background:{T['card']};border:1px solid {T['border']};border-radius:12px;padding:10px 18px;font-size:0.85rem;color:{T['subtext']};">
        🟢 All systems operational
    </div>
</div>
""", unsafe_allow_html=True)

# ── KPI Cards ──────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)
kpis = [
    ("1,284", "Active Deliveries", "↑ 8.2% today", True, "📦"),
    ("₹2,43,500", "Total Cost Saved", "↑ 12% vs yesterday", True, "💰"),
    ("18,240 km", "Distance Optimized", "↑ 6.4% this week", True, "📏"),
    ("142", "At-Risk Shipments", "↓ Needs attention", False, "⚠️"),
]
for col, (val, label, delta, pos, icon) in zip([c1,c2,c3,c4], kpis):
    delta_class = "metric-delta-pos" if pos else "metric-delta-neg"
    col.markdown(f"""
    <div class="metric-card">
        <div style="font-size:1.5rem;margin-bottom:8px;">{icon}</div>
        <div class="metric-value">{val}</div>
        <div class="metric-label">{label}</div>
        <div class="{delta_class}">{delta}</div>
    </div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ── Map + Recent Deliveries ────────────────────────────────────────────────────
map_col, table_col = st.columns([1.6, 1])

with map_col:
    st.markdown(f'<div class="section-title">🗺️ {"நேரடி டெலிவரி நெட்வொர்க்" if lang=="TA" else "Live Delivery Network"}</div>', unsafe_allow_html=True)
    tile = 'CartoDB dark_matter' if st.session_state.dark_mode else 'CartoDB positron'
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles=tile)

    for city, (lat, lon) in CITY_COORDS.items():
        risk = np.random.choice(['high','medium','low'], p=[0.15,0.35,0.5])
        color = {'high':'red','medium':'orange','low':'green'}[risk]
        count = np.random.randint(20, 200)
        folium.CircleMarker(
            [lat, lon], radius=9, color=color, fill=True, fill_opacity=0.85,
            popup=folium.Popup(f"<b>{city}</b><br>Deliveries: {count}<br>Risk: {risk.upper()}", max_width=150)
        ).add_to(m)

    route = ['Chennai','Bangalore','Hyderabad','Pune','Mumbai']
    coords = [CITY_COORDS[c] for c in route]
    folium.PolyLine(coords, color='#4f46e5', weight=3, opacity=0.8, tooltip="Optimized Route").add_to(m)
    folium_static(m, height=380)

with table_col:
    st.markdown(f'<div class="section-title">📋 {"சமீபத்திய டெலிவரிகள்" if lang=="TA" else "Recent Deliveries"}</div>', unsafe_allow_html=True)
    deliveries = [
        ("DEL-2841", "Chennai → Mumbai", "On Time", "green"),
        ("DEL-2840", "Delhi → Bangalore", "Delayed", "red"),
        ("DEL-2839", "Pune → Hyderabad", "In Transit", "yellow"),
        ("DEL-2838", "Kolkata → Chennai", "On Time", "green"),
        ("DEL-2837", "Mumbai → Ahmedabad", "In Transit", "yellow"),
        ("DEL-2836", "Bangalore → Madurai", "On Time", "green"),
        ("DEL-2835", "Jaipur → Delhi", "Delayed", "red"),
    ]
    table_html = f'<div style="background:{T["card"]};border:1px solid {T["border"]};border-radius:16px;overflow:hidden;">'
    for did, route, status, color in deliveries:
        badge_class = f"badge-{color}"
        table_html += f"""
        <div class="delivery-row">
            <div style="flex:1;">
                <div style="font-weight:600;color:{T['text']};font-size:0.88rem;">{did}</div>
                <div style="color:{T['subtext']};font-size:0.8rem;margin-top:2px;">{route}</div>
            </div>
            <span class="status-badge {badge_class}">{status}</span>
        </div>"""
    table_html += "</div>"
    st.markdown(table_html, unsafe_allow_html=True)

# ── Weekly Chart ───────────────────────────────────────────────────────────────
st.markdown(f'<div class="section-title">📈 {"வாராந்திர டெலிவரி போக்கு" if lang=="TA" else "Weekly Delivery Trend"}</div>', unsafe_allow_html=True)

dates = pd.date_range(end=datetime.today(), periods=30)
chart_data = pd.DataFrame({
    'Date': dates,
    'Deliveries': np.random.randint(800, 1400, 30),
    'On Time': np.random.randint(600, 1200, 30),
    'Delayed': np.random.randint(50, 200, 30),
})

fig = go.Figure()
fig.add_trace(go.Scatter(x=chart_data['Date'], y=chart_data['Deliveries'],
    name='Total', line=dict(color='#4f46e5', width=2.5), fill='tozeroy',
    fillcolor='rgba(79,70,229,0.1)'))
fig.add_trace(go.Scatter(x=chart_data['Date'], y=chart_data['On Time'],
    name='On Time', line=dict(color='#10b981', width=2)))
fig.add_trace(go.Scatter(x=chart_data['Date'], y=chart_data['Delayed'],
    name='Delayed', line=dict(color='#ef4444', width=2)))

plot_bg = 'rgba(26,29,39,0.5)' if st.session_state.dark_mode else 'rgba(248,250,252,0.5)'
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=plot_bg,
    height=240, margin=dict(l=0,r=0,t=10,b=0),
    font=dict(color=T['subtext'], family='Plus Jakarta Sans'),
    legend=dict(orientation='h', y=1.15, bgcolor='rgba(0,0,0,0)'),
    xaxis=dict(gridcolor=T['border'], showgrid=True),
    yaxis=dict(gridcolor=T['border'], showgrid=True),
)
st.plotly_chart(fig, use_container_width=True)

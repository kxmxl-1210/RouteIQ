import streamlit as st
import folium
from streamlit_folium import folium_static
import numpy as np
import time
from datetime import datetime

st.set_page_config(page_title="Live Tracker — RouteIQ", page_icon="📍", layout="wide")
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.session_state.logged_in = False
    st.rerun()
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = True
if 'lang' not in st.session_state: st.session_state.lang = "EN"

def get_theme():
    if st.session_state.dark_mode:
        return {"bg":"#0f1117","card":"#1a1d27","border":"#2a2d3e","text":"#ffffff",
                "subtext":"#8b92a5","accent":"#4f46e5","success":"#10b981"}
    else:
        return {"bg":"#f8fafc","card":"#ffffff","border":"#e2e8f0","text":"#0f172a",
                "subtext":"#64748b","accent":"#4f46e5","success":"#059669"}
T = get_theme()
lang = st.session_state.lang

# Simulate live delivery positions along routes
ROUTES = {
    "DEL-2841": {"from": (13.0827,80.2707), "to": (19.0760,72.8777), "driver": "Ravi Kumar", "status": "In Transit"},
    "DEL-2840": {"from": (28.6139,77.2090), "to": (12.9716,77.5946), "driver": "Suresh M", "status": "Delayed"},
    "DEL-2839": {"from": (18.5204,73.8567), "to": (17.3850,78.4867), "driver": "Priya S", "status": "In Transit"},
    "DEL-2838": {"from": (22.5726,88.3639), "to": (13.0827,80.2707), "driver": "Karthik R", "status": "On Time"},
    "DEL-2837": {"from": (19.0760,72.8777), "to": (23.0225,72.5714), "driver": "Anbu T", "status": "In Transit"},
}

def get_current_position(from_coord, to_coord, progress):
    lat = from_coord[0] + (to_coord[0] - from_coord[0]) * progress
    lon = from_coord[1] + (to_coord[1] - from_coord[1]) * progress
    noise_lat = np.random.uniform(-0.05, 0.05)
    noise_lon = np.random.uniform(-0.05, 0.05)
    return (lat + noise_lat, lon + noise_lon)

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
* {{ font-family: 'Plus Jakarta Sans', sans-serif !important; }}
.stApp {{ background: {T['bg']} !important; }}
.block-container {{ padding: 28px 32px !important; max-width: 100% !important; }}
div[data-testid="stToolbar"], footer, #MainMenu {{ display: none; }}
section[data-testid="stSidebar"] > div {{ background: {T['card']} !important; border-right: 1px solid {T['border']} !important; }}
.page-title {{ font-size:1.8rem; font-weight:800; color:{T['text']}; margin-bottom:4px; }}
.page-sub {{ font-size:0.9rem; color:{T['subtext']}; margin-bottom:28px; }}
.card {{ background:{T['card']}; border:1px solid {T['border']}; border-radius:16px; padding:20px 24px; margin-bottom:12px; }}
.delivery-card {{ background:{T['card']}; border:1px solid {T['border']}; border-radius:14px; padding:16px 20px; margin-bottom:10px; cursor:pointer; transition: border-color 0.2s; }}
.delivery-card:hover {{ border-color: {T['accent']}; }}
.delivery-card.selected {{ border-color: {T['accent']}; background: {T['accent']}10; }}
.progress-bar {{ height:6px; background:{T['border']}; border-radius:100px; overflow:hidden; margin-top:8px; }}
.progress-fill {{ height:100%; border-radius:100px; background:linear-gradient(90deg,#4f46e5,#06b6d4); }}
.badge {{ padding:3px 10px; border-radius:100px; font-size:0.72rem; font-weight:700; }}
.badge-green {{ background:#10b98120; color:#10b981; }}
.badge-yellow {{ background:#f59e0b20; color:#f59e0b; }}
.badge-red {{ background:#ef444420; color:#ef4444; }}
.live-dot {{ width:8px; height:8px; background:#10b981; border-radius:50%; display:inline-block; margin-right:6px; animation: pulse 1.5s infinite; }}
@keyframes pulse {{ 0%,100%{{opacity:1;transform:scale(1)}} 50%{{opacity:0.5;transform:scale(1.3)}} }}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown(f'<div style="font-size:1.5rem;font-weight:800;color:{T["text"]};padding:16px 8px 24px;">🚚 RouteIQ</div>', unsafe_allow_html=True)
    st.page_link("pages/1_Dashboard.py", label="📊  Dashboard")
    st.page_link("pages/2_Route_Optimizer.py", label="🗺️  Route Optimizer")
    st.page_link("pages/3_Delay_Predictor.py", label="⚠️  Delay Predictor")
    st.page_link("pages/4_Demand_Forecast.py", label="📈  Demand Forecast")
    st.page_link("pages/5_Tracker.py", label="📍  Live Tracker")
    st.page_link("pages/6_Account.py", label="👤  Account")
    st.page_link("pages/7_About.py", label="ℹ️  About")
    st.divider()
    c1,c2=st.columns(2)
    with c1:
        if st.button("☀️" if st.session_state.dark_mode else "🌙", use_container_width=True):
            st.session_state.dark_mode = not st.session_state.dark_mode; st.rerun()
    with c2:
        if st.button("🌐 "+st.session_state.lang, use_container_width=True):
            st.session_state.lang = "TA" if st.session_state.lang=="EN" else "EN"; st.rerun()
    st.divider()
    if st.button("🚪 Sign Out", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

st.markdown(f"""
<div class="page-title">📍 {"நேரடி கண்காணிப்பு" if lang=="TA" else "Live Tracker"}</div>
<div class="page-sub">
    <span class="live-dot"></span>
    {"நிகழ்நேரத்தில் அனைத்து டெலிவரிகளையும் கண்காணிக்கவும்" if lang=="TA" else "Real-time tracking for all active deliveries — updates every 30 seconds"}
</div>
""", unsafe_allow_html=True)

left, right = st.columns([1, 1.8])

# Generate live positions
np.random.seed(int(time.time()) % 1000)
progress_values = {did: np.random.uniform(0.1, 0.9) for did in ROUTES}

with left:
    st.markdown(f'<div style="font-size:1rem;font-weight:700;color:{T["text"]};margin-bottom:12px;">🚚 {"செயலில் உள்ள டெலிவரிகள்" if lang=="TA" else "Active Deliveries"} ({len(ROUTES)})</div>', unsafe_allow_html=True)

    selected = st.session_state.get('selected_delivery', list(ROUTES.keys())[0])

    for did, info in ROUTES.items():
        prog = progress_values[did]
        status_badge = "badge-green" if info['status']=="On Time" else \
                       "badge-red" if info['status']=="Delayed" else "badge-yellow"
        is_selected = "selected" if did == selected else ""
        eta_hours = int((1 - prog) * np.random.randint(4, 24))

        st.markdown(f"""
        <div class="delivery-card {is_selected}" onclick="">
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;">
                <div style="font-weight:700;color:{T['text']};font-size:0.9rem;">{did}</div>
                <span class="badge {status_badge}">{info['status']}</span>
            </div>
            <div style="color:{T['subtext']};font-size:0.8rem;margin-bottom:4px;">👤 {info['driver']}</div>
            <div style="color:{T['subtext']};font-size:0.8rem;margin-bottom:8px;">⏱️ ETA: ~{eta_hours}h remaining</div>
            <div style="display:flex;justify-content:space-between;margin-bottom:4px;">
                <span style="font-size:0.75rem;color:{T['subtext']};">{"முன்னேற்றம்" if lang=="TA" else "Progress"}</span>
                <span style="font-size:0.75rem;font-weight:600;color:{T['text']};">{prog:.0%}</span>
            </div>
            <div class="progress-bar">
                <div class="progress-fill" style="width:{prog*100:.0f}%;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    if st.button("🔄 " + ("புதுப்பிக்கவும்" if lang=="TA" else "Refresh Locations"), use_container_width=True, type="primary"):
        st.rerun()
    st.markdown(f'<div style="color:{T["subtext"]};font-size:0.75rem;text-align:center;margin-top:8px;">Last updated: {datetime.now().strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)

with right:
    st.markdown(f'<div style="font-size:1rem;font-weight:700;color:{T["text"]};margin-bottom:12px;">🗺️ {"நேரடி வரைபடம்" if lang=="TA" else "Live Map"}</div>', unsafe_allow_html=True)

    tile = 'CartoDB dark_matter' if st.session_state.dark_mode else 'CartoDB positron'
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5, tiles=tile)

    colors_map = {"On Time": "green", "In Transit": "blue", "Delayed": "red"}

    for did, info in ROUTES.items():
        prog = progress_values[did]
        curr_pos = get_current_position(info['from'], info['to'], prog)
        color = colors_map.get(info['status'], 'blue')

        # Route line
        folium.PolyLine([info['from'], info['to']], color='#4f46e540', weight=2, opacity=0.5).add_to(m)

        # Origin marker
        folium.CircleMarker(info['from'], radius=5, color='#4f46e5', fill=True,
                            fill_opacity=0.7, tooltip="Origin").add_to(m)
        # Destination marker
        folium.CircleMarker(info['to'], radius=5, color='#10b981', fill=True,
                            fill_opacity=0.7, tooltip="Destination").add_to(m)

        # Live truck position
        folium.Marker(
            curr_pos,
            tooltip=f"🚚 {did} | {info['driver']} | {info['status']} | {prog:.0%} complete",
            icon=folium.Icon(color=color, icon='truck', prefix='fa')
        ).add_to(m)

        # Progress circle
        folium.CircleMarker(curr_pos, radius=14, color=colors_map.get(info['status'],'blue'),
                            fill=False, weight=2, opacity=0.5).add_to(m)

    folium_static(m, height=520)

# Bottom stats
st.markdown("<br>", unsafe_allow_html=True)
c1, c2, c3, c4 = st.columns(4)
stats = [
    ("5", "Active Vehicles", "#4f46e5"),
    ("3", "On Time", "#10b981"),
    ("1", "Delayed", "#ef4444"),
    ("1", "At Risk", "#f59e0b"),
]
for col, (val, label, color) in zip([c1,c2,c3,c4], stats):
    col.markdown(f"""
    <div style="background:{T['card']};border:1px solid {T['border']};border-radius:14px;
                padding:20px;text-align:center;border-top:3px solid {color};">
        <div style="font-size:2rem;font-weight:800;color:{color};">{val}</div>
        <div style="font-size:0.8rem;color:{T['subtext']};margin-top:4px;">{label}</div>
    </div>""", unsafe_allow_html=True)

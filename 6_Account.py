import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

st.set_page_config(page_title="Account — RouteIQ", page_icon="👤", layout="wide")
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")
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
username = st.session_state.get('username','User')

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
* {{ font-family: 'Plus Jakarta Sans', sans-serif !important; }}
.stApp {{ background: {T['bg']} !important; }}
.block-container {{ padding: 28px 32px !important; max-width: 100% !important; }}
div[data-testid="stToolbar"], footer, #MainMenu {{ display: none; }}
section[data-testid="stSidebar"] > div {{ background: {T['card']} !important; border-right: 1px solid {T['border']} !important; }}
.card {{ background:{T['card']}; border:1px solid {T['border']}; border-radius:16px; padding:24px; margin-bottom:16px; }}
.profile-header {{ background:linear-gradient(135deg,#4f46e5,#06b6d4); border-radius:16px; padding:32px; margin-bottom:20px; }}
.stat-mini {{ text-align:center; padding:16px; }}
.stat-mini-val {{ font-size:1.5rem; font-weight:800; color:{T['text']}; }}
.stat-mini-label {{ font-size:0.75rem; color:{T['subtext']}; margin-top:2px; }}
.activity-row {{ display:flex; align-items:center; gap:14px; padding:12px 0; border-bottom:1px solid {T['border']}; }}
.activity-row:last-child {{ border-bottom:none; }}
.activity-icon {{ width:36px; height:36px; border-radius:10px; display:flex; align-items:center; justify-content:center; font-size:1rem; flex-shrink:0; }}
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
        st.session_state.logged_in = False; st.switch_page("app.py")

# Profile Header
st.markdown(f"""
<div class="profile-header">
    <div style="display:flex;align-items:center;gap:20px;">
        <div style="width:70px;height:70px;background:rgba(255,255,255,0.2);border-radius:50%;
                    display:flex;align-items:center;justify-content:center;font-size:2rem;">
            👤
        </div>
        <div>
            <div style="font-size:1.5rem;font-weight:800;color:white;">{username}</div>
            <div style="color:rgba(255,255,255,0.75);font-size:0.9rem;">Logistics Manager · Pro Plan</div>
            <div style="color:rgba(255,255,255,0.6);font-size:0.8rem;margin-top:4px;">
                📧 {username.lower().replace(' ','')}@routeiq.in · 
                📅 {"Member since" if lang=="EN" else "உறுப்பினர் தொடக்கம்"} Jan 2025
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Stats Row
c1,c2,c3,c4,c5 = st.columns(5)
account_stats = [
    ("8,432", "Total Deliveries"),
    ("₹14.2L", "Total Saved"),
    ("1,24,800 km", "Distance Optimized"),
    ("2,340 L", "Fuel Saved"),
    ("96.4%", "On-time Rate"),
]
for col, (val, label) in zip([c1,c2,c3,c4,c5], account_stats):
    col.markdown(f"""
    <div class="card" style="text-align:center;padding:18px;">
        <div class="stat-mini-val">{val}</div>
        <div class="stat-mini-label">{"மொத்த டெலிவரிகள்" if label=="Total Deliveries" and lang=="TA" else label}</div>
    </div>""", unsafe_allow_html=True)

left, right = st.columns([1.2, 1])

with left:
    # Monthly savings chart
    st.markdown(f'<div style="font-size:1rem;font-weight:700;color:{T["text"]};margin-bottom:12px;">💰 {"மாதாந்திர சேமிப்பு" if lang=="TA" else "Monthly Savings (₹)"}</div>', unsafe_allow_html=True)
    months = ['Aug','Sep','Oct','Nov','Dec','Jan','Feb']
    savings = [85000, 92000, 1,10000, 1,28000, 1,45000, 1,82000, 2,43000]
    savings = [85000, 92000, 110000, 128000, 145000, 182000, 243000]
    km_saved = [3200, 3800, 4100, 4900, 5500, 6800, 8200]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=months, y=savings, name='Cost Saved (₹)',
                         marker_color='#4f46e5', opacity=0.85))
    fig.add_trace(go.Scatter(x=months, y=km_saved, name='KM Saved',
                             yaxis='y2', line=dict(color='#10b981', width=2.5),
                             mode='lines+markers', marker=dict(size=7)))

    plot_bg = 'rgba(26,29,39,0.5)' if st.session_state.dark_mode else 'rgba(248,250,252,0.5)'
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=plot_bg,
        height=280, margin=dict(l=0,r=0,t=10,b=0),
        font=dict(color=T['subtext'], family='Plus Jakarta Sans'),
        legend=dict(orientation='h', y=1.15, bgcolor='rgba(0,0,0,0)'),
        yaxis=dict(gridcolor=T['border'], title='₹ Saved'),
        yaxis2=dict(overlaying='y', side='right', title='KM Saved', gridcolor='transparent'),
        xaxis=dict(gridcolor=T['border']),
        barmode='group'
    )
    st.plotly_chart(fig, use_container_width=True)

    # Petrol savings breakdown
    st.markdown(f'<div style="font-size:1rem;font-weight:700;color:{T["text"]};margin-bottom:12px;">⛽ {"எரிபொருள் சேமிப்பு விவரம்" if lang=="TA" else "Fuel & Cost Breakdown"}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div class="card">
        <div style="display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid {T['border']};">
            <span style="color:{T['subtext']};">{"மொத்த தூர சேமிப்பு" if lang=="TA" else "Total Distance Saved"}</span>
            <span style="font-weight:700;color:{T['text']};">1,24,800 km</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid {T['border']};">
            <span style="color:{T['subtext']};">{"எரிபொருள் சேமிப்பு (@ 12L/100km)" if lang=="TA" else "Fuel Saved (@ 12L/100km)"}</span>
            <span style="font-weight:700;color:#10b981;">2,340 Litres</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid {T['border']};">
            <span style="color:{T['subtext']};">{"பெட்ரோல் செலவு சேமிப்பு (@ ₹101/L)" if lang=="TA" else "Petrol Cost Saved (@ ₹101/L)"}</span>
            <span style="font-weight:700;color:#10b981;">₹2,36,340</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:12px 0;border-bottom:1px solid {T['border']};">
            <span style="color:{T['subtext']};">{"CO₂ குறைப்பு" if lang=="TA" else "CO₂ Reduction"}</span>
            <span style="font-weight:700;color:#10b981;">6.2 Tonnes</span>
        </div>
        <div style="display:flex;justify-content:space-between;padding:12px 0;">
            <span style="color:{T['subtext']};">{"ஒட்டுமொத்த சேமிப்பு" if lang=="TA" else "Total Cost Savings"}</span>
            <span style="font-weight:800;color:#4f46e5;font-size:1.1rem;">₹14,20,000</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    # Recent activity
    st.markdown(f'<div style="font-size:1rem;font-weight:700;color:{T["text"]};margin-bottom:12px;">🕐 {"சமீபத்திய செயல்பாடுகள்" if lang=="TA" else "Recent Activity"}</div>', unsafe_allow_html=True)
    activities = [
        ("🗺️", "#4f46e520", "Route Optimized", "Chennai → Mumbai → Pune", "2 min ago", "#4f46e5"),
        ("✅", "#10b98120", "Delivery Completed", "DEL-2838 arrived on time", "18 min ago", "#10b981"),
        ("⚠️", "#f59e0b20", "Delay Alert", "DEL-2840 delayed by 2h", "1 hr ago", "#f59e0b"),
        ("📦", "#06b6d420", "New Shipment", "DEL-2841 dispatched", "2 hr ago", "#06b6d4"),
        ("📊", "#4f46e520", "Forecast Updated", "Mumbai demand +18%", "3 hr ago", "#4f46e5"),
        ("✅", "#10b98120", "Delivery Completed", "DEL-2835 arrived", "5 hr ago", "#10b981"),
        ("🗺️", "#4f46e520", "Route Optimized", "Bangalore → Coimbatore", "6 hr ago", "#4f46e5"),
    ]
    act_html = f'<div class="card">'
    for icon, bg, title, sub, time_ago, color in activities:
        act_html += f"""
        <div class="activity-row">
            <div class="activity-icon" style="background:{bg};">{icon}</div>
            <div style="flex:1;">
                <div style="font-weight:600;color:{T['text']};font-size:0.88rem;">{title}</div>
                <div style="color:{T['subtext']};font-size:0.78rem;">{sub}</div>
            </div>
            <div style="color:{T['subtext']};font-size:0.75rem;white-space:nowrap;">{time_ago}</div>
        </div>"""
    act_html += '</div>'
    st.markdown(act_html, unsafe_allow_html=True)

    # Plan info
    st.markdown(f'<div style="font-size:1rem;font-weight:700;color:{T["text"]};margin-bottom:12px;">⭐ {"திட்டம்" if lang=="TA" else "Your Plan"}</div>', unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background:linear-gradient(135deg,#4f46e515,#06b6d415);border:1px solid #4f46e530;
                border-radius:16px;padding:20px 24px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:12px;">
            <span style="font-weight:800;color:{T['text']};font-size:1.1rem;">Pro Plan ⭐</span>
            <span style="background:#4f46e5;color:white;padding:4px 12px;border-radius:100px;font-size:0.75rem;font-weight:700;">Active</span>
        </div>
        <div style="color:{T['subtext']};font-size:0.85rem;line-height:1.8;">
            ✅ Unlimited route optimizations<br>
            ✅ Real-time tracking for 50 vehicles<br>
            ✅ AI delay predictions<br>
            ✅ 14-day demand forecasting<br>
            ✅ Priority support
        </div>
        <div style="margin-top:12px;color:{T['subtext']};font-size:0.8rem;">
            Renews on 27 March 2026
        </div>
    </div>
    """, unsafe_allow_html=True)

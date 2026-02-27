import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta

st.set_page_config(page_title="Demand Forecast — RouteIQ", page_icon="📈", layout="wide")
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

ZONES = {
    'Chennai':{'base':320,'growth':0.03},'Mumbai':{'base':580,'growth':0.04},
    'Delhi':{'base':620,'growth':0.035},'Bangalore':{'base':490,'growth':0.045},
    'Hyderabad':{'base':410,'growth':0.038},'Kolkata':{'base':380,'growth':0.025},
    'Pune':{'base':340,'growth':0.04},'Coimbatore':{'base':210,'growth':0.028},
    'Madurai':{'base':180,'growth':0.022},'Ahmedabad':{'base':290,'growth':0.033},
}

def forecast(zone, days=7):
    np.random.seed(hash(zone)%2**32)
    base = ZONES[zone]['base']; growth = ZONES[zone]['growth']
    hist = []
    for i in range(30):
        date = datetime.today() - timedelta(days=30-i)
        trend = base*(1+growth*i/30)
        seasonal = 1.3 if date.weekday() in [4,5] else 1.0
        monthly = 1.2 if date.day >= 25 else 1.0
        hist.append({'date':date,'demand':int(trend*seasonal*monthly*np.random.normal(1,0.08)),'type':'Historical'})
    
    recent_avg = np.mean([h['demand'] for h in hist[-14:]])
    fcast = []
    for i in range(days):
        date = datetime.today() + timedelta(days=i+1)
        seasonal = 1.3 if date.weekday() in [4,5] else 1.0
        monthly = 1.2 if date.day >= 25 else 1.0
        fcast.append({'date':date,'demand':int(recent_avg*(1+growth*(i/30))*seasonal*monthly*np.random.normal(1,0.05)),'type':'Forecast'})
    
    return pd.DataFrame(hist), pd.DataFrame(fcast)

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
.card {{ background:{T['card']}; border:1px solid {T['border']}; border-radius:16px; padding:20px 24px; margin-bottom:16px; }}
.forecast-row {{ display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid {T['border']}; }}
.forecast-row:last-child {{ border-bottom:none; }}
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

st.markdown(f'<div class="page-title">📈 {"தேவை கணிப்பு" if lang=="TA" else "Demand Forecasting"}</div><div class="page-sub">{"மண்டல அளவில் டெலிவரி தேவையை முன்னறிவிக்கவும்" if lang=="TA" else "AI-powered delivery demand forecasts to prepare warehouses in advance"}</div>', unsafe_allow_html=True)

c1, c2 = st.columns([1,3])
with c1:
    zone = st.selectbox("🌆 " + ("நகரம் / மண்டலம்" if lang=="TA" else "Select Zone"), list(ZONES.keys()))
    days = st.slider("📅 " + ("கணிப்பு நாட்கள்" if lang=="TA" else "Forecast Days"), 3, 14, 7)

df_hist, df_fcast = forecast(zone, days)
combined = pd.concat([df_hist, df_fcast])

fig = go.Figure()
hist_data = combined[combined['type']=='Historical']
fcast_data = combined[combined['type']=='Forecast']

fig.add_trace(go.Scatter(x=hist_data['date'], y=hist_data['demand'], name='Historical',
    line=dict(color='#4f46e5', width=2.5), fill='tozeroy', fillcolor='rgba(79,70,229,0.1)'))
fig.add_trace(go.Scatter(x=fcast_data['date'], y=fcast_data['demand'], name='Forecast',
    line=dict(color='#10b981', width=2.5, dash='dot'), mode='lines+markers',
    marker=dict(size=7, color='#10b981')))

plot_bg = 'rgba(26,29,39,0.5)' if st.session_state.dark_mode else 'rgba(248,250,252,0.5)'
fig.update_layout(
    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=plot_bg,
    height=300, margin=dict(l=0,r=0,t=20,b=0),
    font=dict(color=T['subtext'], family='Plus Jakarta Sans'),
    legend=dict(orientation='h', y=1.15, bgcolor='rgba(0,0,0,0)'),
    title=dict(text=f"{zone} — Delivery Demand", font=dict(color=T['text'], size=14)),
    xaxis=dict(gridcolor=T['border']), yaxis=dict(gridcolor=T['border']),
)
st.plotly_chart(fig, use_container_width=True)

# Forecast Table + All Zones
col_a, col_b = st.columns([1, 1.3])

with col_a:
    st.markdown(f'<div style="font-size:1rem;font-weight:700;color:{T["text"]};margin-bottom:12px;">📋 {"கணிப்பு அட்டவணை" if lang=="TA" else "Forecast Table"}</div>', unsafe_allow_html=True)
    baseline = df_hist['demand'].tail(14).mean()
    table_html = f'<div class="card">'
    for _, row in df_fcast.iterrows():
        d = row['demand']; delta = d - baseline; pct = delta/baseline*100
        arrow = "↑" if delta > 0 else "↓"
        color = "#10b981" if delta > 0 else "#ef4444"
        action = ("📦 Stock Up" if lang=="EN" else "📦 கையிருப்பு அதிகரிக்கவும்") if d > baseline*1.2 else \
                 ("📉 Reduce" if lang=="EN" else "📉 குறைக்கவும்") if d < baseline*0.9 else \
                 ("✅ Normal" if lang=="EN" else "✅ சாதாரண")
        table_html += f"""
        <div class="forecast-row">
            <div>
                <div style="font-weight:600;color:{T['text']};font-size:0.88rem;">{row['date'].strftime('%a, %d %b')}</div>
                <div style="color:{T['subtext']};font-size:0.78rem;">{action}</div>
            </div>
            <div style="text-align:right;">
                <div style="font-weight:700;color:{T['text']};">{d:,}</div>
                <div style="font-size:0.78rem;color:{color};">{arrow} {abs(pct):.1f}%</div>
            </div>
        </div>"""
    table_html += '</div>'
    st.markdown(table_html, unsafe_allow_html=True)

with col_b:
    st.markdown(f'<div style="font-size:1rem;font-weight:700;color:{T["text"]};margin-bottom:12px;">🗺️ {"அனைத்து மண்டல சுருக்கம்" if lang=="TA" else "All Zones Summary"}</div>', unsafe_allow_html=True)
    today = datetime.today()
    summary = []
    for z, info in ZONES.items():
        np.random.seed((hash(z)+today.day)%2**32)
        curr = int(info['base'] * (1.3 if today.weekday() in [4,5] else 1.0) * np.random.normal(1,0.06))
        chg = round((curr - info['base'])/info['base']*100, 1)
        summary.append({'Zone':z, 'Demand':curr, 'Change':chg})
    
    df_summary = pd.DataFrame(summary).sort_values('Demand', ascending=False)
    fig2 = px.bar(df_summary, x='Zone', y='Demand', color='Change',
                  color_continuous_scale=['#10b981','#f59e0b','#ef4444'], template='plotly_dark' if st.session_state.dark_mode else 'plotly_white')
    fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor=plot_bg,
                       height=280, margin=dict(l=0,r=0,t=10,b=0),
                       font=dict(color=T['subtext']), coloraxis_showscale=False,
                       xaxis=dict(gridcolor=T['border']), yaxis=dict(gridcolor=T['border']))
    st.plotly_chart(fig2, use_container_width=True)

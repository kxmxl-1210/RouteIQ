import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.preprocessing import LabelEncoder
import joblib, os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Delay Predictor — RouteIQ", page_icon="⚠️", layout="wide")
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.session_state.logged_in = False
    st.rerun()
if 'dark_mode' not in st.session_state: st.session_state.dark_mode = True
if 'lang' not in st.session_state: st.session_state.lang = "EN"

def get_theme():
    if st.session_state.dark_mode:
        return {"bg":"#0f1117","card":"#1a1d27","border":"#2a2d3e","text":"#ffffff",
                "subtext":"#8b92a5","accent":"#4f46e5","success":"#10b981","input_bg":"#1e2130"}
    else:
        return {"bg":"#f8fafc","card":"#ffffff","border":"#e2e8f0","text":"#0f172a",
                "subtext":"#64748b","accent":"#4f46e5","success":"#059669","input_bg":"#f1f5f9"}
T = get_theme()
lang = st.session_state.lang

CITIES = ['Chennai','Mumbai','Delhi','Bangalore','Hyderabad','Kolkata',
          'Pune','Ahmedabad','Coimbatore','Madurai','Jaipur','Surat','Lucknow','Nagpur','Visakhapatnam']

@st.cache_resource
def load_model():
    np.random.seed(42)
    n = 3000
    le = LabelEncoder().fit(CITIES)
    df = pd.DataFrame({
        'distance_km': np.random.randint(50, 2000, n),
        'weight_g': np.random.randint(100, 20000, n),
        'order_dow': np.random.randint(0, 7, n),
        'order_month': np.random.randint(1, 13, n),
        'freight_value': np.random.uniform(10, 500, n),
        'item_count': np.random.randint(1, 10, n),
        'seller_enc': np.random.randint(0, len(CITIES), n),
        'customer_enc': np.random.randint(0, len(CITIES), n),
    })
    delay_prob = (df['distance_km']/2000*0.4 + df['weight_g']/20000*0.2 +
                  df['order_dow'].isin([4,5,6]).astype(int)*0.2 + np.random.uniform(0,0.3,n))
    df['is_late'] = (delay_prob > 0.5).astype(int)
    model = GradientBoostingClassifier(n_estimators=150, learning_rate=0.1, max_depth=4, random_state=42)
    model.fit(df.drop('is_late', axis=1), df['is_late'])
    return model, le

model, le = load_model()

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
.card {{ background:{T['card']}; border:1px solid {T['border']}; border-radius:16px; padding:24px; margin-bottom:16px; }}
.risk-card {{ border-radius:16px; padding:28px; text-align:center; margin:16px 0; }}
.rec-item {{ display:flex; align-items:flex-start; gap:12px; padding:12px 0; border-bottom:1px solid {T['border']}; }}
.rec-item:last-child {{ border-bottom:none; }}
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

st.markdown(f'<div class="page-title">⚠️ {"தாமத கணிப்பான்" if lang=="TA" else "Delay Predictor"}</div><div class="page-sub">{"ஒரு ஷிப்மென்ட் தாமதமாகுமா என்று AI கணிக்கும்" if lang=="TA" else "AI predicts if your shipment will be delayed before it leaves the warehouse"}</div>', unsafe_allow_html=True)

left, right = st.columns([1, 1])

with left:
    st.markdown(f'<div class="card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        seller = st.selectbox("📦 " + ("அனுப்பும் நகரம்" if lang=="TA" else "Seller City"), CITIES)
        distance = st.slider("📏 " + ("தூரம் (km)" if lang=="TA" else "Distance (km)"), 50, 2500, 800)
        freight = st.number_input("💰 " + ("சரக்கு மதிப்பு (₹)" if lang=="TA" else "Freight Value (₹)"), 10.0, 2000.0, 150.0)
        items = st.slider("📦 " + ("பொருள்களின் எண்ணிக்கை" if lang=="TA" else "Number of Items"), 1, 20, 3)
    with c2:
        customer = st.selectbox("🏠 " + ("பெறும் நகரம்" if lang=="TA" else "Customer City"), CITIES, index=3)
        weight = st.number_input("⚖️ " + ("எடை (grams)" if lang=="TA" else "Weight (grams)"), 100, 30000, 2500)
        dow = st.selectbox("📅 " + ("ஆர்டர் நாள்" if lang=="TA" else "Order Day"), ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
        month = st.selectbox("📆 " + ("மாதம்" if lang=="TA" else "Month"), list(range(1,13)), index=0)

    predict_btn = st.button("🔍 " + ("கணிக்கவும்" if lang=="TA" else "Predict Delay Risk"), use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    if predict_btn:
        dow_map = {"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4,"Sat":5,"Sun":6}
        seller_enc = le.transform([seller])[0] if seller in le.classes_ else 0
        customer_enc = le.transform([customer])[0] if customer in le.classes_ else 0

        X = pd.DataFrame([[distance, weight, dow_map[dow], month, freight, items, seller_enc, customer_enc]],
                         columns=['distance_km','weight_g','order_dow','order_month',
                                  'freight_value','item_count','seller_enc','customer_enc'])
        prob = model.predict_proba(X)[0][1]
        st.session_state['delay_prob'] = prob

    if 'delay_prob' in st.session_state:
        prob = st.session_state['delay_prob']

        if prob > 0.6:
            risk_label = "🔴 " + ("அதிக ஆபத்து — தாமதம் எதிர்பார்க்கப்படுகிறது" if lang=="TA" else "HIGH RISK — Likely Delayed")
            bg = "#ef444415"; border = "#ef444440"; text_color = "#ef4444"
            recs = [
                ("🚨", "Alert customer immediately about possible delay" if lang=="EN" else "தாமதம் பற்றி வாடிக்கையாளரை உடனே தெரிவிக்கவும்"),
                ("📦", "Switch to express courier for this shipment" if lang=="EN" else "விரைவு கூரியர் சேவையைப் பயன்படுத்தவும்"),
                ("🔄", "Reroute via a closer hub city" if lang=="EN" else "அருகில் உள்ள மையம் வழியாக திருப்பி அனுப்பவும்"),
                ("📱", "Enable real-time SMS tracking for customer" if lang=="EN" else "நிகழ்நேர SMS கண்காணிப்பை இயக்கவும்"),
            ]
        elif prob > 0.35:
            risk_label = "🟡 " + ("நடுத்தர ஆபத்து — கவனிக்கவும்" if lang=="TA" else "MEDIUM RISK — Monitor Closely")
            bg = "#f59e0b15"; border = "#f59e0b40"; text_color = "#f59e0b"
            recs = [
                ("⚠️", "Monitor this shipment closely" if lang=="EN" else "இந்த ஷிப்மென்டை கவனமாக கண்காணிக்கவும்"),
                ("📱", "Send estimated delivery confirmation to customer" if lang=="EN" else "வாடிக்கையாளருக்கு டெலிவரி உறுதிப்படுத்தல் அனுப்பவும்"),
                ("🗓️", "Consider dispatching 1 day earlier" if lang=="EN" else "1 நாள் முன்னதாக அனுப்புவதை கருத்தில் கொள்ளவும்"),
            ]
        else:
            risk_label = "🟢 " + ("குறைந்த ஆபத்து — சரியான நேரத்தில் வரும்" if lang=="TA" else "LOW RISK — Expected On Time")
            bg = "#10b98115"; border = "#10b98140"; text_color = "#10b981"
            recs = [
                ("✅", "Shipment looks good — no action needed" if lang=="EN" else "ஷிப்மென்ட் நல்லது — நடவடிக்கை தேவையில்லை"),
                ("📊", "Standard tracking is sufficient" if lang=="EN" else "நிலையான கண்காணிப்பு போதுமானது"),
                ("🎯", "Expected to arrive within delivery window" if lang=="EN" else "டெலிவரி கெடுவுக்குள் வரும் என்று எதிர்பார்க்கப்படுகிறது"),
            ]

        st.markdown(f"""
        <div style="background:{bg};border:1px solid {border};border-radius:16px;
                    padding:28px;text-align:center;margin-bottom:16px;">
            <div style="font-size:1.3rem;font-weight:700;color:{text_color};">{risk_label}</div>
            <div style="font-size:3rem;font-weight:800;color:{text_color};margin:8px 0;">{prob:.0%}</div>
            <div style="font-size:0.85rem;color:{T['subtext']};"> {"தாமத நிகழ்தகவு" if lang=="TA" else "Delay Probability"}</div>
        </div>
        """, unsafe_allow_html=True)

        # Gauge
        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=round(prob*100,1),
            number={'suffix':'%','font':{'color':text_color,'size':42}},
            gauge={
                'axis':{'range':[0,100],'tickcolor':T['subtext']},
                'bar':{'color':text_color},
                'bgcolor':T['card'],
                'steps':[
                    {'range':[0,35],'color':'#10b98115'},
                    {'range':[35,60],'color':'#f59e0b15'},
                    {'range':[60,100],'color':'#ef444415'},
                ],
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color=T['subtext']),
                          height=220, margin=dict(t=20,b=0,l=20,r=20))
        st.plotly_chart(fig, use_container_width=True)

        # Recommendations
        st.markdown(f'<div style="font-size:1rem;font-weight:700;color:{T["text"]};margin-bottom:8px;">💡 {"பரிந்துரைகள்" if lang=="TA" else "Recommendations"}</div>', unsafe_allow_html=True)
        rec_html = f'<div class="card">'
        for icon, text in recs:
            rec_html += f'<div class="rec-item"><span style="font-size:1.2rem;">{icon}</span><span style="color:{T["text"]};font-size:0.9rem;">{text}</span></div>'
        rec_html += '</div>'
        st.markdown(rec_html, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;justify-content:center;align-items:center;
                    height:400px;color:{T['subtext']};text-align:center;">
            <div style="font-size:3rem;margin-bottom:16px;">🔍</div>
            <div style="font-size:1rem;font-weight:600;">{"ஷிப்மென்ட் விவரங்களை உள்ளிட்டு கணிக்கவும்" if lang=="TA" else "Fill in shipment details and click Predict"}</div>
        </div>
        """, unsafe_allow_html=True)

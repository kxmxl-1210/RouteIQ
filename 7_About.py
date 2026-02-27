import streamlit as st

st.set_page_config(page_title="About — RouteIQ", page_icon="ℹ️", layout="wide")
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

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
* {{ font-family: 'Plus Jakarta Sans', sans-serif !important; }}
.stApp {{ background: {T['bg']} !important; }}
.block-container {{ padding: 28px 32px !important; max-width: 100% !important; }}
div[data-testid="stToolbar"], footer, #MainMenu {{ display: none; }}
section[data-testid="stSidebar"] > div {{ background: {T['card']} !important; border-right: 1px solid {T['border']} !important; }}
.hero {{ background:linear-gradient(135deg,#4f46e5,#06b6d4); border-radius:20px; padding:48px; text-align:center; margin-bottom:32px; }}
.benefit-card {{ background:{T['card']}; border:1px solid {T['border']}; border-radius:16px; padding:24px; height:100%; }}
.benefit-icon {{ font-size:2.2rem; margin-bottom:12px; }}
.benefit-title {{ font-size:1rem; font-weight:700; color:{T['text']}; margin-bottom:8px; }}
.benefit-desc {{ font-size:0.85rem; color:{T['subtext']}; line-height:1.6; }}
.stat-hero {{ background:rgba(255,255,255,0.1); border-radius:14px; padding:20px; text-align:center; margin:8px; }}
.tech-badge {{ background:{T['card']}; border:1px solid {T['border']}; border-radius:10px; padding:10px 16px; display:inline-block; margin:6px; font-size:0.85rem; color:{T['text']}; font-weight:600; }}
.team-card {{ background:{T['card']}; border:1px solid {T['border']}; border-radius:16px; padding:24px; text-align:center; }}
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

# Hero
tagline = "AI-இயங்கும் டெலிவரி தேர்வு தளம்" if lang=="TA" else "AI-Powered Delivery Optimization Platform"
desc = "RouteIQ நவீன தளவாட நிறுவனங்களுக்காக உருவாக்கப்பட்ட AI தீர்வு" if lang=="TA" else \
       "RouteIQ is built for modern logistics companies to cut costs, reduce delays, and deliver smarter using AI and Machine Learning."

st.markdown(f"""
<div class="hero">
    <div style="font-size:3rem;font-weight:800;color:white;letter-spacing:-1px;margin-bottom:8px;">🚚 RouteIQ</div>
    <div style="font-size:1.2rem;color:rgba(255,255,255,0.85);margin-bottom:24px;">{tagline}</div>
    <div style="font-size:0.95rem;color:rgba(255,255,255,0.7);max-width:600px;margin:0 auto 32px;">{desc}</div>
    <div style="display:flex;justify-content:center;flex-wrap:wrap;gap:8px;">
        <div class="stat-hero"><div style="font-size:1.8rem;font-weight:800;color:white;">30%</div><div style="color:rgba(255,255,255,0.7);font-size:0.8rem;">{"செலவு குறைப்பு" if lang=="TA" else "Cost Reduction"}</div></div>
        <div class="stat-hero"><div style="font-size:1.8rem;font-weight:800;color:white;">2M+</div><div style="color:rgba(255,255,255,0.7);font-size:0.8rem;">{"டெலிவரிகள்" if lang=="TA" else "Deliveries"}</div></div>
        <div class="stat-hero"><div style="font-size:1.8rem;font-weight:800;color:white;">98%</div><div style="color:rgba(255,255,255,0.7);font-size:0.8rem;">{"சரியான நேரம்" if lang=="TA" else "On-time Rate"}</div></div>
        <div class="stat-hero"><div style="font-size:1.8rem;font-weight:800;color:white;">85%</div><div style="color:rgba(255,255,255,0.7);font-size:0.8rem;">{"AI துல்லியம்" if lang=="TA" else "AI Accuracy"}</div></div>
    </div>
</div>
""", unsafe_allow_html=True)

# Benefits
st.markdown(f'<div style="font-size:1.4rem;font-weight:800;color:{T["text"]};text-align:center;margin-bottom:20px;">{"RouteIQ பயன்கள்" if lang=="TA" else "Why RouteIQ?"}</div>', unsafe_allow_html=True)

benefits = [
    ("🗺️", "Route Optimization" if lang=="EN" else "பாதை தேர்வு",
     "AI finds the shortest delivery path across multiple stops, saving up to 30% in distance and fuel costs every trip." if lang=="EN" else
     "AI பல நிறுத்தங்களில் குறுகிய டெலிவரி பாதையை கண்டுபிடிக்கிறது, ஒவ்வொரு பயணத்திலும் 30% வரை சேமிக்கிறது."),
    ("⚠️", "Delay Prediction" if lang=="EN" else "தாமத கணிப்பு",
     "Machine learning predicts delivery delays before dispatch, allowing teams to act proactively and alert customers." if lang=="EN" else
     "ஒரு ஷிப்மென்ட் அனுப்பப்படுவதற்கு முன்பே தாமதங்களை AI கணிக்கிறது."),
    ("📍", "Real-time Tracking" if lang=="EN" else "நிகழ்நேர கண்காணிப்பு",
     "Track all active deliveries live on an interactive map. Know exactly where every vehicle is at any moment." if lang=="EN" else
     "நேரடி வரைபடத்தில் அனைத்து டெலிவரிகளையும் கண்காணிக்கவும். ஒவ்வொரு வாகனமும் எங்கே உள்ளது என்று தெரியும்."),
    ("📈", "Demand Forecasting" if lang=="EN" else "தேவை கணிப்பு",
     "Forecast delivery demand 7-14 days in advance by zone so warehouses can stock and staff efficiently." if lang=="EN" else
     "கோதான்கள் திறமையாக இருப்புவைக்க 7-14 நாட்கள் முன்னதாக மண்டல தேவையை கணிக்கவும்."),
    ("💰", "Cost Analytics" if lang=="EN" else "செலவு பகுப்பாய்வு",
     "Track every rupee saved — fuel costs, distance reduction, petrol savings — with detailed monthly breakdowns." if lang=="EN" else
     "சேமிக்கப்பட்ட ஒவ்வொரு ரூபாயையும் கண்காணிக்கவும் — எரிபொருள் செலவு, தூர குறைப்பு, பெட்ரோல் சேமிப்பு."),
    ("🌱", "Eco Friendly" if lang=="EN" else "சுற்றுச்சூழல் நட்பு",
     "Less distance = less fuel = less CO₂. RouteIQ helps companies reduce their carbon footprint significantly." if lang=="EN" else
     "குறைந்த தூரம் = குறைந்த எரிபொருள் = குறைந்த CO₂. RouteIQ நிறுவனங்களின் கார்பன் தடயத்தை குறைக்க உதவுகிறது."),
]

c1,c2,c3 = st.columns(3)
for i, (icon, title, desc) in enumerate(benefits):
    col = [c1,c2,c3][i%3]
    col.markdown(f"""
    <div class="benefit-card" style="margin-bottom:16px;">
        <div class="benefit-icon">{icon}</div>
        <div class="benefit-title">{title}</div>
        <div class="benefit-desc">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

# Tech Stack
st.markdown(f'<div style="font-size:1.2rem;font-weight:800;color:{T["text"]};text-align:center;margin:28px 0 16px;">⚙️ {"தொழில்நுட்பம்" if lang=="TA" else "Built With"}</div>', unsafe_allow_html=True)
tech = ["🐍 Python", "⚡ Streamlit", "🤖 Scikit-learn", "📊 Plotly", "🗺️ Folium", "🧮 Gradient Boosting", "📈 Time-Series Forecasting", "🔬 Haversine Algorithm"]
tech_html = f'<div style="text-align:center;margin-bottom:32px;">'
for t in tech:
    tech_html += f'<span class="tech-badge">{t}</span>'
tech_html += '</div>'
st.markdown(tech_html, unsafe_allow_html=True)

# How it works
st.markdown(f'<div style="font-size:1.2rem;font-weight:800;color:{T["text"]};text-align:center;margin-bottom:20px;">🔄 {"இது எவ்வாறு செயல்படுகிறது" if lang=="TA" else "How It Works"}</div>', unsafe_allow_html=True)

steps = [
    ("1", "#4f46e5", "Input Shipment Data" if lang=="EN" else "ஷிப்மென்ட் தரவை உள்ளிடவும்",
     "Enter origin, destination, weight, and shipment details" if lang=="EN" else "தொடக்கம், இலக்கு, எடை மற்றும் விவரங்களை உள்ளிடவும்"),
    ("2", "#06b6d4", "AI Analyzes" if lang=="EN" else "AI பகுப்பாய்கிறது",
     "ML model predicts delays and optimizer finds best route" if lang=="EN" else "ML மாதிரி தாமதங்களை கணிக்கிறது மற்றும் சிறந்த பாதையை கண்டுபிடிக்கிறது"),
    ("3", "#10b981", "Get Results" if lang=="EN" else "முடிவுகளைப் பெறவும்",
     "See optimized route, risk level, savings, and recommendations" if lang=="EN" else "தேர்வு செய்யப்பட்ட பாதை, ஆபத்து நிலை, சேமிப்பு மற்றும் பரிந்துரைகளைப் பாருங்கள்"),
    ("4", "#f59e0b", "Track Live" if lang=="EN" else "நேரடியாக கண்காணிக்கவும்",
     "Monitor delivery in real-time on interactive map" if lang=="EN" else "ஊடாடும் வரைபடத்தில் டெலிவரியை நேரடியாக கண்காணிக்கவும்"),
]

sc1,sc2,sc3,sc4 = st.columns(4)
for col, (num, color, title, desc) in zip([sc1,sc2,sc3,sc4], steps):
    col.markdown(f"""
    <div style="background:{T['card']};border:1px solid {T['border']};border-radius:16px;padding:24px;text-align:center;">
        <div style="width:44px;height:44px;background:{color};border-radius:50%;
                    display:flex;align-items:center;justify-content:center;
                    font-size:1.2rem;font-weight:800;color:white;margin:0 auto 12px;">{num}</div>
        <div style="font-weight:700;color:{T['text']};margin-bottom:6px;">{title}</div>
        <div style="font-size:0.82rem;color:{T['subtext']};line-height:1.5;">{desc}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center;margin-top:40px;padding:24px;color:{T['subtext']};font-size:0.85rem;">
    Built with ❤️ for TN IMPACT Hackathon 2026 · RouteIQ Pro v2.0
</div>
""", unsafe_allow_html=True)

"""
RouteIQ Pro — Professional Logistics Dashboard
Main Entry Point — Login Page
"""

import streamlit as st

st.set_page_config(
    page_title="RouteIQ — Smart Delivery Platform",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── Theme State ────────────────────────────────────────────────────────────────
if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'lang' not in st.session_state:
    st.session_state.lang = "EN"

# ── Theme Colors ───────────────────────────────────────────────────────────────
def get_theme():
    if st.session_state.dark_mode:
        return {
            "bg": "#0f1117", "card": "#1a1d27", "border": "#2a2d3e",
            "text": "#ffffff", "subtext": "#8b92a5", "accent": "#4f46e5",
            "accent2": "#06b6d4", "success": "#10b981", "warning": "#f59e0b",
            "danger": "#ef4444", "input_bg": "#1e2130"
        }
    else:
        return {
            "bg": "#f8fafc", "card": "#ffffff", "border": "#e2e8f0",
            "text": "#0f172a", "subtext": "#64748b", "accent": "#4f46e5",
            "accent2": "#0891b2", "success": "#059669", "warning": "#d97706",
            "danger": "#dc2626", "input_bg": "#f1f5f9"
        }

T = get_theme()

# ── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&display=swap');

* {{ font-family: 'Plus Jakarta Sans', sans-serif !important; box-sizing: border-box; }}
html, body, .stApp {{ background: {T['bg']} !important; color: {T['text']} !important; }}
.stApp {{ background: {T['bg']} !important; }}
section[data-testid="stSidebar"] {{ display: none; }}
.block-container {{ padding: 0 !important; max-width: 100% !important; }}
div[data-testid="stToolbar"] {{ display: none; }}
footer {{ display: none; }}
#MainMenu {{ display: none; }}
button[kind="header"] {{ display: none; }}

.login-wrap {{
    min-height: 100vh;
    display: flex;
    background: {T['bg']};
}}
.login-left {{
    flex: 1;
    background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 60px;
    position: relative;
    overflow: hidden;
}}
.login-left::before {{
    content: '';
    position: absolute;
    width: 400px; height: 400px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
    top: -100px; right: -100px;
}}
.login-left::after {{
    content: '';
    position: absolute;
    width: 300px; height: 300px;
    background: rgba(255,255,255,0.05);
    border-radius: 50%;
    bottom: -80px; left: -80px;
}}
.login-right {{
    flex: 1;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 60px;
    background: {T['bg']};
}}
.brand-logo {{
    font-size: 2.8rem;
    font-weight: 800;
    color: white;
    letter-spacing: -1px;
    margin-bottom: 8px;
    z-index: 1;
}}
.brand-tagline {{
    font-size: 1.1rem;
    color: rgba(255,255,255,0.8);
    text-align: center;
    z-index: 1;
    max-width: 320px;
    line-height: 1.6;
}}
.feature-pill {{
    background: rgba(255,255,255,0.15);
    border: 1px solid rgba(255,255,255,0.25);
    border-radius: 100px;
    padding: 8px 20px;
    color: white;
    font-size: 0.85rem;
    font-weight: 500;
    margin: 6px;
    display: inline-block;
    z-index: 1;
}}
.login-card {{
    width: 100%;
    max-width: 420px;
}}
.login-title {{
    font-size: 2rem;
    font-weight: 800;
    color: {T['text']};
    margin-bottom: 6px;
}}
.login-sub {{
    font-size: 0.95rem;
    color: {T['subtext']};
    margin-bottom: 32px;
}}
.custom-input {{
    width: 100%;
    padding: 14px 16px;
    border: 1.5px solid {T['border']};
    border-radius: 12px;
    background: {T['input_bg']};
    color: {T['text']};
    font-size: 0.95rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    outline: none;
    transition: border-color 0.2s;
    margin-bottom: 16px;
}}
.custom-input:focus {{ border-color: {T['accent']}; }}
.btn-primary {{
    width: 100%;
    padding: 14px;
    background: linear-gradient(135deg, #4f46e5, #06b6d4);
    color: white;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 700;
    cursor: pointer;
    font-family: 'Plus Jakarta Sans', sans-serif;
    transition: opacity 0.2s;
    margin-top: 8px;
}}
.btn-primary:hover {{ opacity: 0.9; }}
.divider {{
    display: flex;
    align-items: center;
    margin: 24px 0;
    color: {T['subtext']};
    font-size: 0.85rem;
}}
.divider::before, .divider::after {{
    content: '';
    flex: 1;
    height: 1px;
    background: {T['border']};
    margin: 0 12px;
}}
.demo-btn {{
    width: 100%;
    padding: 12px;
    background: {T['card']};
    color: {T['text']};
    border: 1.5px solid {T['border']};
    border-radius: 12px;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    font-family: 'Plus Jakarta Sans', sans-serif;
}}
.theme-toggle {{
    position: fixed;
    top: 20px;
    right: 20px;
    background: {T['card']};
    border: 1.5px solid {T['border']};
    border-radius: 100px;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 0.85rem;
    color: {T['text']};
    z-index: 1000;
}}
.lang-toggle {{
    position: fixed;
    top: 20px;
    right: 120px;
    background: {T['card']};
    border: 1.5px solid {T['border']};
    border-radius: 100px;
    padding: 8px 16px;
    cursor: pointer;
    font-size: 0.85rem;
    color: {T['text']};
    z-index: 1000;
}}
.stat-box {{
    background: rgba(255,255,255,0.1);
    border-radius: 16px;
    padding: 20px 28px;
    text-align: center;
    z-index: 1;
    margin: 8px;
}}
.stat-num {{
    font-size: 1.8rem;
    font-weight: 800;
    color: white;
}}
.stat-label {{
    font-size: 0.8rem;
    color: rgba(255,255,255,0.7);
    margin-top: 4px;
}}
</style>
""", unsafe_allow_html=True)

# ── Language ───────────────────────────────────────────────────────────────────
LANG = {
    "EN": {
        "welcome": "Welcome back",
        "sub": "Sign in to your RouteIQ account",
        "email": "Email address",
        "pass": "Password",
        "signin": "Sign In",
        "or": "or continue with",
        "demo": "Try Demo Account",
        "tagline": "Smart AI-powered delivery optimization for modern logistics teams",
        "feat1": "AI Route Optimization",
        "feat2": "Real-time Tracking",
        "feat3": "Cost Analytics",
        "s1": "30%", "l1": "Cost Reduction",
        "s2": "2M+", "l2": "Deliveries Tracked",
        "s3": "98%", "l3": "On-time Rate",
    },
    "TA": {
        "welcome": "மீண்டும் வரவேற்கிறோம்",
        "sub": "உங்கள் RouteIQ கணக்கில் உள்நுழையவும்",
        "email": "மின்னஞ்சல் முகவரி",
        "pass": "கடவுச்சொல்",
        "signin": "உள்நுழை",
        "or": "அல்லது தொடரவும்",
        "demo": "டெமோ கணக்கை முயற்சிக்கவும்",
        "tagline": "நவீன தளவாட குழுக்களுக்கான AI-இயங்கும் டெலிவரி தேர்வு",
        "feat1": "AI பாதை தேர்வு",
        "feat2": "நிகழ்நேர கண்காணிப்பு",
        "feat3": "செலவு பகுப்பாய்வு",
        "s1": "30%", "l1": "செலவு குறைப்பு",
        "s2": "2M+", "l2": "டெலிவரிகள்",
        "s3": "98%", "l3": "சரியான நேரம்",
    }
}
L = LANG[st.session_state.lang]

# ── If already logged in, redirect ────────────────────────────────────────────
if st.session_state.logged_in:
    st.switch_page("pages/1_Dashboard.py")
    st.stop()

# ── Theme & Lang Toggle ────────────────────────────────────────────────────────
col_t1, col_t2, col_t3 = st.columns([8, 1, 1])
with col_t2:
    if st.button("🌐 " + st.session_state.lang):
        st.session_state.lang = "TA" if st.session_state.lang == "EN" else "EN"
        st.rerun()
with col_t3:
    if st.button("🌙" if not st.session_state.dark_mode else "☀️"):
        st.session_state.dark_mode = not st.session_state.dark_mode
        st.rerun()

# ── Login Layout ───────────────────────────────────────────────────────────────
left, right = st.columns([1, 1])

with left:
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #4f46e5 0%, #06b6d4 100%);
                min-height: 92vh; border-radius: 24px; padding: 60px 50px;
                display: flex; flex-direction: column; justify-content: center;
                position: relative; overflow: hidden;">
        <div style="position:absolute;width:350px;height:350px;background:rgba(255,255,255,0.05);
                    border-radius:50%;top:-100px;right:-100px;"></div>
        <div style="position:absolute;width:250px;height:250px;background:rgba(255,255,255,0.05);
                    border-radius:50%;bottom:-60px;left:-60px;"></div>
        <div style="font-size:3rem;font-weight:800;color:white;letter-spacing:-1px;margin-bottom:6px;">
            🚚 RouteIQ
        </div>
        <div style="font-size:1.1rem;color:rgba(255,255,255,0.85);margin-bottom:40px;line-height:1.6;max-width:340px;">
            {L['tagline']}
        </div>
        <div style="margin-bottom:40px;">
            <span class="feature-pill">✦ {L['feat1']}</span>
            <span class="feature-pill">✦ {L['feat2']}</span>
            <span class="feature-pill">✦ {L['feat3']}</span>
        </div>
        <div style="display:flex;gap:16px;flex-wrap:wrap;">
            <div class="stat-box">
                <div class="stat-num">{L['s1']}</div>
                <div class="stat-label">{L['l1']}</div>
            </div>
            <div class="stat-box">
                <div class="stat-num">{L['s2']}</div>
                <div class="stat-label">{L['l2']}</div>
            </div>
            <div class="stat-box">
                <div class="stat-num">{L['s3']}</div>
                <div class="stat-label">{L['l3']}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown(f"""
    <div style="display:flex;flex-direction:column;justify-content:center;
                align-items:center;min-height:92vh;padding:40px;">
        <div style="width:100%;max-width:400px;">
            <div style="font-size:2rem;font-weight:800;color:{T['text']};margin-bottom:6px;">
                {L['welcome']} 👋
            </div>
            <div style="font-size:0.95rem;color:{T['subtext']};margin-bottom:36px;">
                {L['sub']}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Center the form
    _, form_col, _ = st.columns([0.5, 3, 0.5])
    with form_col:
        email = st.text_input("", placeholder=L['email'], label_visibility="collapsed")
        password = st.text_input("", placeholder=L['pass'], type="password", label_visibility="collapsed")

        col_a, col_b = st.columns(2)
        with col_a:
            if st.button(L['signin'], use_container_width=True, type="primary"):
                if email and password:
                    st.session_state.logged_in = True
                    st.session_state.username = email.split("@")[0].title()
                    st.rerun()
                else:
                    st.error("Please enter email and password")
        with col_b:
            if st.button(L['demo'], use_container_width=True):
                st.session_state.logged_in = True
                st.session_state.username = "Demo User"
                st.rerun()

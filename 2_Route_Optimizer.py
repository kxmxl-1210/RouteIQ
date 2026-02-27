import streamlit as st
import folium
from streamlit_folium import folium_static
import numpy as np
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

st.set_page_config(page_title="Route Optimizer — RouteIQ", page_icon="🗺️", layout="wide")
if 'logged_in' not in st.session_state or not st.session_state.logged_in:
    st.switch_page("app.py")
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

CITY_COORDS = {
    'Chennai':(13.0827,80.2707),'Mumbai':(19.0760,72.8777),'Delhi':(28.6139,77.2090),
    'Bangalore':(12.9716,77.5946),'Hyderabad':(17.3850,78.4867),'Kolkata':(22.5726,88.3639),
    'Pune':(18.5204,73.8567),'Ahmedabad':(23.0225,72.5714),'Coimbatore':(11.0168,76.9558),
    'Madurai':(9.9252,78.1198),'Jaipur':(26.9124,75.7873),'Surat':(21.1702,72.8311),
    'Lucknow':(26.8467,80.9462),'Nagpur':(21.1458,79.0882),'Visakhapatnam':(17.6868,83.2185),
}

def haversine(c1, c2):
    R = 6371
    lat1,lon1 = np.radians(c1); lat2,lon2 = np.radians(c2)
    dlat=lat2-lat1; dlon=lon2-lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return R * 2 * np.arcsin(np.sqrt(a))

def optimize(cities, start):
    unvisited = cities.copy()
    if start in unvisited: unvisited.remove(start)
    route = [start]; total = 0; current = start
    while unvisited:
        nearest = min(unvisited, key=lambda c: haversine(CITY_COORDS[current], CITY_COORDS[c]))
        total += haversine(CITY_COORDS[current], CITY_COORDS[nearest])
        route.append(nearest); unvisited.remove(nearest); current = nearest
    return route, round(total, 1)

def original_dist(cities):
    total = 0
    for i in range(len(cities)-1):
        total += haversine(CITY_COORDS[cities[i]], CITY_COORDS[cities[i+1]])
    return round(total, 1)

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
.savings-row {{ display:flex; justify-content:space-between; align-items:center; padding:12px 0; border-bottom:1px solid {T['border']}; }}
.savings-row:last-child {{ border-bottom:none; }}
.savings-label {{ font-size:0.85rem; color:{T['subtext']}; }}
.savings-value {{ font-size:1rem; font-weight:700; color:{T['text']}; }}
.savings-value.green {{ color:#10b981; }}
.big-saving {{ background:linear-gradient(135deg,#10b98115,#06b6d415); border:1px solid #10b98130; border-radius:16px; padding:20px 24px; text-align:center; margin:16px 0; }}
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

title = "பாதை தேர்வு" if lang=="TA" else "Route Optimizer"
sub = "சிறந்த டெலிவரி பாதையை கண்டுபிடிக்கவும்" if lang=="TA" else "Find the most efficient delivery path and see your savings"
st.markdown(f'<div class="page-title">🗺️ {title}</div><div class="page-sub">{sub}</div>', unsafe_allow_html=True)

left, right = st.columns([1, 1.6])

with left:
    st.markdown(f'<div class="card">', unsafe_allow_html=True)
    all_cities = list(CITY_COORDS.keys())
    start = st.selectbox("🏭 " + ("தொடக்க நகரம்" if lang=="TA" else "Starting Warehouse"), all_cities)
    stops = st.multiselect(
        "📍 " + ("டெலிவரி நிறுத்தங்கள்" if lang=="TA" else "Delivery Stops"),
        [c for c in all_cities if c != start],
        default=['Madurai','Coimbatore','Bangalore','Hyderabad']
    )
    optimize_btn = st.button("🚀 " + ("பாதையை தேர்வு செய்" if lang=="TA" else "Optimize Route"), use_container_width=True, type="primary")
    st.markdown('</div>', unsafe_allow_html=True)

    if optimize_btn and len(stops) >= 2:
        cities = [start] + stops
        opt_route, opt_dist = optimize(cities, start)
        orig_dist = original_dist(cities)
        savings_km = round(orig_dist - opt_dist, 1)
        savings_pct = round(savings_km / orig_dist * 100, 1) if orig_dist > 0 else 0
        fuel_saved = round(savings_km * 0.12, 1)
        cost_saved = round(fuel_saved * 101, 0)
        petrol_money = round(savings_km * 12.12, 0)

        st.session_state['route_data'] = {
            'orig': cities, 'opt': opt_route,
            'orig_dist': orig_dist, 'opt_dist': opt_dist,
            'savings_km': savings_km, 'savings_pct': savings_pct,
            'fuel_saved': fuel_saved, 'cost_saved': cost_saved,
            'petrol_money': petrol_money
        }

    if 'route_data' in st.session_state:
        r = st.session_state['route_data']
        st.markdown(f"""
        <div class="big-saving">
            <div style="font-size:2rem;font-weight:800;color:#10b981;">₹{r['cost_saved']:,.0f}</div>
            <div style="font-size:0.85rem;color:{T['subtext']};margin-top:4px;">{"இந்த பயணத்தில் சேமிப்பு" if lang=="TA" else "Total savings on this trip"}</div>
        </div>
        <div class="card">
            <div class="savings-row">
                <span class="savings-label">{"அசல் தூரம்" if lang=="TA" else "Original Distance"}</span>
                <span class="savings-value">{r['orig_dist']} km</span>
            </div>
            <div class="savings-row">
                <span class="savings-label">{"தேர்வு செய்யப்பட்ட தூரம்" if lang=="TA" else "Optimized Distance"}</span>
                <span class="savings-value green">{r['opt_dist']} km</span>
            </div>
            <div class="savings-row">
                <span class="savings-label">{"தூர சேமிப்பு" if lang=="TA" else "Distance Saved"}</span>
                <span class="savings-value green">{r['savings_km']} km ({r['savings_pct']}%)</span>
            </div>
            <div class="savings-row">
                <span class="savings-label">{"எரிபொருள் சேமிப்பு" if lang=="TA" else "Fuel Saved"}</span>
                <span class="savings-value green">{r['fuel_saved']} Litres</span>
            </div>
            <div class="savings-row">
                <span class="savings-label">{"பெட்ரோல் செலவு சேமிப்பு" if lang=="TA" else "Petrol Cost Saved"}</span>
                <span class="savings-value green">₹{r['petrol_money']:,.0f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"**{'அசல் பாதை' if lang=='TA' else 'Original Route'}:** " + " → ".join(r['orig']))
        st.markdown(f"**{'தேர்வு பாதை' if lang=='TA' else 'Optimized Route'}:** " + " → ".join(r['opt']))
    elif optimize_btn:
        st.warning("Please select at least 2 delivery stops.")

with right:
    st.markdown(f'<div style="font-size:1rem;font-weight:700;color:{T["text"]};margin-bottom:12px;">🗺️ {"பாதை வரைபடம்" if lang=="TA" else "Route Map"}</div>', unsafe_allow_html=True)
    tile = 'CartoDB dark_matter' if st.session_state.dark_mode else 'CartoDB positron'
    m = folium.Map(location=[18, 78], zoom_start=5, tiles=tile)

    if 'route_data' in st.session_state:
        r = st.session_state['route_data']
        orig_coords = [CITY_COORDS[c] for c in r['orig']]
        opt_coords = [CITY_COORDS[c] for c in r['opt']]
        folium.PolyLine(orig_coords, color='#ef4444', weight=2.5, opacity=0.5,
                        dash_array='8', tooltip="Original Route").add_to(m)
        folium.PolyLine(opt_coords, color='#4f46e5', weight=3.5, opacity=0.9,
                        tooltip="Optimized Route").add_to(m)
        for i, city in enumerate(r['opt']):
            lat, lon = CITY_COORDS[city]
            color = 'green' if i == 0 else 'blue' if i == len(r['opt'])-1 else 'lightblue'
            folium.Marker([lat, lon], tooltip=f"Stop {i+1}: {city}",
                icon=folium.Icon(color=color, icon='circle', prefix='fa')).add_to(m)
    else:
        for city, (lat, lon) in CITY_COORDS.items():
            folium.CircleMarker([lat, lon], radius=6, color='#4f46e5',
                fill=True, fill_opacity=0.6, tooltip=city).add_to(m)

    folium_static(m, height=520)

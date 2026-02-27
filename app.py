"""
RouteIQ — AI-Powered Logistics & Delivery Optimization Dashboard
Run: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import numpy as np
import folium
from streamlit_folium import folium_static
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

from route_optimizer import optimize_and_compare, get_route_coordinates, CITY_COORDS
from demand_forecast import forecast_demand, get_all_zones_summary, generate_historical_data
from delay_model import predict_delay, train_model, generate_sample_data

# ── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RouteIQ — Logistics AI",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Custom CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

    html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

    .main { background: #0a0e1a; }
    .stApp { background: linear-gradient(135deg, #0a0e1a 0%, #0d1525 100%); }

    .metric-card {
        background: linear-gradient(135deg, #1a2035 0%, #1e2840 100%);
        border: 1px solid #2a3a5c;
        border-radius: 16px;
        padding: 20px 24px;
        text-align: center;
        box-shadow: 0 4px 24px rgba(0,0,0,0.3);
    }
    .metric-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #00d4ff;
        font-family: 'JetBrains Mono', monospace;
    }
    .metric-label {
        font-size: 0.8rem;
        color: #8899bb;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 4px;
    }
    .metric-delta {
        font-size: 0.9rem;
        color: #00ff88;
        margin-top: 6px;
    }

    .section-header {
        font-size: 1.4rem;
        font-weight: 700;
        color: #e8f0ff;
        margin: 28px 0 16px 0;
        padding-bottom: 8px;
        border-bottom: 2px solid #00d4ff33;
    }

    .risk-high   { background:#ff4d4d22; border:1px solid #ff4d4d55; border-radius:12px; padding:16px; }
    .risk-medium { background:#ffaa0022; border:1px solid #ffaa0055; border-radius:12px; padding:16px; }
    .risk-low    { background:#00ff8822; border:1px solid #00ff8855; border-radius:12px; padding:16px; }

    .stSelectbox label, .stSlider label, .stNumberInput label,
    .stMultiSelect label { color: #aabbdd !important; }

    div[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d1525 0%, #111827 100%);
        border-right: 1px solid #1e2840;
    }

    .savings-box {
        background: linear-gradient(135deg, #003322, #001a11);
        border: 1px solid #00ff8844;
        border-radius: 16px;
        padding: 20px;
        margin: 12px 0;
    }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚚 RouteIQ")
    st.markdown("<small style='color:#667799'>AI Logistics Optimization</small>", unsafe_allow_html=True)
    st.divider()
    page = st.radio("Navigation", [
        "📊 Dashboard Overview",
        "🗺️ Route Optimizer",
        "⚠️ Delay Predictor",
        "📈 Demand Forecasting",
    ])
    st.divider()
    st.markdown("<small style='color:#445577'>Built for TN IMPACT Hackathon 2026</small>", unsafe_allow_html=True)


# ── Train model (cached) ───────────────────────────────────────────────────────
@st.cache_resource
def load_model():
    df = generate_sample_data(3000)
    model, acc = train_model(df)
    return model, acc

with st.spinner("🔧 Loading AI models..."):
    model, model_acc = load_model()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 1 — DASHBOARD OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
if page == "📊 Dashboard Overview":
    st.markdown("# 📊 RouteIQ — Operations Dashboard")
    st.markdown(f"<small style='color:#556688'>Live as of {datetime.now().strftime('%d %b %Y, %I:%M %p')}</small>", unsafe_allow_html=True)

    # KPI Row
    col1, col2, col3, col4 = st.columns(4)
    kpis = [
        ("1,284", "Active Deliveries", "+8.2% today"),
        ("142",   "At-Risk Shipments", "🔴 Needs attention"),
        ("₹2.4L", "Cost Saved (Today)", "+12% vs yesterday"),
        (f"{model_acc:.0%}", "Model Accuracy",  "Gradient Boosting"),
    ]
    for col, (val, label, delta) in zip([col1, col2, col3, col4], kpis):
        col.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{val}</div>
            <div class="metric-label">{label}</div>
            <div class="metric-delta">{delta}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        st.markdown('<div class="section-header">🗺️ Live Delivery Network</div>', unsafe_allow_html=True)
        m = folium.Map(location=[20.5937, 78.9629], zoom_start=5,
                       tiles='CartoDB dark_matter')
        cities_list = list(CITY_COORDS.keys())
        for city, (lat, lon) in CITY_COORDS.items():
            risk = np.random.choice(['high', 'medium', 'low'], p=[0.15, 0.35, 0.5])
            color = {'high': 'red', 'medium': 'orange', 'low': 'green'}[risk]
            count = np.random.randint(20, 200)
            folium.CircleMarker(
                [lat, lon], radius=8, color=color, fill=True, fill_opacity=0.8,
                popup=f"<b>{city}</b><br>Deliveries: {count}<br>Risk: {risk.upper()}"
            ).add_to(m)
        # Draw sample route
        route_cities = ['Chennai', 'Bangalore', 'Hyderabad', 'Pune', 'Mumbai']
        route_coords = [CITY_COORDS[c] for c in route_cities]
        folium.PolyLine(route_coords, color='#00d4ff', weight=2.5, opacity=0.7,
                        tooltip="Sample Optimized Route").add_to(m)
        folium_static(m, height=400)

    with col_right:
        st.markdown('<div class="section-header">📦 Zone Demand Status</div>', unsafe_allow_html=True)
        zone_df = get_all_zones_summary()
        fig = px.bar(
            zone_df.head(8), x='Today Demand', y='Zone', orientation='h',
            color='Change %',
            color_continuous_scale=['#00ff88', '#ffaa00', '#ff4d4d'],
            template='plotly_dark',
            labels={'Today Demand': 'Deliveries Today'}
        )
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            height=380,
            margin=dict(l=0, r=10, t=10, b=10),
            font=dict(color='#aabbdd'),
            coloraxis_showscale=False
        )
        st.plotly_chart(fig, use_container_width=True)

    # Bottom row — weekly trend
    st.markdown('<div class="section-header">📈 Weekly Delivery Trend — All Zones</div>', unsafe_allow_html=True)
    hist_data = []
    for zone in ['Chennai', 'Mumbai', 'Bangalore', 'Delhi']:
        df_h = generate_historical_data(zone, 30)
        hist_data.append(df_h)
    all_hist = pd.concat(hist_data)

    fig2 = px.line(all_hist, x='date', y='demand', color='zone',
                   template='plotly_dark',
                   color_discrete_sequence=['#00d4ff', '#00ff88', '#ffaa00', '#ff6b6b'])
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13,21,37,0.5)',
        height=260,
        margin=dict(l=0, r=0, t=10, b=10),
        font=dict(color='#aabbdd'),
        legend=dict(orientation='h', y=1.1)
    )
    fig2.update_xaxes(gridcolor='#1e2840')
    fig2.update_yaxes(gridcolor='#1e2840')
    st.plotly_chart(fig2, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 2 — ROUTE OPTIMIZER
# ══════════════════════════════════════════════════════════════════════════════
elif page == "🗺️ Route Optimizer":
    st.markdown("# 🗺️ Delivery Route Optimizer")
    st.markdown("Select your delivery stops and RouteIQ will find the most efficient route.")

    all_cities = list(CITY_COORDS.keys())

    col1, col2 = st.columns([1, 1.5])

    with col1:
        st.markdown('<div class="section-header">⚙️ Configure Route</div>', unsafe_allow_html=True)
        start_city = st.selectbox("🏭 Starting Warehouse / Hub", all_cities, index=0)
        selected_cities = st.multiselect(
            "📍 Select Delivery Stops",
            [c for c in all_cities if c != start_city],
            default=['Madurai', 'Coimbatore', 'Bangalore', 'Hyderabad']
        )

        if st.button("🚀 Optimize Route", use_container_width=True, type="primary"):
            if len(selected_cities) < 2:
                st.warning("Please select at least 2 delivery stops.")
            else:
                cities_to_optimize = [start_city] + selected_cities
                result = optimize_and_compare(cities_to_optimize, start=start_city)
                st.session_state['route_result'] = result

    if 'route_result' in st.session_state:
        result = st.session_state['route_result']

        with col1:
            st.markdown(f"""
            <div class="savings-box">
                <div style="font-size:1.1rem;font-weight:700;color:#00ff88;margin-bottom:12px">💰 Optimization Results</div>
                <div style="color:#aabbdd;font-size:0.9rem">
                    📏 Original Distance: <b style="color:white">{result['original_distance_km']} km</b><br>
                    🚀 Optimized Distance: <b style="color:#00d4ff">{result['optimized_distance_km']} km</b><br>
                    ✅ Distance Saved: <b style="color:#00ff88">{result['savings_km']} km ({result['savings_pct']}%)</b><br>
                    ⛽ Fuel Saved: <b style="color:#00ff88">{result['estimated_fuel_saved_l']} L</b><br>
                    💵 Cost Saved: <b style="color:#00ff88">₹{result['estimated_cost_saved_inr']:,.0f}</b>
                </div>
            </div>""", unsafe_allow_html=True)

            st.markdown("**Original Route:**")
            st.code(" → ".join(result['original_route']), language=None)
            st.markdown("**Optimized Route:**")
            st.code(" → ".join(result['optimized_route']), language=None)

        with col2:
            st.markdown('<div class="section-header">🗺️ Route Map</div>', unsafe_allow_html=True)
            m2 = folium.Map(location=[18, 78], zoom_start=5, tiles='CartoDB dark_matter')

            # Original route (red dashed)
            orig_coords = get_route_coordinates(result['original_route'])
            folium.PolyLine(orig_coords, color='#ff4d4d', weight=2,
                            opacity=0.5, dash_array='8', tooltip="Original Route").add_to(m2)

            # Optimized route (cyan)
            opt_coords = get_route_coordinates(result['optimized_route'])
            folium.PolyLine(opt_coords, color='#00d4ff', weight=3.5,
                            opacity=0.9, tooltip="Optimized Route").add_to(m2)

            # Markers
            for i, city in enumerate(result['optimized_route']):
                lat, lon = CITY_COORDS[city]
                color = 'green' if i == 0 else 'blue'
                icon = 'home' if i == 0 else 'truck'
                folium.Marker([lat, lon],
                    popup=f"Stop {i+1}: {city}",
                    tooltip=city,
                    icon=folium.Icon(color=color, icon='circle', prefix='fa')
                ).add_to(m2)

            folium_static(m2, height=500)


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 3 — DELAY PREDICTOR
# ══════════════════════════════════════════════════════════════════════════════
elif page == "⚠️ Delay Predictor":
    st.markdown("# ⚠️ Delivery Delay Predictor")
    st.markdown("Enter shipment details and the AI will predict delay risk in real time.")

    all_cities = list(CITY_COORDS.keys())

    col1, col2 = st.columns(2)
    with col1:
        seller_city   = st.selectbox("📦 Seller / Origin City", all_cities, index=0)
        customer_city = st.selectbox("🏠 Customer / Destination City", all_cities, index=3)
        distance_km   = st.slider("📏 Distance (km)", 50, 2500, 800)
        weight_g      = st.number_input("⚖️ Package Weight (grams)", 100, 30000, 2500)

    with col2:
        freight_value = st.number_input("💰 Freight Value (₹)", 10.0, 2000.0, 150.0)
        item_count    = st.slider("📦 Number of Items", 1, 20, 3)
        order_dow     = st.selectbox("📅 Order Day", ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])
        order_month   = st.selectbox("📆 Order Month", list(range(1,13)), index=datetime.today().month - 1)

    dow_map = {"Mon":0,"Tue":1,"Wed":2,"Thu":3,"Fri":4,"Sat":5,"Sun":6}

    if st.button("🔍 Predict Delay Risk", use_container_width=True, type="primary"):
        prediction, prob = predict_delay(
            distance_km, weight_g, dow_map[order_dow], order_month,
            freight_value, item_count, seller_city, customer_city
        )

        risk_class = "risk-high" if prob > 0.6 else "risk-medium" if prob > 0.35 else "risk-low"
        st.markdown(f"""
        <div class="{risk_class}" style="margin-top:20px; text-align:center">
            <div style="font-size:1.8rem; font-weight:700; margin-bottom:8px">{prediction}</div>
            <div style="font-size:1.1rem; color:#aabbdd">Delay Probability: <b style="font-size:1.4rem">{prob:.1%}</b></div>
        </div>""", unsafe_allow_html=True)

        # Gauge chart
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=round(prob * 100, 1),
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Delay Risk Score", 'font': {'color': '#aabbdd'}},
            number={'suffix': '%', 'font': {'color': '#00d4ff', 'size': 48}},
            gauge={
                'axis': {'range': [0, 100], 'tickcolor': '#556688'},
                'bar': {'color': '#ff4d4d' if prob > 0.6 else '#ffaa00' if prob > 0.35 else '#00ff88'},
                'bgcolor': '#1a2035',
                'steps': [
                    {'range': [0, 35],  'color': '#00ff8811'},
                    {'range': [35, 60], 'color': '#ffaa0011'},
                    {'range': [60, 100],'color': '#ff4d4d11'},
                ],
                'threshold': {'line': {'color': 'white', 'width': 2}, 'value': prob * 100}
            }
        ))
        fig.update_layout(
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#aabbdd'),
            height=300, margin=dict(t=40, b=0)
        )
        st.plotly_chart(fig, use_container_width=True)

        # Recommendations
        st.markdown('<div class="section-header">💡 AI Recommendations</div>', unsafe_allow_html=True)
        if prob > 0.6:
            recs = ["🚨 Alert the customer proactively about possible delay",
                    "📦 Switch to express courier for this shipment",
                    "🔄 Consider rerouting via a closer hub city",
                    "📍 Assign priority tracking & real-time SMS updates"]
        elif prob > 0.35:
            recs = ["⚠️ Monitor this shipment closely",
                    "📱 Send estimated delivery confirmation to customer",
                    "🗓️ Consider dispatching 1 day earlier next time"]
        else:
            recs = ["✅ Shipment looks good — no action needed",
                    "📊 Standard tracking is sufficient",
                    "🎯 Estimated to arrive within delivery window"]
        for r in recs:
            st.markdown(f"- {r}")

    # Bulk Risk Table
    st.markdown('<div class="section-header">📋 Bulk Shipment Risk Overview (Sample)</div>', unsafe_allow_html=True)
    sample_df = generate_sample_data(200)
    sample_df['Risk'] = sample_df['is_late'].map({1: '🔴 High', 0: '🟢 Low'})
    display_cols = ['distance_km', 'weight_g', 'freight_value', 'item_count', 'Risk']
    st.dataframe(
        sample_df[display_cols].rename(columns={
            'distance_km':'Distance (km)', 'weight_g':'Weight (g)',
            'freight_value':'Freight (₹)', 'item_count':'Items'
        }).head(15),
        use_container_width=True
    )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE 4 — DEMAND FORECASTING
# ══════════════════════════════════════════════════════════════════════════════
elif page == "📈 Demand Forecasting":
    st.markdown("# 📈 Zone Demand Forecasting")
    st.markdown("AI-powered delivery demand forecasts to help warehouses stock & staff efficiently.")

    col1, col2 = st.columns([1, 2])
    with col1:
        zone = st.selectbox("🌆 Select Zone / City", list(CITY_COORDS.keys()), index=0)
        forecast_days = st.slider("📅 Forecast Days", 3, 14, 7)

    df_forecast, df_hist = forecast_demand(zone, forecast_days)

    # Combine hist + forecast for chart
    df_hist_plot = df_hist.tail(30).copy()
    df_hist_plot['type'] = 'Historical'
    df_forecast_plot = df_forecast.copy()
    df_forecast_plot['type'] = 'Forecast'
    df_combined = pd.concat([df_hist_plot[['date','demand','type']],
                              df_forecast_plot[['date','demand','type']]])

    fig = px.line(df_combined, x='date', y='demand', color='type',
                  template='plotly_dark',
                  color_discrete_map={'Historical': '#00d4ff', 'Forecast': '#00ff88'},
                  markers=True)
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13,21,37,0.5)',
        height=350,
        font=dict(color='#aabbdd'),
        legend=dict(orientation='h', y=1.1),
        margin=dict(l=0, r=0, t=10, b=10),
        title=f"{zone} — Demand Forecast"
    )
    fig.update_xaxes(gridcolor='#1e2840')
    fig.update_yaxes(gridcolor='#1e2840')

    with col2:
        st.plotly_chart(fig, use_container_width=True)

    # Forecast table
    st.markdown('<div class="section-header">📋 Forecast Table</div>', unsafe_allow_html=True)
    df_display = df_forecast.copy()
    df_display['date'] = df_display['date'].dt.strftime('%a, %d %b')
    df_display['demand'] = df_display['demand'].astype(int)
    avg = df_hist['demand'].tail(14).mean()
    df_display['vs Baseline'] = df_display['demand'].apply(
        lambda x: f"{'↑' if x > avg else '↓'} {abs(x - avg):.0f} ({(x-avg)/avg*100:+.1f}%)")
    df_display['Action'] = df_display['demand'].apply(
        lambda x: "📦 Stock Up" if x > avg * 1.2 else "✅ Normal" if x > avg * 0.9 else "📉 Reduce Stock")
    st.dataframe(df_display[['date','demand','vs Baseline','Action']].rename(
        columns={'date':'Date','demand':'Expected Deliveries'}),
        use_container_width=True)

    # All zones heatmap
    st.markdown('<div class="section-header">🗺️ All Zones — Demand Summary</div>', unsafe_allow_html=True)
    zone_summary = get_all_zones_summary()
    fig2 = px.bar(zone_summary, x='Zone', y='Today Demand', color='Change %',
                  color_continuous_scale=['#00ff88','#ffaa00','#ff4d4d'],
                  template='plotly_dark', text='Status')
    fig2.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(13,21,37,0.5)',
        height=300,
        font=dict(color='#aabbdd'),
        margin=dict(l=0, r=0, t=10, b=10),
        coloraxis_showscale=False
    )
    fig2.update_xaxes(gridcolor='#1e2840')
    fig2.update_yaxes(gridcolor='#1e2840')
    st.plotly_chart(fig2, use_container_width=True)

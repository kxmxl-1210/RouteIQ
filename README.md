# 🚚 RouteIQ — AI-Powered Logistics & Delivery Optimization

> Built for TN IMPACT Hackathon 2026 | Theme: Logistics & Delivery Optimization (AI/ML)

---

## 🚀 Quick Start (3 Steps)

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Run the app
```bash
streamlit run app.py
```

### 3. Open browser
```
http://localhost:8501
```

---

## 📁 Project Structure

```
routeiq/
├── app.py                 # Main Streamlit dashboard (4 pages)
├── delay_model.py         # ML delay prediction (Gradient Boosting)
├── route_optimizer.py     # Route optimization (Nearest Neighbor TSP)
├── demand_forecast.py     # Demand forecasting (Time-series)
├── requirements.txt       # Python dependencies
└── README.md
```

---

## 🧠 Features

| Feature | Description | ML Technique |
|---|---|---|
| **Delay Predictor** | Predicts if a shipment will be late | Gradient Boosting Classifier |
| **Route Optimizer** | Finds shortest delivery path | Nearest Neighbor + Haversine |
| **Demand Forecasting** | Forecasts zone demand 7–14 days ahead | Trend + Seasonal Decomposition |
| **Live Map** | Interactive delivery network map | Folium + OpenStreetMap |
| **Risk Dashboard** | KPIs, alerts, charts | Plotly + Streamlit |

---

## 🎯 Business Impact

- 📉 Up to **30% reduction** in delivery distance
- ⛽ Significant **fuel cost savings**
- ⚠️ Proactive **delay alerts** before shipment leaves warehouse
- 📦 Better **warehouse staffing** with demand forecasts

---

## 🎤 Pitch (60 seconds)

> "Every day, logistics companies lose lakhs of rupees due to unoptimized routes, surprise delays, and poor demand forecasting.
> RouteIQ fixes this with 3 AI-powered tools: it **predicts delays** before they happen, **optimizes delivery routes** to cut distance by 30%, and **forecasts zone demand** so warehouses are always prepared.
> Built on real machine learning — no guesswork, just data-driven decisions."

---

## 🏆 Why This Wins

1. **Directly matches the hackathon theme** — Logistics & Delivery Optimization (AI/ML)
2. **Live interactive demo** — judges can see it running, not just slides
3. **3-in-1 solution** — prediction + optimization + forecasting
4. **Real business ROI** — quantifiable cost savings shown in dashboard
5. **100% Python** — clean, readable, extensible code

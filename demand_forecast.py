"""
RouteIQ - Demand Forecasting
Uses simple time-series simulation + trend analysis for zone-level demand forecasting
(Lightweight version — no Prophet needed, works out of the box)
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


ZONES = {
    'Chennai':     {'base': 320, 'growth': 0.03},
    'Mumbai':      {'base': 580, 'growth': 0.04},
    'Delhi':       {'base': 620, 'growth': 0.035},
    'Bangalore':   {'base': 490, 'growth': 0.045},
    'Hyderabad':   {'base': 410, 'growth': 0.038},
    'Kolkata':     {'base': 380, 'growth': 0.025},
    'Pune':        {'base': 340, 'growth': 0.04},
    'Coimbatore':  {'base': 210, 'growth': 0.028},
    'Madurai':     {'base': 180, 'growth': 0.022},
    'Ahmedabad':   {'base': 290, 'growth': 0.033},
}


def generate_historical_data(zone, days=60):
    """Generate 60 days of historical delivery demand for a zone."""
    np.random.seed(hash(zone) % 2**32)
    base = ZONES.get(zone, {}).get('base', 200)
    growth = ZONES.get(zone, {}).get('growth', 0.03)

    dates = [datetime.today() - timedelta(days=days - i) for i in range(days)]
    demand = []
    for i, date in enumerate(dates):
        trend = base * (1 + growth * i / 30)
        seasonal = 1.3 if date.weekday() in [4, 5] else 1.0  # Fri/Sat spike
        monthly = 1.2 if date.day >= 25 else 1.0             # Month-end spike
        noise = np.random.normal(1.0, 0.08)
        demand.append(max(0, int(trend * seasonal * monthly * noise)))

    return pd.DataFrame({'date': dates, 'demand': demand, 'zone': zone})


def forecast_demand(zone, forecast_days=7):
    """Forecast next N days of demand for a zone."""
    hist = generate_historical_data(zone)
    recent_avg = hist['demand'].tail(14).mean()
    growth = ZONES.get(zone, {}).get('growth', 0.03)

    forecasted = []
    for i in range(forecast_days):
        date = datetime.today() + timedelta(days=i + 1)
        trend_factor = 1 + growth * (i / 30)
        seasonal = 1.3 if date.weekday() in [4, 5] else 1.0
        monthly = 1.2 if date.day >= 25 else 1.0
        noise = np.random.normal(1.0, 0.05)
        val = int(recent_avg * trend_factor * seasonal * monthly * noise)
        forecasted.append({'date': date, 'demand': val, 'zone': zone})

    return pd.DataFrame(forecasted), hist


def get_all_zones_summary():
    """Get today's demand summary for all zones."""
    today = datetime.today()
    summary = []
    for zone in ZONES:
        np.random.seed((hash(zone) + today.day) % 2**32)
        base = ZONES[zone]['base']
        seasonal = 1.3 if today.weekday() in [4, 5] else 1.0
        noise = np.random.normal(1.0, 0.06)
        current = int(base * seasonal * noise)
        status = "🔴 High" if current > base * 1.2 else \
                 "🟡 Medium" if current > base * 0.9 else "🟢 Normal"
        summary.append({
            'Zone': zone,
            'Today Demand': current,
            'Baseline': base,
            'Status': status,
            'Change %': round((current - base) / base * 100, 1)
        })
    return pd.DataFrame(summary).sort_values('Today Demand', ascending=False)


if __name__ == "__main__":
    df_forecast, df_hist = forecast_demand('Chennai', 7)
    print("📈 Chennai 7-Day Demand Forecast:")
    print(df_forecast[['date', 'demand']].to_string(index=False))
    print("\n🗺️ All Zones Summary:")
    print(get_all_zones_summary().to_string(index=False))

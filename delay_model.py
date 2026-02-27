"""
RouteIQ - Delay Prediction Model
Uses Random Forest / XGBoost to predict delivery delays
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
import joblib
import os

def generate_sample_data(n=2000):
    """Generate realistic sample logistics data if no dataset is available."""
    np.random.seed(42)
    cities = ['Chennai', 'Mumbai', 'Delhi', 'Bangalore', 'Hyderabad',
              'Kolkata', 'Pune', 'Ahmedabad', 'Coimbatore', 'Madurai']
    
    data = {
        'distance_km': np.random.randint(50, 2000, n),
        'weight_g': np.random.randint(100, 20000, n),
        'order_dow': np.random.randint(0, 7, n),
        'order_month': np.random.randint(1, 13, n),
        'freight_value': np.random.uniform(10, 500, n),
        'item_count': np.random.randint(1, 10, n),
        'seller_city': np.random.choice(cities, n),
        'customer_city': np.random.choice(cities, n),
        'estimated_days': np.random.randint(2, 15, n),
    }
    df = pd.DataFrame(data)
    
    # Simulate actual days (higher distance/weight = more likely delayed)
    delay_prob = (
        (df['distance_km'] / 2000) * 0.4 +
        (df['weight_g'] / 20000) * 0.2 +
        (df['order_dow'].isin([4, 5, 6]).astype(int)) * 0.2 +
        np.random.uniform(0, 0.3, n)
    )
    df['is_late'] = (delay_prob > 0.5).astype(int)
    return df


def train_model(df=None):
    """Train the delay prediction model."""
    if df is None:
        print("📦 No dataset found. Generating sample data...")
        df = generate_sample_data()

    le = LabelEncoder()
    df['seller_city_enc'] = le.fit_transform(df['seller_city'].fillna('Unknown'))
    df['customer_city_enc'] = le.transform(df['customer_city'].fillna('Unknown'))

    features = ['distance_km', 'weight_g', 'order_dow', 'order_month',
                'freight_value', 'item_count', 'seller_city_enc', 'customer_city_enc']

    X = df[features].fillna(0)
    y = df['is_late']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y)

    model = GradientBoostingClassifier(n_estimators=150, learning_rate=0.1,
                                        max_depth=4, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    acc = accuracy_score(y_test, y_pred)
    print(f"\n✅ Model Accuracy: {acc:.2%}")
    print(classification_report(y_test, y_pred, target_names=['On-Time', 'Delayed']))

    joblib.dump(model, 'delay_model.pkl')
    joblib.dump(le, 'city_encoder.pkl')
    joblib.dump(features, 'features.pkl')
    print("💾 Model saved as delay_model.pkl")
    return model, acc


def predict_delay(distance_km, weight_g, order_dow, order_month,
                  freight_value, item_count, seller_city, customer_city):
    """Predict if a single delivery will be delayed."""
    if not os.path.exists('delay_model.pkl'):
        train_model()

    model = joblib.load('delay_model.pkl')
    le = joblib.load('city_encoder.pkl')
    features = joblib.load('features.pkl')

    known_cities = list(le.classes_)
    seller_enc = le.transform([seller_city])[0] if seller_city in known_cities else 0
    customer_enc = le.transform([customer_city])[0] if customer_city in known_cities else 0

    input_data = pd.DataFrame([[distance_km, weight_g, order_dow, order_month,
                                  freight_value, item_count, seller_enc, customer_enc]],
                               columns=features)

    prob = model.predict_proba(input_data)[0][1]
    prediction = "🔴 HIGH RISK - Likely Delayed" if prob > 0.6 else \
                 "🟡 MEDIUM RISK - Might Delay" if prob > 0.35 else \
                 "🟢 LOW RISK - On Time"
    return prediction, prob


if __name__ == "__main__":
    train_model()

from flask import Flask, request, jsonify
import joblib
import pandas as pd
import psycopg
from datetime import datetime


app = Flask("store-sales-prediction")

# --- PostgreSQL connection config ---
DB_CONFIG = {
    "dbname": "store_sales_db",
    "user": "postgres",
    "password": "admin",
    "host": "localhost",
    "port": 5432
}

create_table_statement = """
DROP TABLE IF EXISTS prediction_logs;
CREATE TABLE prediction_logs (
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    store INTEGER,
    promo INTEGER,
    holiday INTEGER,
    year INTEGER,
    month INTEGER,
    dayofweek INTEGER,
    is_weekend INTEGER,
    prediction FLOAT
);
"""
    
def prep_db():
	with psycopg.connect(**DB_CONFIG, autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='store_sales_db'")
		if len(res.fetchall()) == 0:
			conn.execute("create database store_sales_db;")
		with psycopg.connect("host=localhost port=5432 dbname=store_sales_db user=postgres password=admin") as conn:
			conn.execute(create_table_statement)

 
def load_model():
	with open('./lin_reg.bin', 'rb') as f_in:
		model = joblib.load(f_in)
	return model 
# --- Feature Preparation ---
def prepare_features(row):
    date = pd.to_datetime(row['date'])
    features = {
        'store': row['store'],
        'promo': row['promo'],
        'holiday': row['holiday'],
        'year': date.year,
        'month': date.month,
        'dayofweek': date.dayofweek,
        'is_weekend': int(date.dayofweek >= 5)
    }
    print(features)
    return features

# --- Predict Function ---
def predict(model, features):
    
    # Convert to DataFrame with one row
    df_features = pd.DataFrame([features])  # shape: (1, n_features)
    preds = model.predict(df_features)
    return round(preds[0], 2) 

# --- Log to PostgreSQL ---
def log_to_postgres(features, prediction):
    try:
        with psycopg.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO prediction_logs (
                        timestamp, store, promo, holiday, year, month, dayofweek, is_weekend, prediction
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    datetime.now(),
                    features['store'],
                    features['promo'],
                    features['holiday'],
                    features['year'],
                    features['month'],
                    features['dayofweek'],
                    features['is_weekend'],
                    prediction
                ))
            conn.commit()
    except Exception as e:
        print("Failed to log to PostgreSQL:", e)

# --- Predict Endpoint ---
@app.route('/predict', methods=['POST'])
def predict_endpoint():
    prep_db()
    model= load_model()
    input_data = request.get_json()
    features = prepare_features(input_data)
    prediction = predict(model,features)
    print(prediction)

    # Log prediction
    log_to_postgres(features, prediction)

    return jsonify({
        'prediction': prediction
    })

# --- Optional Health Check ---
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"})

# --- Run Server ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)

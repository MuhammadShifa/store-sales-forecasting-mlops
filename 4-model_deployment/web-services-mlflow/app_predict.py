import os
from flask import Flask, request, jsonify
import pandas as pd
import mlflow



# Load the RUN_ID and S3_BUCKET_NAME from mlfow

RUN_ID = os.getenv("RUN_ID")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
EXP_ID = os.getenv('EXP_ID')

# if server is down, directly point to the location locally s3 etc.
logged_model = f"s3://{S3_BUCKET_NAME}/{EXP_ID}/{RUN_ID}/artifacts/model"


model = mlflow.pyfunc.load_model(logged_model)


app = Flask("store-sales-prediction")

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
    return features

def predict(features):
    preds = model.predict(features)
    
    return preds[0]

@app.route('/predict', methods=['POST'])
def predict_endpoint():
    input_data = request.get_json()
    features = prepare_features(input_data)
    prediction = predict(features)
    
    result = {
        'duration': prediction
    }

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9696)
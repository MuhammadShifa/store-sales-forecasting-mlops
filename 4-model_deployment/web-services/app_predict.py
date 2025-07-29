from flask import Flask, request, jsonify
import pickle
import pandas as pd


# Load model and DictVectorizer
with open('./lin_reg.bin', 'rb') as f_in:
    dv, model = pickle.load(f_in)

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
    X = dv.transform([features])
    preds = model.predict(X)
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
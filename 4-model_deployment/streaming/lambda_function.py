import os
import mlflow
import boto3
import json
import base64
import pandas as pd

kinesis_client = boto3.client('kinesis')

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'sales_predictions')
TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'

# read the RUN_ID, EXP ID and S3_BUCKET_NAME to load model from mlflow
RUN_ID = os.getenv("RUN_ID","080e0226c1fc49cc818d3c023625b36d")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME","mlartifact-s3")
EXP_ID = os.getenv('EXP_ID',"6")

# if server is down, directly point to the location locally s3 etc.
logged_model = f"s3://{S3_BUCKET_NAME}/{EXP_ID}/{RUN_ID}/artifacts/model"

model = mlflow.pyfunc.load_model(logged_model)

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

def lambda_handler(event, context):
    # print(json.dumps(event))
    
    predictions_events = []
    
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        sales_event = json.loads(decoded_data)

        sales = sales_event['sales_input']
        sales_id = sales_event['sales_id']
    
        features = prepare_features(sales)
        prediction = predict(features)
    
        prediction_event = {
            'model': 'sales_prediction_model',
            'version': '123',
            'prediction': {
                'sales_prediction': prediction,
                'sales_id': sales_id   
            }
        }

        if not TEST_RUN:
            kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data=json.dumps(prediction_event),
                PartitionKey=str(sales_id)
            )
        
        predictions_events.append(prediction_event)


    return {
        'predictions': predictions_events
    }


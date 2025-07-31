import os
import json
import base64

import boto3
import mlflow
import pandas as pd

# pylint: disable=invalid-name


def get_model_location(run_id):
    model_location = os.getenv("MODEL_LOCATION")

    if model_location is not None:
        return model_location

    S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "mlartifact-s3")
    EXP_ID = os.getenv("EXP_ID", "6")

    model_location = f"s3://{S3_BUCKET_NAME}/{EXP_ID}/{run_id}/artifacts/model"
    return model_location


def load_mode(run_id):

    # local path
    model_path = get_model_location(run_id)
    model = mlflow.pyfunc.load_model(model_path)

    return model


def base64_decode(encoded_data):

    decoded_data = base64.b64decode(encoded_data).decode("utf-8")
    sales_event = json.loads(decoded_data)

    return sales_event


class ModelService:

    def __init__(self, model, model_version=None, callbacks=None):
        self.model = model
        self.model_version = model_version
        self.callbacks = callbacks or []

    def prepare_features(self, row):
        date = pd.to_datetime(row["date"])
        features = {
            "store": row["store"],
            "promo": row["promo"],
            "holiday": row["holiday"],
            "year": date.year,
            "month": date.month,
            "dayofweek": date.dayofweek,
            "is_weekend": int(date.dayofweek >= 5),
        }
        return features

    def predict(self, features):

        pred = self.model.predict(features)
        return float(pred[0])

    def lambda_handler(self, event):

        predictions_events = []

        for record in event["Records"]:
            encoded_data = record["kinesis"]["data"]
            decoded_data = base64.b64decode(encoded_data).decode("utf-8")
            sales_event = json.loads(decoded_data)

            sales = sales_event["sales_input"]
            sales_id = sales_event["sales_id"]

            features = self.prepare_features(sales)
            prediction = self.predict(features)

            prediction_event = {
                "model": "sales_prediction_model",
                "version": self.model_version,
                "prediction": {"sales_prediction": prediction, "sales_id": sales_id},
            }

            for callback in self.callbacks:
                callback(prediction_event)

            predictions_events.append(prediction_event)

        return {"predictions": predictions_events}


class KinesisCallbacks:

    def __init__(self, kinesis_client, prediction_stream_name):
        self.kinesis_client = kinesis_client
        self.prediction_stream_name = prediction_stream_name

    def put_record(self, prediction_event):
        sales_id = prediction_event["prediction"]["sales_id"]

        self.kinesis_client.put_record(
            StreamName=self.prediction_stream_name,
            Data=json.dumps(prediction_event),
            PartitionKey=str(sales_id),
        )


def create_kinesis_client():
    endpoint_url = os.getenv("KINESIS_ENDPOINT_URL")

    if endpoint_url is None:
        return boto3.client("kinesis")

    return boto3.client("kinesis", endpoint_url=endpoint_url)


def init(prediction_stream_name: str, run_id: str, test_run: bool):

    callbacks = []
    model = load_mode(run_id=run_id)
    if not test_run:
        kinesis_client = create_kinesis_client()

        kinesis_callback = KinesisCallbacks(kinesis_client, prediction_stream_name)
        callbacks.append(kinesis_callback.put_record)

    model_service = ModelService(model=model, model_version=run_id, callbacks=callbacks)

    return model_service

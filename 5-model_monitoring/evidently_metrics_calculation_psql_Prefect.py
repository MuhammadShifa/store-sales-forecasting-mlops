import datetime
import time
import logging 
import pandas as pd
import psycopg
import joblib

from prefect import task, flow

from evidently.report import Report
from evidently import ColumnMapping
from evidently.metrics import ColumnDriftMetric, DatasetDriftMetric, DatasetMissingValuesMetric

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s]: %(message)s")

SEND_TIMEOUT = 10

create_table_statement = """
drop table if exists store_metrics;
create table store_metrics(
	timestamp timestamp,
	prediction_drift float,
	num_drifted_columns integer,
	share_missing_values float
)
"""
@task
def load_model(model_path):
	with open(model_path, 'rb') as f_in:
		model = joblib.load(f_in)
	return model 

@task
def preprocess_raw_data(df):
    # data feature engineering
	df["date"] = pd.to_datetime(df["date"])

	# Feature Engineering — Date-based features
	df["year"] = df["date"].dt.year
	df["month"] = df["date"].dt.month
	df["day"] = df["date"].dt.day
	df["dayofweek"] = df["date"].dt.dayofweek
	df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)
	
	return df

@task
def read_raw_csv(raw_data):
	raw_data = pd.read_csv(raw_data)
	processed_raw_data = preprocess_raw_data(raw_data)
 
	return processed_raw_data

@task
def read_ref_csv(ref_data):
    ref_df = pd.read_csv(ref_data)
    ref_df["date"] = pd.to_datetime(ref_df["date"])

    return ref_df
    

begin = datetime.datetime(2022, 1, 1, 0, 0)
categorical_features = ["store", "promo", "holiday", "year", "month", "dayofweek", "is_weekend"]

column_mapping = ColumnMapping(
    prediction='prediction',
    categorical_features=categorical_features,
    target=None
)

report = Report(metrics = [
    ColumnDriftMetric(column_name='prediction'),
    DatasetDriftMetric(),
    DatasetMissingValuesMetric()
])

@task
def prep_db():
	with psycopg.connect("host=localhost port=5432 user=postgres password=admin", autocommit=True) as conn:
		res = conn.execute("SELECT 1 FROM pg_database WHERE datname='store_sales_db'")
		if len(res.fetchall()) == 0:
			conn.execute("create database store_sales_db;")
		with psycopg.connect("host=localhost port=5432 dbname=store_sales_db user=postgres password=admin") as conn:
			conn.execute(create_table_statement)

@task
def calculate_metrics_postgresql(reference_data, current_data, model):
    
    current_data['prediction'] = model.predict(current_data[categorical_features].fillna(0))

    report.run(
        reference_data=reference_data,
        current_data=current_data,
        column_mapping=column_mapping
    )
    result = report.as_dict()
    prediction_drift = result['metrics'][0]['result']['drift_score']
    num_drifted_columns = result['metrics'][1]['result']['number_of_drifted_columns']
    share_missing_values = result['metrics'][2]['result']['current']['share_of_missing_values']
    
    return {
        "prediction_drift": prediction_drift,
        "num_drifted_columns": num_drifted_columns,
        "share_missing_values": share_missing_values
    }

@flow
def batch_monitoring_backfill():
    raw_data_path = "./data/store_sales.csv"
    ref_data_path = "./data/reference.csv"
    model_path = "./models/lin_reg.bin"
    
    processed_raw_data = read_raw_csv(raw_data_path)
    reference_data = read_ref_csv(ref_data_path)
    loaded_model = load_model(model_path)
    
    prep_db()
    with psycopg.connect("host=localhost port=5432 dbname=store_sales_db user=postgres password=admin", autocommit=True) as conn:
        # Select 1-day data
        for i in range(30):
            current_data = processed_raw_data[
			(processed_raw_data.date >= (begin + datetime.timedelta(i))) &
			(processed_raw_data.date < (begin + datetime.timedelta(i + 1)))
			]
            
            # Task: compute metrics
            metrics = calculate_metrics_postgresql(reference_data= reference_data, 
                                                   current_data=current_data,
                                                   model= loaded_model)
            
            with conn.cursor() as curr:
                curr.execute(
					"""
					INSERT INTO store_metrics(timestamp, prediction_drift, num_drifted_columns, share_missing_values)
					VALUES (%s, %s, %s, %s)
					""",
					(
						begin + datetime.timedelta(i),
						metrics["prediction_drift"],
						metrics["num_drifted_columns"],
						metrics["share_missing_values"]
					)
				)
                
            logging.info("data sent to PostgreSQL")
            time.sleep(SEND_TIMEOUT)

if __name__ == '__main__':
	batch_monitoring_backfill()
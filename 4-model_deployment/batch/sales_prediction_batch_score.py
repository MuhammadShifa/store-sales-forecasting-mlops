import os
import uuid
import sys
import pandas as pd
import mlflow

# read the RUN_ID, EXP ID and S3_BUCKET_NAME to load model from mlflow
RUN_ID = os.getenv("RUN_ID")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
print("S3_BUCKET_NAME: ", S3_BUCKET_NAME)
EXP_ID = os.getenv('EXP_ID')

def generate_uuids(n):
    sales_ids = []
    for i in range(n):
        sales_ids.append(str(uuid.uuid4()))
    return sales_ids


def read_dataframe(filename: str):
    df = pd.read_csv(filename)
    df["sales_id"] = generate_uuids(len(df))

    return df

def prepare_dict_features(df: pd.DataFrame):
    
    df["date"] = pd.to_datetime(df["date"])
    # Feature Engineering — Date-based features
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["day"] = df["date"].dt.day
    df["dayofweek"] = df["date"].dt.dayofweek
    df["is_weekend"] = df["dayofweek"].isin([5, 6]).astype(int)

    # Define categorical features
    categorical = ["store", "promo", "holiday", "year", "month", "dayofweek", "is_weekend"]
    df_dicts = df[categorical].to_dict(orient="records")
    
    return df_dicts


def load_model_from_mlflow():
    logged_model = f"s3://{S3_BUCKET_NAME}/{EXP_ID}/{RUN_ID}/artifacts/model"    
    model = mlflow.pyfunc.load_model(logged_model)
    return model


def apply_model(input_file, output_file):
    print(f"reading the data from {input_file}...")
    df = read_dataframe(input_file)
    
    dicts = prepare_dict_features(df)
    print(f"loading the model having run_id: {RUN_ID}")
    model = load_model_from_mlflow()
    
    print("applying the model ...")
    y_pred = model.predict(dicts)
    
    print(f"saving the results to {output_file}")
    
    df['sales_prediction'] =  y_pred
    df['model_version'] = RUN_ID
    df_desired_order = [
            'sales_id',
            'store',
            'date',
            'promo',
            'holiday',
            'year',
            'month',
            'day',
            'dayofweek',
            'is_weekend',
            'sales',
            'sales_prediction',
            'model_version'
        ]

    df = df[df_desired_order]
    df.to_csv(output_file, index=False)


def run():
    input_file_path = sys.argv[1]
    output_file_name = sys.argv[2]

    input_file = f"{input_file_path}"
    output_file = f"output/{output_file_name}.csv"

    apply_model(input_file=input_file, 
                output_file=output_file)


if __name__ == "__main__":
    run()

# run the script
# python sales_prediction_batch_score.py input_file_path output_file_name
# e.g python sales_prediction_batch_score.py ./input_data/test.csv test_output


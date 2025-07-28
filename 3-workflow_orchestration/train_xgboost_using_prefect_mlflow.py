import os
import pickle
import mlflow
import argparse
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.feature_extraction import DictVectorizer
from xgboost import XGBRegressor

from prefect import task, flow, get_run_logger


# os.environ["AWS_PROFILE"] = "default"
@task
def dump_pickle(obj, filename: str):
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)

# read the csv file
@task
def read_data(filename):
    df = pd.read_csv(filename)
    return df

# dataframe feature engineering
@task
def prepare_data(df: pd.DataFrame):
    
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
    
    target_label = 'sales'
    y_labels = df[target_label].values

    return df_dicts, y_labels

#train a model
@task
def train_model(train_dicts, y_train):

    dv = DictVectorizer()
    X_train = dv.fit_transform(train_dicts)
    
    # Train XGBoost model
    xgb_model = XGBRegressor(
        n_estimators=300,
        learning_rate=0.1,
        max_depth=4,
        random_state=42
    )

    xgb_model.fit(X_train, y_train)

    return dv, xgb_model

@task
def log_model(dv, model):
    logger = get_run_logger()
    
    TRACKING_SERVER_HOST = os.environ.get("TRACKING_SERVER_HOST")

    if TRACKING_SERVER_HOST:
        mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
        print(f"Tracking URI set to: http://{TRACKING_SERVER_HOST}:5000")
    else:
        print("TRACKING_SERVER_HOST is not set!")
    
    mlflow.set_experiment("store-sales-prediction-orchestration")

    with mlflow.start_run() as run:
        mlflow.log_param("model_type", "XGBRegressor")

        dump_pickle(dv, "dict_vectorizer.pkl")
        
        mlflow.log_artifact("dict_vectorizer.pkl")
        mlflow.sklearn.log_model(model, artifact_path="model")

        run_id = run.info.run_id
        logger.info(f"MLflow model successfully loged having Run ID: {run_id}")
            
# testing the model
@task
def run_trained_model(X_val_dicts, y_val, dv, model):
    
    X_val = dv.transform(X_val_dicts) 
 
    y_pred = model.predict(X_val)

    mse = mean_squared_error(y_val, y_pred, squared=False)
    print(f"The MSE of validation is: {mse}")
    
    return

@flow      
def run_main(train_df: str, test_df:str):
    train_df = read_data("./input_data/train.csv")
    test_df = read_data("./input_data/test.csv")
    
    X_train_dicts, y_train = prepare_data(train_df)
    X_test_dicts_, y_test = prepare_data(test_df)

    dv, model = train_model(X_train_dicts, y_train)
    
    log_model(dv, model)
    
    run_trained_model(X_val_dicts=X_test_dicts_, y_val=y_test, dv=dv, model=model)
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--train_csv_path",
        default="./input_data/train.csv",
        help="the location where the train csv was saved."
    )
    parser.add_argument(
        "--test_csv_path",
        default="./input_data/test.csv",
        help="the location where the test csv was saved."
    )
    args = parser.parse_args()

    run_main(args.train_csv_path, args.test_csv_path)
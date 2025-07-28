import os
import pickle
import mlflow
import argparse

from sklearn.metrics import mean_squared_error
from sklearn.ensemble import RandomForestRegressor


TRACKING_SERVER_HOST = os.environ.get("TRACKING_SERVER_HOST")

if TRACKING_SERVER_HOST:
    mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
    print(f"Tracking URI set to: http://{TRACKING_SERVER_HOST}:5000")
else:
    print("TRACKING_SERVER_HOST is not set!")

EXPERIMENT_NAME = "random-forest-best-models"
mlflow.set_experiment(EXPERIMENT_NAME)

mlflow.sklearn.autolog()


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)


def run_train_and_autolog_model(data_path: str):
   
    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    with mlflow.start_run():
            
        rf = RandomForestRegressor(max_depth=10, random_state=0)
        rf.fit(X_train, y_train)
        y_pred = rf.predict(X_val)

        rmse = mean_squared_error(y_val, y_pred, squared=False)
        print("rmse: ", rmse)
        
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        default="./preprocessed_output",
        help="the location where the processed red wine quality data was saved."
    )
    args = parser.parse_args()

    run_train_and_autolog_model(args.data_path)
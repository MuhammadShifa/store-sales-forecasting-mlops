import argparse
import os
import pickle

import mlflow
import numpy as np
from hyperopt import STATUS_OK, Trials, fmin, hp, tpe
from hyperopt.pyll import scope
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error


TRACKING_SERVER_HOST = os.environ.get("TRACKING_SERVER_HOST")

if TRACKING_SERVER_HOST:
    mlflow.set_tracking_uri(f"http://{TRACKING_SERVER_HOST}:5000")
    print(f"Tracking URI set to: http://{TRACKING_SERVER_HOST}:5000")
else:
    print("TRACKING_SERVER_HOST is not set!")
    
mlflow.set_experiment("store-sales-hyperopt-random-forest")


def load_pickle(filename: str):
    with open(filename, "rb") as f_in:
        return pickle.load(f_in)

def run_optimization(data_path: str, num_trials: int):

    X_train, y_train = load_pickle(os.path.join(data_path, "train.pkl"))
    X_val, y_val = load_pickle(os.path.join(data_path, "val.pkl"))

    def objective(params):
        with mlflow.start_run():
                
            rf = RandomForestRegressor(**params)
            rf.fit(X_train, y_train)
            y_pred = rf.predict(X_val)
            rmse = mean_squared_error(y_val, y_pred, squared=False)
            
            # Log hyperparameters and RMSE manually
            mlflow.log_params(params)
            mlflow.log_metric("rmse", rmse)

            return {'loss': rmse, 'status': STATUS_OK}

    search_space = {
        'max_depth': scope.int(hp.quniform('max_depth', 1, 20, 1)),
        'n_estimators': scope.int(hp.quniform('n_estimators', 10, 50, 1)),
        'min_samples_split': scope.int(hp.quniform('min_samples_split', 2, 10, 1)),
        'min_samples_leaf': scope.int(hp.quniform('min_samples_leaf', 1, 4, 1)),
        'random_state': 42
    }

    rstate = np.random.default_rng(42)  # for reproducible results
    fmin(
        fn=objective,
        space=search_space,
        algo=tpe.suggest,
        max_evals=num_trials,
        trials=Trials(),
        rstate=rstate
    )
    
if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--data_path",
        default="./preprocessed_output",
        help="the location where the processed red wine quality data was saved."
    )
    parser.add_argument(
        "--max_evals",
        default=10,
        help="the number of parameter evaluations for the optimizer to explore."
    )
    args = parser.parse_args()

    run_optimization(args.data_path, args.max_evals)
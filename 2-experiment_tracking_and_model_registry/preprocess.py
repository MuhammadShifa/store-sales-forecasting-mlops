import argparse
import os
import pickle
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction import DictVectorizer

def dump_pickle(obj, filename: str):
    with open(filename, "wb") as f_out:
        return pickle.dump(obj, f_out)

# read the csv file
def read_dataframe(filename):
    df = pd.read_csv(filename)

    return df

# dataframe feature engineering
def prepare_data(df: pd.DataFrame, dv: DictVectorizer, fit_dv: bool = False):
    
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
    
    if fit_dv:
        X = dv.fit_transform(df_dicts)
    else:
        X = dv.transform(df_dicts)
    return X, dv


def run_data_preprocessing(raw_data_path: str, dest_path: str):
    # Load csv files
    store_df = read_dataframe(os.path.join(raw_data_path, "store_sales.csv"))

    # extract the target
    y = store_df['sales']
    X = store_df.drop('sales', axis = 1)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2, random_state = 42)
    X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.2, random_state=42)
    

    # Fit the DictVectorizer and preprocess data
    dv = DictVectorizer()
    X_train, dv = prepare_data(X_train, dv, fit_dv=True)
    X_val, _ = prepare_data(X_valid, dv, fit_dv=False)
    X_test, _ = prepare_data(X_test, dv, fit_dv=False)

    # create dest_path folder if it doesn't exists
    os.makedirs(dest_path, exist_ok=True)

    # Save DictVectorizer and datasets
    dump_pickle(dv, os.path.join(dest_path, "dv.pkl"))
    dump_pickle((X_train, y_train), os.path.join(dest_path, "train.pkl"))
    dump_pickle((X_val, y_valid), os.path.join(dest_path, "val.pkl"))
    dump_pickle((X_test, y_test), os.path.join(dest_path, "test.pkl"))


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw_data_path",
        default="./input_data",
        help="the location where the raw red wine quality data was saved"
    )
    parser.add_argument(
        "--dest_path",
        default="./preprocessed_output",
        help="the location where the resulting files will be saved."
    )
    args = parser.parse_args()

    run_data_preprocessing(args.raw_data_path, args.dest_path)
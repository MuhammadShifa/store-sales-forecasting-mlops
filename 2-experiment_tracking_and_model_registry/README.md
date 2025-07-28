# 🧪 Module 2: Experiment Tracking and Model Registry with MLflow

This module focuses on integrating **MLflow** into our Store Sales Prediction project to enable **experiment tracking**, **model registry**, and **remote server integration** via **AWS EC2 + S3 + PostgreSQL**.  
We continue building on the environment established in Module 1.

---

## 📦 Environment Setup

Install MLflow and required dependencies:

```bash
pip install mlflow==2.22.0
pip install boto3
```

To run MLflow UI locally:

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db --default-artifact-root ./mlruns
```

---

## 📘 Contents

| File | Description |
|------|-------------|
| `1.2 store-sales-prediction-local-mlfow-exp.ipynb` | Modified notebook from Module 1 to track local MLflow experiments |
| `1.3 store-sales-prediction-aws-ec2-mlfow-exp.ipynb` | Remote MLflow experiment tracking using AWS EC2, PostgreSQL, and S3 |
| `mlflow_on_aws.md` | Instructions to configure a remote MLflow server on AWS EC2 (based on Zoomcamp guide) |
| `images/` | Folder containing screenshots and visual results from MLflow experiments |

---

## 🧪 Local MLflow Experiment Tracking

In the notebook `1.2 store-sales-prediction-local-mlfow-exp.ipynb`, we:

- Tracked **Lasso Regression** experiment locally  
  ![Linear Regression](images/local_linear_regression.png)

- Optimized **XGBoost hyperparameters** using MLflow  
  ![XGBoost Hyperparameter Tuning](images/local_xgb_hpo.png)

- Trained and tracked final **XGBoost model**  
  ![XGBoost Final Model](images/local_xgb_final.png)

The backend store is local SQLite and artifacts are saved in `./mlruns`.

---

## ☁️ Remote MLflow Server on AWS

> 🔧 Based on instructions from [`mlflow_on_aws.md`](https://github.com/DataTalksClub/mlops-zoomcamp/blob/main/02-experiment-tracking/mlflow_on_aws.md)

### ✅ Remote Setup Overview

- **Tracking Server:** MLflow on EC2 (Linux instance)
- **Backend Store:** PostgreSQL (RDS or manually installed)
- **Artifacts Store:** S3 bucket (`mlartifact-s3`)

---

### 🔧 EC2 Setup Steps

Install dependencies:

```bash
sudo yum update
pip3 install mlflow boto3 psycopg2-binary
```

Then configure AWS credentials:
For accessing AWS services using CLI, please configure your aws credentials. It can be done in SSH terminal/Anaconda Prompt by running the command : aws configure

```bash
aws configure
```
It will ask you for your :

1. AWS Access Key ID
2. AWS Secret Access Key
3. Default region name
4. Default output format

More information on setting up profile can be found [here](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-profiles.html)

SSH into your EC2 instance and start the MLflow server:

```bash
mlflow server \
    -h 0.0.0.0 \
    -p 5000 \
    --backend-store-uri postgresql://<DB_USER>:<DB_PASSWORD>@<DB_ENDPOINT>:5432/<DB_NAME> \
    --default-artifact-root s3://<S3_BUCKET_NAME>
```

Access the remote MLflow UI via:

```
http://<EC2_PUBLIC_DNS>:5000
```

---

## 🌐 Remote MLflow Experiments

In `1.3 store-sales-prediction-aws-ec2-mlfow-exp.ipynb`, we ran the same experiments and tracked them on the remote MLflow server:

- Lasso Regression Tracking  
  ![Lasso Regression](images/remote_lasso_regression.png)

- Hyperparameter tuning  
  ![Remote HPO](images/remote_xgb_hpo.png)

- XGBoost Final Model  
  ![Remote XGBoost](images/remote_xgb_final.png)

---

## Further File Structure : 

Before Running the below script, it would be great if we explore the public DNS of ec2.

```bash
export TRACKING_SERVER_HOST='ec2-PublicDNS'
```

confirm it:

```bash
echo $TRACKING_SERVER_HOST
```
Now we can easily get the value within the python code.
```python
import os

tracking_host = os.environ.get("TRACKING_SERVER_HOST")

if tracking_host:
    mlflow.set_tracking_uri(f"http://{tracking_host}:5000")
    print(f"Tracking URI set to: http://{tracking_host}:5000")
else:
    print("TRACKING_SERVER_HOST is not set!")
```

1. `preprocess.py` -> This script loads the raw data from input folder, processes it and saves the pre-processed data in `preprocessed_output` folder.

2. `train.py` -> The script will load the pre-processed data from output folder, train the model on the training set and calculate the RMSE on the validation set. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud).

3. `hpo.py` -> This script tries to reduce the validation error by tuning the hyperparameters of the random forest regressor using hyperopt. The script logs the parameters and artifacts in MLflow(locally) as well as logs the artifacts in S3 bucket(cloud).

4. `register_model.py` -> This script will promote the best model (with lowest test_rmse) to the model registry. It will check the results from the previous step and select the top 5 runs. After that, it will calculate the RMSE of those models on the test set and save the results to a new experiment called "red-wine-random-forest-best-models". The model with lowest test RMSE from the 5 runs is registered.

you will have to make some changes in train.py, hpo.py and register_model.py. These changes are to set the Tracking-uri of your ec2 (public_dns) and port 5000

**NOTE :** I have used Anaconda Prompt for this section instead of SSH terminal because I was having issues with sklearn version in SSH terminal. If you face any errors while running the script, please consider creating a new environment using the requirements.txt file.

**Artifacts can be saved locally as well as on cloud (AWS). My script saves these artifacts in S3 bucket. It meets the requirement of developing project on Cloud (mentioned in README of course project of MLOps Zoomcamp Github Repo).**
---
Each step images are stored in `images` folder for a reference.

```

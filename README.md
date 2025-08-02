# MLOps Zoomcamp Project - Store Sales Forecasting

Welcome to the **MLOps Zoomcamp 2025 Cohort Project**!  
This repository showcases how modern MLOps practices are applied to a real-world store sales forecasting use case.

## 🎯 Problem Description

**Retail store sales forecasting** is a vital business challenge for retailers aiming to optimize inventory, staffing, and promotional strategies. Accurate sales predictions empower companies to make data-driven decisions that directly impact profitability and operational efficiency. This project addresses:

- **Business Impact**: Under/overstocking, misallocated staff, and poor promotions hurt business outcomes.
- **Forecasting Challenge**: Incorporating seasonality, holidays, and promotions into a daily-level prediction.
- **Production Readiness**: Building a solution that can be deployed, monitored, and retrained automatically.
- **Scalable ML Lifecycle**: Ensuring automation, observability, and reproducibility across development and deployment.

## 🚀 Project Objective

The objective of this project is to build a robust, end-to-end, and production-grade MLOps pipeline that forecast **daily store sales** using historical and contextual data. It includes all phases of the ML lifecycle, from experimentation to deployment and monitoring, using the best MLOps practices.

### 🧩 Key Features
- ✅ **Automated Data Processing**: Feature engineering, cleaning, and validation.
- ✅ **Model Training & Optimization**: XGBoost, Linear Regression, and RandomForest with hyperparameter tuning.
- ✅ **Experiment Tracking**: MLflow for logging parameters, metrics, and artifacts.
- ✅ **Pipeline Orchestration**: Prefect for workflow management across stages.
- ✅ **Model Deployment**: Flask-based API served via Docker containers, Batch Scoring and Streaming Deployment.
- ✅ **Monitoring & Alerting**: Evidently AI + PostgreSQL + Grafana for production drift and performance monitoring.
- ✅ **Code Quality**: Pylint, isort, black and github pre-commit hooks
- ✅ **Unit & Integration Tests**: Unit test for core components and integration test for streaming deployment pipeline.
- ✅ **Code Quality**: Enforced via `pylint`, `black`, `isort`, and pre-commit hooks.
- ✅ **Infrastructure as Code**: Terraform-based EC2 setup for reproducibility.
- ✅ **CI/CD Automation**: GitHub Actions for continuous integration and delivery.


## ❗ Problem Statement

The dataset provides **daily sales data** for multiple retail stores, along with contextual features such as promotions and dates. While no explicit holiday data is included, we **engineered temporal features** from the `date` column, including `year`, `month`, `day`, `dayofweek`, and `is_weekend`.

Our goal:
- 📈 **Forecast daily store sales** using historical sales trends and contextual features.
- ⚙️ Build a production-ready MLOps pipeline with support for **web service deployment**, **batch scoring**, and **streaming predictions**.
- 🚀 Ensure end‑to‑end automation of **data preprocessing, model scoring**, and **monitoring**, with full reproducibility using infrastructure-as-code and CI/CD workflows.

> Dataset Source: [Kaggle – Store Sales Dataset](https://www.kaggle.com/datasets/abhishekjaiswal4896/store-sales-dataset/data)

## 🛠 Tools and Technologies Used

| Category                  | Tools Used                                        |
|---------------------------|---------------------------------------------------|
| Cloud                     | AWS (EC2, S3, Kinesis,lambda function, PostgreSQL)|
| Experiment Tracking       | MLflow                                            |
| Workflow Orchestration    | Prefect                                           |
| Containerization          | Docker, Docker Compose                            |
| Model Deployment          | Flask, Docker, MLflow, AWS and localstack        |
| Model Monitoring          | Evidently AI, PostgreSQL, Grafana                 |
| Best Practices            | Linting, Testing, Pre-commit, Makefile, CI/CD     |

---


## Project Structure and Set-up Environment Configuration
The project is implemented on **Ubuntu 22.04** using an **Anaconda environment** (Python 3.9). Each module of the Zoomcamp course is structured in its own directory and includes a dedicated `README.md` for details instructions. The `requirement.txt` and other information related to python environment are provided within each module `README.md`.

> Note: Some steps assume AWS EC2 usage as demonstrated in [this video](https://www.youtube.com/watch?v=IXSiYkP23zo&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK&index=4). Using other platforms may require modifications.
> Additionaly, a seperate complete environment configuration file is available for Github Codespaces, Anaconda, EC2, Docker etc in [env_configuration.md](./env_configuration.md)

### Module Directories:

 - `1-introduction`
 - `2-experiment_tracking_and_model_registry`
 - `3-workflow_orchestration`
 - `4-model_deployment`
 - `5-model_monitoring`
 - `6-best_practices`

Each folder includes:
- Source code
- Notebooks
- `requirements.txt`, `Pipfile` and environment setup instructions in `README.md`
- A detailed `README.md` within each module contained code parts explaination, screenshoots etc. as well. 


## 🚀 How to Use This Repository
- clone the repository and follow each section/module having a  seperate `readme.md` file.
```bash
git clone https://github.com/MuhammadShifa/store-sales-prediction-mlops.git
```

---

## 🔗 Useful Links

- [MLOps Zoomcamp Course Website](https://datatalks.club/)
- [My personal repo - mlops-zoomcamp2025](https://github.com/MuhammadShifa/mlops-zoomcamp2025)
- [DataTalks.Club YouTube Channel](https://youtube.com/playlist?list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK&si=GJzG_nixJHDOoioj)  

---

Feel free to explore and contribute!  
Happy learning with MLOps Zoomcamp! 🎉


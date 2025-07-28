# MLOps Zoomcamp Project - Store Sales Prediction

Welcome to the **MLOps Zoomcamp 2025 Cohort Project**!  
This repository showcases how modern MLOps practices are applied to a real-world store sales prediction use case.


## Objective
The objective of this project is to build a robust, end-to-end, and production-grade MLOps pipeline that predicts **daily store sales** using historical data. By leveraging the [Store Sales Dataset](https://www.kaggle.com/datasets/abhishekjaiswal4896/store-sales-dataset/data), we aim to:

- Develop and deploy multiple machine learning models (XGBoost, RandomForest, Linear Regression).
- Enable a fully automated pipeline using modern MLOps tools and techniques.
- Ensure scalability, reliability, and monitoring across all phases of the ML lifecycle.

This pipeline integrates:
- **MLflow** for experiment tracking and model registry,
- **Prefect** for orchestration,
- **Flask + Docker** for model serving,
- **Evidently + PostgreSQL + Grafana** for monitoring and observability,
- **CI/CD** and production best practices.


## Problem Statements
The dataset provides historical daily sales information of retail stores, including factors such as promotions, holidays, and date-specific trends. The key problem we aim to solve:

- **Forecast daily sales** for retail stores based on historical and contextual data.
- Build a system that supports **retraining, serving, and monitoring** of models in production.
- Provide the business with tools to **optimize inventory, staffing, and promotions** using predictions.
- Ensure **data pipelines, batch scoring, monitoring**, and **logging** are fully automated and reproducible.

> Dataset Source: [Kaggle - Store Sales Dataset](https://www.kaggle.com/datasets/abhishekjaiswal4896/store-sales-dataset/data)


## Project Structure and Set-up Environment Configuration
The project is implemented on **Ubuntu 22.04** using an **Anaconda environment** (Python 3.9). Each module of the Zoomcamp course is structured in its own directory and includes a dedicated `README.md` for instructions.

> Note: Some steps assume AWS EC2 usage as demonstrated in [this video](https://www.youtube.com/watch?v=IXSiYkP23zo&list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK&index=4). Using other platforms may require modifications.
> The complete environment configuration file is available for Github Codespaces, Anaconda, EC2, Docker etc in [env_configuration.md](./env_configuration.md)

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

More information on how to create a virtual environment using Pipfile can be found [here](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment)

## 🛠 Tools and Technologies Used

| Category                  | Tools Used                                          |
|---------------------------|-----------------------------------------------------|
| Cloud                     | AWS (EC2, optionally S3)                            |
| Experiment Tracking       | MLflow                                              |
| Workflow Orchestration    | Prefect                                             |
| Containerization          | Docker, Docker Compose                             |
| Model Deployment          | Flask, Docker, MLflow                              |
| Model Monitoring          | Evidently AI, PostgreSQL, Grafana, Prometheus      |
| Best Practices            | Linting, Testing, Pre-commit, Makefile, CI/CD      |

## 🚀 How to Use This Repository
- clone the repository and follow each section seperate `readme.md` file.
`git clone repository-link`
---

## 🔗 Useful Links

- [MLOps Zoomcamp Course Website](https://datatalks.club/)
- [My personal repo - mlops-zoomcamp2025](https://github.com/MuhammadShifa/mlops-zoomcamp2025)
- [DataTalks.Club YouTube Channel](https://youtube.com/playlist?list=PL3MmuxUbc_hIUISrluw_A7wDSmfOhErJK&si=GJzG_nixJHDOoioj)  

---

Feel free to explore and contribute!  
Happy learning with MLOps Zoomcamp 2025! 🎉


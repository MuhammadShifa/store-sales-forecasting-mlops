# 🛒 Store Sales Forecasting – Introduction Module

This is the first module of the **Store Sales Prediction** MLOps project. It sets up the development environment, prepares the dataset, performs exploratory data analysis and feature engineering, and trains baseline regression models to predict daily store sales.

---

## 📦 Step 1: Download & Install Anaconda

To begin, install **Anaconda** on your system:

```bash
wget https://repo.anaconda.com/archive/Anaconda3-2022.05-Linux-x86_64.sh
bash Anaconda3-2022.05-Linux-x86_64.sh
```

### ✅ Verify Anaconda Installation

```bash
conda --version
```

> 🔧 **If `conda` is not recognized**, run the following:

```bash
source ~/.bashrc
```

Then recheck:

```bash
conda --version
```

---

## 🐍 Step 2: Create Python Environment

Create and activate a new Conda environment with Python 3.9:

```bash
conda create -n py39 python=3.9 -y
conda activate py39
```

Install project dependencies:

```bash
pip install -r requirements.txt
```

---

## 📊 Step 3: Run the Notebook

Open and run all cells in the notebook:

```bash
1.1-store-sales-prediction.ipynb
```

This notebook performs the following tasks:

- ✅ **Data Loading**: Reads raw dataset.
- 📁 **Data Split**: Splits the data into `train.csv` and `test.csv`.
- 🧹 **Preprocessing**: Cleans column names and checks dataset statistics.
- 📈 **EDA**: Performs statistical overview and basic visual analysis.
- 🧠 **Feature Engineering**: Extracts features from the date column.
- 🔁 **Data Transformation**: Applies `DictVectorizer` for categorical encoding.
- 🧪 **Model Training**: Trains the following models:
  - Linear Regression
  - Lasso Regression
  - Ridge Regression
  - XGBoost Regressor
- 📉 **Evaluation**: Plots model performance and compares results.
- 💾 **Model Saving**: Trained models are saved to the `model/` directory.

---

## 📂 Output

After successful execution:

- data splitted as `train.csv` and `test.csv`
- Trained models saved in the `model/` folder
- Performance plots available in the notebook
---




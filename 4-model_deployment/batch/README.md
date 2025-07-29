# Batch Sales Prediction with MLflow & Prefect

This module performs **batch sales prediction** using a trained machine learning model stored on a remote MLflow tracking server (hosted on S3). It uses **Prefect** for task orchestration and runs as a command-line script.


## How It Works

1. **Reads input CSV data**.
2. **Generates unique `sales_id`s**.
3. **Performs feature engineering** (e.g., extracting date components).
4. **Loads the ML model from an MLflow S3 artifact store**.
5. **Predicts sales values**.
6. **Saves results** in a clean, formatted CSV including predictions and model version.

---
### Environment Variables Required

Make sure the following environment variables are set **before running the script**:

- `RUN_ID`: The MLflow run ID of the trained model
- `EXP_ID`: The MLflow experiment ID
- `S3_BUCKET_NAME`: The name of the S3 bucket where the model is stored

### Run the Scripts:
Activate the `pipenv` cirtual environment in batch directory using terminal
```bash
pipenv shell
```
Install the packages, `Pipefile` are provided, by running the command:
```
pipenv install
```

All set, now we need to run the script.

```python
# python sales_prediction_batch_score.py input_file_path output_file_name
python sales_prediction_batch_score.py ./input_data/test.csv test_output
```
For running the script with Prefect Orchestration, run the below command:
```python
# python sales_prediction_batch_score_prefect.py input_file_path output_file_name
python sales_prediction_batch_score_prefect.py ./input_data/test.csv test_output
```

**Note**: We are loading the model from S3 Bucket, if you want local you need to makes some changes in code.

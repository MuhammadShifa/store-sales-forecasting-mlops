## Store Sales Prediction API with Logging to PostgreSQL

This Flask application provides a RESTful API to serve a trained **Linear Regression** model for daily **store sales prediction**, and logs predictions to a **PostgreSQL** database for monitoring purposes.

---

#### 🚀 Key Features

- **Endpoint:** `POST /predict`  
  - Accepts JSON input containing:
    - `store`, `promo`, `holiday`, `date`
  - Parses and processes the input date into additional time-based features:
    - `year`, `month`, `dayofweek`, `is_weekend`
  - Loads the pre-trained model (`lin_reg.bin`) and returns a **sales prediction** rounded to 2 decimal places.
  - Logs both input features and the prediction to a PostgreSQL table `prediction_logs`.

- **Logging Table:** `prediction_logs`  
  Stores the following for each prediction:
  - `timestamp`, `store`, `promo`, `holiday`, `year`, `month`, `dayofweek`, `is_weekend`, `prediction`

- **Database Bootstrapping:**  
  The `prep_db()` function ensures the database and logging table exist. It drops the existing `prediction_logs` table and recreates it to ensure a clean schema.

- **Endpoint:** `GET /health`  
  - Returns a simple status check (`{"status": "ok"}`) to verify the API is running.

---


#### 📦 Usage
Run the flask app:
```bash
python app.py
```

Run the testing script and verify the results in PostgreSQL.
```bash
python test_app.py
```


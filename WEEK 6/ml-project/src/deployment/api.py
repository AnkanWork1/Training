import os
import uuid
import joblib
import pandas as pd
import numpy as np
from datetime import datetime

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# -------------------------------------------------------------------
# CONFIG
# -------------------------------------------------------------------

CURRENT_YEAR = 2025

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "models/model_tuned_optuna.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models/model_label_encoder.pkl")
LOG_FILE = os.path.join(BASE_DIR, "prediction_logs.csv")

# IMPORTANT: must match training feature order EXACTLY
MODEL_FEATURE_ORDER = [
    "year",
    "mileage",
    "log_mileage",
    "mpg",
    "model",
    "tax",
    "transmission_Semi-Auto",
    "transmission_Manual",
    "is_automatic",
    "is_diesel"
]

# -------------------------------------------------------------------
# LOAD ARTIFACTS
# -------------------------------------------------------------------

model = joblib.load(MODEL_PATH)
model_encoder = joblib.load(ENCODER_PATH)

# -------------------------------------------------------------------
# FASTAPI APP
# -------------------------------------------------------------------

app = FastAPI(
    title="BMW Price Prediction API",
    version="1.0"
)

# -------------------------------------------------------------------
# INPUT SCHEMA (RAW INPUT — NOT PROCESSED)
# -------------------------------------------------------------------

class PredictionRequest(BaseModel):
    year: int
    mileage: float
    mpg: float
    tax: float
    engineSize: float
    model: str
    transmission: str        # Automatic / Manual / Semi-Auto
    fuelType: str            # Diesel / Petrol

# -------------------------------------------------------------------
# PREPROCESSING (SAME AS build_features.py)
# -------------------------------------------------------------------

def preprocess_input(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Time features
    df["car_age"] = CURRENT_YEAR - df["year"]
    df["mileage_per_year"] = df["mileage"] / df["car_age"].replace(0, 1)

    # Numerical transforms
    df["log_mileage"] = np.log1p(df["mileage"])
    df["log_tax"] = np.log1p(df["tax"])
    df["mpg_per_engine"] = df["mpg"] / df["engineSize"].replace(0, 0.1)
    df["tax_per_engine"] = df["tax"] / df["engineSize"].replace(0, 0.1)

    # Binary features
    df["is_automatic"] = (df["transmission"] == "Automatic").astype(int)
    df["is_diesel"] = (df["fuelType"] == "Diesel").astype(int)

    # One-hot encoding
    df = pd.get_dummies(df, columns=["transmission", "fuelType"], drop_first=True)

    # Ensure expected OHE columns exist
    for col in ["transmission_Manual", "transmission_Semi-Auto"]:
        if col not in df.columns:
            df[col] = 0

    # Label encode model
    try:
        df["model"] = model_encoder.transform(df["model"])
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Unknown car model received. Model not seen during training."
        )

    # Select final features in correct order
    df = df[MODEL_FEATURE_ORDER]

    return df

# -------------------------------------------------------------------
# LOGGING
# -------------------------------------------------------------------

def log_prediction(raw_input: dict, prediction: float, request_id: str):
    log_row = {
        "request_id": request_id,
        "timestamp": datetime.utcnow(),
        **raw_input,
        "prediction": prediction
    }

    df = pd.DataFrame([log_row])

    if os.path.exists(LOG_FILE):
        df.to_csv(LOG_FILE, mode="a", header=False, index=False)
    else:
        df.to_csv(LOG_FILE, index=False)

# -------------------------------------------------------------------
# PREDICT ENDPOINT
# -------------------------------------------------------------------

@app.post("/predict")
def predict(data: PredictionRequest):
    request_id = str(uuid.uuid4())

    try:
        raw_df = pd.DataFrame([data.dict()])
        processed_df = preprocess_input(raw_df)

        prediction = model.predict(processed_df)[0]

        log_prediction(data.dict(), float(prediction), request_id)

        return {
            "request_id": request_id,
            "prediction": float(prediction)
        }

    except HTTPException:
        raise

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

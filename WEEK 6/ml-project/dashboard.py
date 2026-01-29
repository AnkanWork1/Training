import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

st.title("Car Price Prediction Dashboard")

# Load model and LabelEncoder
model = joblib.load(Path("src/models/model_tuned_optuna.pkl"))
le_model = joblib.load(Path("src/models/model_label_encoder.pkl"))

# User inputs
year = st.number_input("Year", 2000, 2025, 2018)
mileage = st.number_input("Mileage", 0, 500000, 30000)
mpg = st.number_input("MPG", 0, 100, 50)
tax = st.number_input("Tax", 0, 1000, 150)
engineSize = st.number_input("Engine Size", 0.0, 6.0, 2.0)
model_name = st.selectbox("Model", le_model.classes_)

# Predict button
if st.button("Predict"):
    import numpy as np
    # Encode model
    model_idx = le_model.transform([model_name])[0]
    # Create input vector
    X = pd.DataFrame([{
        "year": year,
        "mileage": mileage,
        "mpg": mpg,
        "tax": tax,
        "engineSize": engineSize,
        "model": model_idx
    }])
    # Prediction
    price_pred = model.predict(X)[0]
    st.success(f"Predicted Price: {price_pred:.2f}")

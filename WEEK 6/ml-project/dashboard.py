import streamlit as st
import requests
import json

st.title("Car Price Prediction Dashboard (API)")

# User inputs
year = st.number_input("Year", 2000, 2025, 2018)
mileage = st.number_input("Mileage", 0, 500000, 30000)
mpg = st.number_input("MPG", 0, 100, 50)
tax = st.number_input("Tax", 0, 1000, 150)
engineSize = st.number_input("Engine Size", 0.0, 6.0, 2.0)
model_name = st.selectbox("Model", ["1 Series", "2 Series", "3 Series", "4 Series", "5 Series", "6 Series", "X1", "X2", "X3", "X4", "X5", "Z4"])
trans = st.selectbox("Transmission", ["Automatic", "Semi-Auto", "Manual"])
fuel = st.selectbox("Fuel Type", ["Petrol", "Diesel"])

# API URL
API_URL = "http://backend:8000/predict"
  # Update if using a different host/port

if st.button("Predict"):

    # Build JSON payload exactly as API expects
    payload = {
        "year": year,
        "mileage": mileage,
        "mpg": mpg,
        "tax": tax,
        "engineSize": engineSize,
        "model": " "+model_name,
        "transmission": trans,
        "fuelType": fuel
    }

    try:
        # Call the API
        response = requests.post(API_URL, json=payload)
        response.raise_for_status()  # Raise error for bad status

        # Get prediction
        result = response.json()
        st.success(f"Predicted Price: {result['prediction']:.2f}")

    except requests.exceptions.HTTPError as errh:
        st.error(f"HTTP Error: {response.json()['detail']}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error calling API: {e}")

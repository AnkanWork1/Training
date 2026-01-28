import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder, LabelEncoder
from sklearn.model_selection import train_test_split

CURRENT_YEAR = 2025

def build_features(df):
    df = df.copy()

    # Target
    y = df["price"]
    df = df.drop(columns=["price"])

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
    cat_cols = ["transmission", "fuelType"]
    df = pd.get_dummies(df, columns=cat_cols, drop_first=True)

    # Label encode 'model'
    le_model = LabelEncoder()
    df["model"] = le_model.fit_transform(df["model"])

    return df, y ,le_model

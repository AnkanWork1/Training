import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.base import BaseEstimator, TransformerMixin
import joblib

CURRENT_YEAR = 2025

# -----------------------------
# 1️⃣ Custom feature builder
# -----------------------------
class FeatureBuilder(BaseEstimator, TransformerMixin):
    def __init__(self, le_model=None):
        self.le_model = le_model  # fitted LabelEncoder for 'model'

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        # Core engineered features
        X["car_age"] = CURRENT_YEAR - X["year"]
        X["mileage_per_year"] = X["mileage"] / X["car_age"].replace(0,1)
        X["log_mileage"] = np.log1p(X["mileage"])
        X["log_tax"] = np.log1p(X["tax"])
        X["mpg_per_engine"] = X["mpg"] / X["engineSize"].replace(0, 0.1)
        X["tax_per_engine"] = X["tax"] / X["engineSize"].replace(0, 0.1)

        # Binary features
        X["is_automatic"] = (X["transmission"] == "Automatic").astype(int)
        X["is_diesel"] = (X["fuelType"] == "Diesel").astype(int)

        # One-hot encoding for transmission/fuelType
        X = pd.get_dummies(X, columns=["transmission", "fuelType"], drop_first=True)

        # Label encode model
        if self.le_model is not None:
            X["model"] = self.le_model.transform(X["model"])
        return X

# -----------------------------
# 2️⃣ Column lists
# -----------------------------
numeric_cols = ['year', 'mileage', 'log_mileage', 'mpg', 'tax', 'car_age', 
                'mileage_per_year', 'log_tax', 'mpg_per_engine', 'tax_per_engine']
binary_cols = ['is_automatic', 'is_diesel']
# One-hot and model already handled in FeatureBuilder

# -----------------------------
# 3️⃣ Pipelines
# -----------------------------
numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('to_float', FunctionTransformer(lambda x: x.astype(float)))
])

binary_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
    ('to_float', FunctionTransformer(lambda x: x.astype(float)))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_cols),
        ('bin', binary_transformer, binary_cols)
        # All categorical handled in FeatureBuilder
    ]
)

# -----------------------------
# 4️⃣ Full pipeline
# -----------------------------
full_pipeline = Pipeline([
    ('features', FeatureBuilder()),  # apply feature engineering
    ('preprocessor', preprocessor)   # numeric + binary transformations
])

# -----------------------------
# 5️⃣ Fit pipeline on training data
# -----------------------------
X_train_final_transformed = full_pipeline.fit_transform(X_train)  # X_train is raw features

# -----------------------------
# 6️⃣ Save for production
# -----------------------------
joblib.dump(full_pipeline, 'preprocessor.pkl')
print("preprocessor.pkl saved!")

import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer

CURRENT_YEAR = 2025

class FeatureBuilder(BaseEstimator, TransformerMixin):
    def __init__(self, le_model=None):
        self.le_model = le_model

    def fit(self, X, y=None):
        return self

    def transform(self, X):
        X = X.copy()
        X["car_age"] = CURRENT_YEAR - X["year"]
        X["mileage_per_year"] = X["mileage"] / X["car_age"].replace(0,1)
        X["log_mileage"] = np.log1p(X["mileage"])
        X["log_tax"] = np.log1p(X["tax"])
        X["mpg_per_engine"] = X["mpg"] / X["engineSize"].replace(0, 0.1)
        X["tax_per_engine"] = X["tax"] / X["engineSize"].replace(0, 0.1)

        X["is_automatic"] = (X["transmission"] == "Automatic").astype(int)
        X["is_diesel"] = (X["fuelType"] == "Diesel").astype(int)

        X = pd.get_dummies(X, columns=["transmission", "fuelType"], drop_first=True)
        if self.le_model is not None:
            X["model"] = self.le_model.transform(X["model"])
        return X

numeric_cols = ['year', 'mileage', 'log_mileage', 'mpg', 'tax', 'car_age',
                'mileage_per_year', 'log_tax', 'mpg_per_engine', 'tax_per_engine']
binary_cols = ['is_automatic', 'is_diesel']

numeric_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='median')),
    ('to_float', FunctionTransformer(lambda x: x.astype(float)))
])

binary_transformer = Pipeline([
    ('imputer', SimpleImputer(strategy='constant', fill_value=0)),
    ('to_float', FunctionTransformer(lambda x: x.astype(float)))
])

full_pipeline = Pipeline([
    ('features', FeatureBuilder()),
    ('preprocessor', ColumnTransformer([
        ('num', numeric_transformer, numeric_cols),
        ('bin', binary_transformer, binary_cols)
    ]))
])

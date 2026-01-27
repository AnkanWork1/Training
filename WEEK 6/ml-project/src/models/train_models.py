# models/train_models.py
from pathlib import Path
import joblib

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.neural_network import MLPRegressor

# OPTIONAL: comment this if xgboost not installed
from xgboost import XGBRegressor


# Resolve models directory safely (src/models/)
BASE_DIR = Path(__file__).resolve().parent.parent
MODELS_DIR = BASE_DIR / "models"
MODELS_DIR.mkdir(parents=True, exist_ok=True)


# Model training functions
def train_linear_regression(X_train, y_train):
    model = LinearRegression()
    model.fit(X_train, y_train)
    joblib.dump(model, MODELS_DIR / "linear_reg.pkl")
    return model


def train_random_forest(X_train, y_train):
    model = RandomForestRegressor(
        n_estimators=200,
        random_state=42,
        n_jobs=-1
    )
    model.fit(X_train, y_train)
    joblib.dump(model, MODELS_DIR / "random_forest.pkl")
    return model


def train_xgboost(X_train, y_train):
    model = XGBRegressor(
        n_estimators=200,
        random_state=42,
        verbosity=0
    )
    model.fit(X_train, y_train)
    joblib.dump(model, MODELS_DIR / "xgboost.pkl")
    return model


def train_neural_network(X_train, y_train):
    model = MLPRegressor(
        hidden_layer_sizes=(64, 32),
        max_iter=500,
        random_state=42
    )
    model.fit(X_train, y_train)
    joblib.dump(model, MODELS_DIR / "neural_net.pkl")
    return model

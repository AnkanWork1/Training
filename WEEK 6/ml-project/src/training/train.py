import pandas as pd
import joblib
import json
from pathlib import Path

from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Model training functions
from models.train_models import (
    train_linear_regression,
    train_random_forest,
    train_xgboost,
    train_neural_network
)

def train_all_models(X_train, X_test, y_train, y_test):
    """
    Trains multiple regression models, evaluates them, 
    saves all models and the best model, and returns metrics.
    """
    # Train models
    models = {
        "LinearRegression": train_linear_regression(X_train, y_train),
        "RandomForest": train_random_forest(X_train, y_train),
        "XGBoost": train_xgboost(X_train, y_train),
        "NeuralNetwork": train_neural_network(X_train, y_train)
    }

    # Evaluate models
    metrics = {}
    best_model_name = None
    best_r2 = -float('inf')
    best_model_obj = None

    for name, model in models.items():
        y_pred = model.predict(X_test)
        mae = mean_absolute_error(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)
        rmse = mse ** 0.5

        r2 = r2_score(y_test, y_pred)
        cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring='r2')
        cv_mean = cv_scores.mean()

        metrics[name] = {"MAE": mae, "RMSE": rmse, "R2": r2, "CV_R2_mean": cv_mean}

        if r2 > best_r2:
            best_r2 = r2
            best_model_name = name
            best_model_obj = model
            
        print(f"{name}: Test R2={r2:.4f}, 5-Fold CV R2={cv_mean:.4f}")
    
    BASE_DIR = Path(__file__).parent.parent  
    
    MODELS_DIR = BASE_DIR / "models"
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    
    EVAL_DIR = BASE_DIR / "evaluation"
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    
    # Save all models
    for name, model in models.items():
        joblib.dump(model, MODELS_DIR / f"{name}.pkl")
    
    # Save best model
    joblib.dump(best_model_obj, MODELS_DIR / "best_model.pkl")
    

    # Save metrics
    with open(EVAL_DIR / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=4)

    print(f"Best model: {best_model_name} with R2={best_r2:.4f}")
    print("All models and metrics saved.")

    return models, best_model_obj, metrics

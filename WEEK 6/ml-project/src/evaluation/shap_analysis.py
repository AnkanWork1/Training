# src/evaluation/shap_analysis.py

import shap
import joblib
import matplotlib.pyplot as plt
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
EVAL_DIR = BASE_DIR / "evaluation"

EVAL_DIR.mkdir(parents=True, exist_ok=True)


def run_shap_analysis(X_train):
    """
    Generate SHAP summary plot
    """

    model = joblib.load(MODELS_DIR / "xgb_tuned_optuna.pkl")

    explainer = shap.Explainer(model, X_train)
    shap_values = explainer(X_train)

    plt.figure()
    shap.summary_plot(shap_values, X_train, show=False)
    plt.savefig(EVAL_DIR / "shap_summary.png", bbox_inches="tight")
    plt.close()

    print("SHAP analysis completed")

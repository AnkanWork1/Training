# src/evaluation/feature_importance.py

import matplotlib.pyplot as plt
import joblib
from pathlib import Path
import pandas as pd

# Paths
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
FIGURES_DIR = BASE_DIR / "evaluation"
FIGURES_DIR.mkdir(exist_ok=True, parents=True)

# Load the trained model
model = joblib.load(MODELS_DIR / "xgb_tuned_optuna.pkl")  # or best_model.pkl

# Load feature names (if you have X_train_final as DataFrame)
import pandas as pd
feature_names = list(pd.read_csv("/home/ankanguha/Desktop/Training/WEEK 6/ml-project/data/processed/bmw_final.csv").drop(columns=['price']).columns)

# Feature importances
importances = model.feature_importances_

# Sort features
sorted_idx = importances.argsort()
plt.figure(figsize=(8,6))
plt.barh(range(len(sorted_idx)), importances[sorted_idx], color="skyblue")
plt.yticks(range(len(sorted_idx)), [feature_names[i] for i in sorted_idx])
plt.xlabel("Feature Importance")
plt.title("Feature Importance Chart")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "feature_importance.png")
plt.show()

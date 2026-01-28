# src/evaluation/error_analysis.py

import matplotlib.pyplot as plt
import seaborn as sns
import joblib
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
FIGURES_DIR = BASE_DIR / "evaluation"
FIGURES_DIR.mkdir(exist_ok=True, parents=True)

# Load model
model = joblib.load(MODELS_DIR / "xgb_tuned_optuna.pkl")  # your tuned model

# Load test data
df = pd.read_csv("/home/ankanguha/Desktop/Training/WEEK 6/ml-project/data/processed/bmw_final.csv")
X_test = df.drop(columns=['price']).iloc[-50:]  # last 50 for example
y_test = df['price'].iloc[-50:]

# Predictions
y_pred = model.predict(X_test)
errors = y_test - y_pred

# Convert to DataFrame for heatmap (reshaped for 2D view)
error_df = pd.DataFrame({'error': errors, 'index': range(len(errors))})
error_matrix = error_df.pivot_table(index='index', values='error', aggfunc='mean')

plt.figure(figsize=(10,2))
sns.heatmap(error_matrix.T, cmap="coolwarm", center=0, cbar_kws={'label': 'Prediction Error'})
plt.title("Error Analysis Heatmap")
plt.tight_layout()
plt.savefig(FIGURES_DIR / "error_analysis_heatmap.png")
plt.show()

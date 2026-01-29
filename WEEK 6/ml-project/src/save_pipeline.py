from models.preprocessor_module import full_pipeline
import joblib
import pandas as pd

# Load raw training data
X_train = pd.read_csv("../data/processed/bmw_final.csv").drop(columns=["price"])

# Fit the pipeline
full_pipeline.fit(X_train)

# Save pipeline
joblib.dump(full_pipeline, "models/preprocessor.pkl")
print("✅ Preprocessor saved")

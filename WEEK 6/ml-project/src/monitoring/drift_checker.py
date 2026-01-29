import pandas as pd
from scipy.stats import ks_2samp
import os

LOG_FILE = os.path.join(os.path.dirname(__file__), "../prediction_logs.csv")
REFERENCE_FILE = os.path.join(os.path.dirname(__file__), "../data/processed/final.csv")

FEATURES = ['year', 'mileage', 'log_mileage', 'mpg', 'model', 'tax', 
            'transmission_Semi-Auto', 'transmission_Manual', 'is_automatic', 'is_diesel']

def check_data_drift():
    if not os.path.exists(LOG_FILE):
        print("No prediction logs found.")
        return

    logs = pd.read_csv(LOG_FILE)
    reference = pd.read_csv(REFERENCE_FILE)

    drift_report = {}

    for col in FEATURES:
        # Handle categorical/text column differently
        if reference[col].dtype == 'object':
            # simple check: unique value overlap
            ref_vals = set(reference[col])
            log_vals = set(logs[col])
            drifted = not log_vals.issubset(ref_vals)
            drift_report[col] = {"drifted": drifted, "unique_ref": len(ref_vals), "unique_logs": len(log_vals)}
        else:
            stat, p_value = ks_2samp(reference[col], logs[col])
            drift_report[col] = {"ks_stat": stat, "p_value": p_value, "drifted": p_value < 0.05}

    for feature, res in drift_report.items():
        print(f"{feature}: {res}")

if __name__ == "__main__":
    check_data_drift()

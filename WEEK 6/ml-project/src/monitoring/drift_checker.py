from pathlib import Path

import pandas as pd
from scipy.stats import ks_2samp


# -------------------------------------------------------
# Project root (ml-project)
# -------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]

LOG_FILE = BASE_DIR / "src"/"prediction_logs.csv"
REFERENCE_FILE = BASE_DIR / "data" / "processed" / "bmw_final.csv"


FEATURES = [
    "year",
    "mileage",
    "log_mileage",
    "mpg",
    "model",
    "tax",
    "transmission_Semi-Auto",
    "transmission_Manual",
    "is_automatic",
    "is_diesel",
]


def check_data_drift(alpha: float = 0.05):

    if not LOG_FILE.exists():
        print(f"[ERROR] Prediction log file not found: {LOG_FILE}")
        return

    if not REFERENCE_FILE.exists():
        print(f"[ERROR] Reference file not found: {REFERENCE_FILE}")
        return

    logs = pd.read_csv(LOG_FILE)
    reference = pd.read_csv(REFERENCE_FILE)

    drift_report = {}

    for col in FEATURES:

        if col not in logs.columns:
            drift_report[col] = {"error": "column missing in logs"}
            continue

        if col not in reference.columns:
            drift_report[col] = {"error": "column missing in reference"}
            continue

        ref_col = reference[col].dropna()
        log_col = logs[col].dropna()

        if len(ref_col) == 0 or len(log_col) == 0:
            drift_report[col] = {"error": "empty column after NaN removal"}
            continue

        # -------------------------------------------------
        # Categorical (object / string)
        # -------------------------------------------------
        if ref_col.dtype == "object":

            ref_vals = set(ref_col.astype(str).unique())
            log_vals = set(log_col.astype(str).unique())

            unseen_categories = list(log_vals - ref_vals)

            drift_report[col] = {
                "type": "categorical",
                "n_unique_reference": len(ref_vals),
                "n_unique_logs": len(log_vals),
                "n_unseen_in_logs": len(unseen_categories),
                "unseen_examples": unseen_categories[:5],
                "drifted": len(unseen_categories) > 0,
            }

        # -------------------------------------------------
        # Numerical
        # -------------------------------------------------
        else:
            stat, p_value = ks_2samp(ref_col, log_col)

            drift_report[col] = {
                "type": "numerical",
                "ks_stat": float(stat),
                "p_value": float(p_value),
                "alpha": alpha,
                "drifted": p_value < alpha,
            }

    print("\n========== DATA DRIFT REPORT ==========\n")

    for feature, res in drift_report.items():
        print(f"{feature} -> {res}")

    print("\n======================================\n")


if __name__ == "__main__":
    check_data_drift()

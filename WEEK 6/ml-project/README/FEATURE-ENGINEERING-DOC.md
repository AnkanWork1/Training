# FEATURE ENGINEERING & SELECTION DOCUMENTATION

## 1. Objective
Transform raw BMW vehicle data into a high-quality feature set suitable for regression modeling.

## 2. Feature Engineering Pipeline
Implemented in `/features/build_features.py`.

### Categorical Encoding
- `transmission` → binary (`is_automatic`)
- `fuelType` → binary (`is_diesel`)
- `model` → one-hot encoded

### Numerical Transformations
- `log_mileage`
- `car_age`
- `mileage_per_year`
- `mpg_per_engine`
- `tax_per_engine`

### Scaling
- Applied **StandardScaler** where required (model-specific)

## 3. Generated Features
Total engineered features: **18**

Examples:
- `car_age`
- `log_mileage`
- `mileage_per_year`
- `mpg_per_engine`
- `tax_per_engine`

## 4. Feature Selection

### Step 1: Correlation Filtering
- Threshold: **0.85**
- Removed highly correlated features:
  - `car_age`
  - `mileage_per_year`
  - `log_tax`
  - `mpg_per_engine`
  - `tax_per_engine`

### Step 2: Mutual Information
- Selected features with MI score > 0.01
- Top features:
  - `year`
  - `mileage`
  - `log_mileage`
  - `mpg`
  - `tax`

### Step 3: Recursive Feature Elimination (RFE)
Final selected features:
year
log_mileage
mpg
is_automatic
is_diesel


## 4. Final Dataset
- **X shape**: (3780, 5)
- **y shape**: (3780,)

## 5. Outputs
- Feature selection logic saved in:

/features/feature_selector.py
- Feature importance visualized via Mutual Information plot

## 6. Conclusion
Feature engineering and selection significantly reduced dimensionality while preserving predictive power.

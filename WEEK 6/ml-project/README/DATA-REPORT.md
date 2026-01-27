# DATA REPORT — BMW Price Prediction

## 1. Dataset Overview
- **Source**: BMW Used Car Dataset
- **Initial Rows**: 10,781
- **Final Rows after Cleaning**: 4,726
- **Target Variable**: `price`

## 2. Data Pipeline Summary
Steps applied in `/pipelines/data_pipeline.py`:

1. Loaded raw data from `/data/raw/bmw.csv`
2. Removed duplicate records
3. Handled missing values using **median imputation**
4. Removed outliers using **IQR method**
5. Saved cleaned data to `/data/processed/bmw_final.csv`

## 3. Missing Values
- Only `price` had missing values
- Filled using **median value**

## 4. Outlier Treatment
Outliers removed using IQR for:
- `year`
- `price`
- `mileage`
- `tax`
- `mpg`
- `engineSize`

This significantly reduced skewness and variance.

## 5. Exploratory Data Analysis (EDA)

### Correlation Matrix
- Strong correlation between engineered mileage-related features
- Multicollinearity handled in feature selection phase

### Feature Distributions
- `price` is right-skewed
- `mileage` and `tax` show heavy tails

### Target Distribution
- Price distribution normalized after outlier removal

### Missing Values Heatmap
- No missing values remain after preprocessing

## 6. Final Output
- Cleaned dataset saved as:

/data/processed/bmw_final.csv

## 7. Conclusion
The dataset is clean, consistent, and ready for feature engineering and model training.

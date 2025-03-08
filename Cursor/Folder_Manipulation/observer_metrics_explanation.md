# Observer Metrics Explanation

This document explains each metric used in the observer comparison analysis, what they mean, and how to interpret them.

## Basic Statistics

### Number of Valid Cases
- **What it is**: The number of kidney measurements where both observers (AIRA and SREENADH) have provided values
- **Example**: If "Number of Valid Cases = 10", it means there are 10 kidneys that both observers measured
- **Interpretation**: Higher numbers provide more reliable statistical comparisons

### Volume Measurements

#### AIRA/SREENADH Mean Volume
- **What it is**: The average volume measured by each observer
- **Example**: 
  - AIRA Mean Volume = 132.68 ml
  - SREENADH Mean Volume = 133.01 ml
- **Interpretation**: Similar means suggest no systematic bias between observers

#### AIRA/SREENADH Volume Range
- **What it is**: The minimum and maximum volumes measured by each observer
- **Example**: AIRA Range = 106.49 - 176.01 ml
- **Interpretation**: Shows the spread of measurements and helps identify potential outliers

## Agreement Metrics

### Mean Absolute Error (MAE)
- **What it is**: Average absolute difference between AIRA and SREENADH measurements
- **Example**: MAE = 1.988 ml means on average, measurements differ by about 2 ml
- **Interpretation**: Lower values indicate better agreement
  - < 5 ml: Excellent agreement
  - 5-10 ml: Good agreement
  - > 10 ml: Poor agreement

### Root Mean Squared Error (RMSE)
- **What it is**: Square root of the average squared differences (gives more weight to larger differences)
- **Example**: RMSE = 3.558 ml
- **Interpretation**: Similar to MAE but penalizes larger differences more heavily
  - Should be larger than MAE
  - Difference between RMSE and MAE indicates variability in disagreements

### Mean Difference (AIRA - SREENADH)
- **What it is**: Average difference between AIRA and SREENADH measurements
- **Example**: -0.34 ml means AIRA's measurements are on average 0.34 ml lower than SREENADH's
- **Interpretation**: Values close to 0 indicate no systematic bias between observers

### Mean Percentage Difference
- **What it is**: Average absolute percentage difference between measurements
- **Example**: 1.55% means measurements typically differ by 1.55% of the volume
- **Interpretation**:
  - < 5%: Excellent agreement
  - 5-10%: Good agreement
  - > 10%: Notable differences

## Correlation Metrics

### Pearson Correlation
- **What it is**: Measures linear correlation between observers' measurements
- **Example**: 0.991 indicates very strong positive correlation
- **Interpretation**:
  - > 0.9: Very strong correlation
  - 0.7-0.9: Strong correlation
  - 0.5-0.7: Moderate correlation
  - < 0.5: Weak correlation

### Spearman Correlation
- **What it is**: Measures rank correlation (monotonic relationship)
- **Example**: 0.964 indicates very strong rank correlation
- **Interpretation**: Similar to Pearson but less sensitive to outliers

### R-squared Score
- **What it is**: Proportion of variance in one observer's measurements explained by the other
- **Example**: 0.975 means 97.5% of variance is explained
- **Interpretation**:
  - > 0.9: Excellent agreement
  - 0.7-0.9: Good agreement
  - < 0.7: Poor agreement

## Statistical Tests

### Paired t-test
- **What it is**: Tests if there's a significant difference between observers' measurements
- **Example**: p-value = 0.782
- **Interpretation**:
  - p < 0.05: Statistically significant difference
  - p ≥ 0.05: No statistically significant difference

### Standard Deviation of Differences
- **What it is**: Measures consistency of differences between observers
- **Example**: 3.54 ml means differences typically vary by ±3.54 ml around the mean difference
- **Interpretation**: Lower values indicate more consistent differences

## Example Interpretation

Using the Right Kidney measurements as an example:
```
Mean Absolute Error: 1.988 ml
Mean Percentage Difference: 1.55%
Pearson Correlation: 0.991
p-value: 0.782
```

This indicates:
1. Excellent agreement (MAE < 5 ml, percentage difference < 5%)
2. Very strong correlation (> 0.9)
3. No statistically significant differences (p > 0.05)
4. High reliability between observers

## Threshold Analysis

The analysis also flags cases where differences exceed 15% threshold:
- **What it is**: Identifies individual cases with large discrepancies
- **Example**: If Right_Exceeds_Threshold = True, the difference for that kidney is > 15%
- **Purpose**: Helps identify specific cases that might need review or discussion between observers 
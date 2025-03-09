# Observer Analysis Formulas and Calculations

This document details all formulas and calculations used in the observer comparison analysis.

## Basic Statistics

### Valid Cases
- Number of cases where both observers have non-null measurements
```python
valid_cases = len(valid_data)  # valid_data contains rows where both observers have measurements
```

### Mean Volume
- Average volume measured by each observer
```python
mean_volume = sum(measurements) / len(measurements)
```

### Volume Range
- Minimum and maximum volumes for each observer
```python
min_volume = min(measurements)
max_volume = max(measurements)
```

## Agreement Metrics

### Mean Absolute Error (MAE)
- Average absolute difference between observers' measurements
```python
MAE = (1/n) * Σ|x₁ᵢ - x₂ᵢ|
# where:
# n = number of measurements
# x₁ᵢ = measurement by observer 1
# x₂ᵢ = measurement by observer 2
```

### Root Mean Squared Error (RMSE)
- Square root of the average squared differences
```python
RMSE = √[(1/n) * Σ(x₁ᵢ - x₂ᵢ)²]
```

### Mean Difference
- Average difference between observers
```python
mean_diff = (1/n) * Σ(x₁ᵢ - x₂ᵢ)
```

### Median Difference
- Middle value of all differences between observers
```python
median_diff = median(x₁ᵢ - x₂ᵢ)
```

### Mean Percentage Difference
- Average absolute percentage difference between observers
```python
mean_percent_diff = (1/n) * Σ|((x₁ᵢ - x₂ᵢ) / x₁ᵢ) * 100|
```

### Standard Deviation of Differences
- Spread of differences between observers
```python
std_diff = √[(1/n) * Σ((diff_i - mean_diff)²)]
# where:
# diff_i = x₁ᵢ - x₂ᵢ
# mean_diff = average difference
```

## Correlation Metrics

### R-squared Score (Coefficient of Determination)
- Proportion of variance in one observer's measurements explained by the other
```python
R² = 1 - (Σ(x₁ᵢ - x₂ᵢ)²) / (Σ(x₁ᵢ - mean(x₁))²)
```

### Pearson Correlation
- Linear correlation between observers' measurements
```python
r = Σ((x₁ᵢ - mean(x₁))(x₂ᵢ - mean(x₂))) / √[Σ(x₁ᵢ - mean(x₁))² * Σ(x₂ᵢ - mean(x₂))²]
```

### Spearman Correlation
- Rank correlation between observers' measurements
```python
ρ = 1 - (6 * Σd²) / (n * (n² - 1))
# where:
# d = difference in ranks
# n = number of measurements
```

## Statistical Tests

### Paired t-test
- Tests for significant differences between observers
```python
t = (mean_diff) / (std_diff / √n)
# where:
# mean_diff = average difference
# std_diff = standard deviation of differences
# n = number of pairs
```

### Degrees of Freedom
```python
df = n - 1
# where n = number of pairs
```

### P-value
- Calculated from t-statistic and degrees of freedom using t-distribution

## Threshold Analysis

### Percentage Difference Threshold
- Identifies cases exceeding specified difference threshold (default: 15%)
```python
exceeds_threshold = |((x₁ᵢ - x₂ᵢ) / x₁ᵢ) * 100| > threshold_percentage
```

## Total Volume Calculations

### Total Kidney Volume
- Sum of Right and Left kidney volumes for each observer
```python
total_volume = right_kidney_volume + left_kidney_volume
```

### Total Volume Difference
- Difference in total volumes between observers
```python
total_diff = total_volume_obs1 - total_volume_obs2
```

### Total Volume Percentage Difference
- Percentage difference in total volumes
```python
total_percent_diff = ((total_volume_obs1 - total_volume_obs2) / total_volume_obs1) * 100
```

## Interpretation Guidelines

### Correlation Strength
- Very Strong: > 0.9
- Strong: 0.7 - 0.9
- Moderate: 0.5 - 0.7
- Weak: < 0.5

### Agreement Quality
- Excellent: Mean % diff < 5%
- Good: Mean % diff 5-10%
- Poor: Mean % diff > 10%

### Statistical Significance
- Significant: p-value < 0.05
- Not Significant: p-value ≥ 0.05

## Implementation Notes

1. All calculations are performed on valid pairs only (where both observers have measurements)
2. Missing values are excluded from calculations
3. Rounding:
   - Volume measurements: 2 decimal places
   - Correlation metrics: 3 decimal places
   - Statistical tests: 3 decimal places
   - Percentages: 2 decimal places

## Python Libraries Used

- NumPy: Basic statistical calculations
- SciPy: Statistical tests and correlations
- scikit-learn: Error metrics and R-squared calculation 
# Kidney Volume Analysis Metrics Explained

This document explains all the metrics and visualizations used to compare kidney volumes measured at 2.5mm and 5.0mm slice thicknesses.

## Table of Contents
1. [Basic Statistical Metrics](#basic-statistical-metrics)
2. [Correlation Metrics](#correlation-metrics)
3. [Error Metrics](#error-metrics)
4. [Statistical Tests](#statistical-tests)
5. [Visualizations](#visualizations)
6. [Technical Details](#technical-details)

## Basic Statistical Metrics

### Mean Volume Difference
- **What it measures**: The average difference between volumes measured at 2.5mm and 5.0mm
- **How to interpret**: 
  - Positive value: 2.5mm measurements tend to be larger
  - Negative value: 5.0mm measurements tend to be larger
  - Value close to 0: measurements are similar on average
- **Example**: If 2.5mm measurement = 150ml and 5.0mm measurement = 140ml, the difference is 10ml
- **Formula**: Average of (2.5mm volume - 5.0mm volume) for all cases

### Median Volume Difference
- **What it measures**: The middle value of all volume differences
- **Why it's useful**: Less sensitive to extreme values than the mean
- **How to interpret**: Similar to mean difference, but represents the "typical" difference better if there are outliers
- **Example**: For differences [5, 8, 10, 15, 100], median = 10 (more representative than mean = 27.6)

## Correlation Metrics

### Pearson Correlation
- **What it measures**: How linearly related the 2.5mm and 5.0mm measurements are
- **Range**: -1 to +1
  - +1: Perfect positive correlation (measurements increase together)
  - 0: No correlation
  - -1: Perfect negative correlation
- **How to interpret**: Higher positive values mean stronger agreement between measurements
- **Example**: 0.95 would indicate very strong agreement between 2.5mm and 5.0mm measurements

### Spearman Correlation
- **What it measures**: Similar to Pearson, but measures monotonic relationships (can capture non-linear relationships)
- **When to use**: When relationship might not be perfectly linear
- **Range and interpretation**: Same as Pearson correlation
- **Example**: Useful if larger kidneys show more variation between measurements

## Error Metrics

### Mean Absolute Error (MAE)
- **What it measures**: Average absolute difference between measurements
- **Why it's useful**: Easy to understand, represents typical error magnitude
- **Example**: 
  - Measurement 1: [100, 150, 200]
  - Measurement 2: [105, 140, 210]
  - Differences: [5, 10, 10]
  - MAE = (5 + 10 + 10) ÷ 3 = 8.33

### Root Mean Square Error (RMSE)
- **What it measures**: Square root of average squared differences
- **Why it's useful**: Penalizes larger errors more heavily than MAE
- **How to interpret**: Higher values indicate more variation between measurements
- **Example**:
  - Using same measurements as above
  - Squared differences: [25, 100, 100]
  - Mean of squares = 75
  - RMSE = √75 ≈ 8.66

### Mean Percentage Error
- **What it measures**: Average percentage difference between measurements
- **Why it's useful**: Shows relative size of errors
- **Example**:
  - 2.5mm measurement = 100ml, 5.0mm = 110ml → 10% error
  - 2.5mm measurement = 200ml, 5.0mm = 220ml → 10% error
  - Same percentage despite different absolute differences

## Statistical Tests

### Paired t-test
- **What it measures**: Whether there's a significant systematic difference between 2.5mm and 5.0mm measurements
- **How to interpret**: 
  - p-value < 0.05: significant systematic difference exists
  - p-value ≥ 0.05: no significant systematic difference
- **Example**: p-value = 0.03 would suggest systematic differences between measurement methods

## Visualizations

### Scatter Plot
- **What it shows**: Direct comparison of 2.5mm vs 5.0mm measurements
- **How to read**:
  - Points along diagonal line: perfect agreement
  - Points above/below line: systematic differences
  - Spread of points: measurement variability

### Bland-Altman Plot
- **What it shows**: Agreement between measurement methods
- **Key features**:
  - X-axis: Average of two measurements
  - Y-axis: Difference between measurements
  - Red line: Mean difference
  - Green lines: 95% limits of agreement
- **How to interpret**:
  - Points clustered around zero difference: good agreement
  - Pattern in differences: systematic bias
  - Wider spread at higher values: proportional errors

### Box Plot
- **What it shows**: Distribution of measurements for each method
- **Key features**:
  - Box: 25th to 75th percentile
  - Line in box: median
  - Whiskers: range of typical values
  - Points: outliers
- **How to interpret**: Compare distributions between methods

### Case-wise Comparison
- **What it shows**: Individual measurements across all cases
- **How to read**:
  - X-axis: Case number
  - Y-axis: Volume
  - Different lines: Different measurement methods
  - Pattern comparison: Visual assessment of agreement

## Technical Details

For those interested in the implementation details, here's how each metric is calculated in the code:

### Basic Statistics
```python
# Mean Volume Difference
mean_diff = np.mean(df['Right_2.5mm'] - df['Right_5.0mm'])

# Median Volume Difference
median_diff = np.median(df['Right_2.5mm'] - df['Right_5.0mm'])
```

### Correlation Metrics
```python
# Pearson Correlation
pearson_corr = stats.pearsonr(df['Right_2.5mm'], df['Right_5.0mm'])[0]

# Spearman Correlation
spearman_corr = stats.spearmanr(df['Right_2.5mm'], df['Right_5.0mm'])[0]
```

### Error Metrics
```python
# Mean Absolute Error
mae = mean_absolute_error(df['Right_2.5mm'], df['Right_5.0mm'])

# Root Mean Square Error
rmse = np.sqrt(mean_squared_error(df['Right_2.5mm'], df['Right_5.0mm']))

# Mean Percentage Error
mpe = np.mean(np.abs((df['Right_2.5mm'] - df['Right_5.0mm']) / df['Right_2.5mm'])) * 100
```

### Statistical Tests
```python
# Paired t-test
t_stat, p_value = stats.ttest_rel(df['Right_2.5mm'], df['Right_5.0mm'])
```

The same calculations are performed for both right and left kidneys separately to provide a comprehensive comparison of the measurement methods. 
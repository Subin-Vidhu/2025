import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns

# Load the DICOM metadata (updated path since we're in the FDA folder)
df = pd.read_csv('orthanc_series_metadata.csv')

# Define problematic patient IDs
problem_ids = ['N-012', 'N-016', 'N-023', 'N-051', 'N-088', 'N-090', 
               'N-092', 'N-101', 'N-126', 'N-135']

# Add a flag to identify problematic cases
df['is_problematic'] = df['PatientName'].isin(problem_ids)

# Basic summary statistics
print(f"Total studies: {len(df['PatientName'].unique())}")
print(f"Problem cases: {len(problem_ids)}")
print(f"Number of records: {len(df)}")
print(f"Number of problematic records: {len(df[df['is_problematic']])}")

# Function to analyze differences in categorical columns
def analyze_categorical_differences(df, column):
    if column not in df.columns:
        return None
    
    # Check if column has mostly non-null values
    if df[column].isna().sum() / len(df) > 0.5:
        return None
    
    problem_counts = df[df['is_problematic']][column].value_counts(normalize=True)
    normal_counts = df[~df['is_problematic']][column].value_counts(normalize=True)
    
    # Combine the results
    combined = pd.DataFrame({
        'Problematic': problem_counts,
        'Normal': normal_counts
    }).fillna(0)
    
    # Calculate absolute difference
    combined['Difference'] = abs(combined['Problematic'] - combined['Normal'])
    
    # Sort by difference
    combined = combined.sort_values('Difference', ascending=False)
    
    return combined.head(10)  # Return top 10 differences

# Function to analyze differences in numerical columns
def analyze_numerical_differences(df, column):
    if column not in df.columns:
        return None
    
    # Try to convert to numeric, ignoring errors
    try:
        df[column] = pd.to_numeric(df[column], errors='coerce')
    except:
        return None
    
    # Check if column has mostly non-null values
    if df[column].isna().sum() / len(df) > 0.5:
        return None
    
    # Calculate statistics
    problem_stats = df[df['is_problematic']][column].describe()
    normal_stats = df[~df['is_problematic']][column].describe()
    
    # Combine the results
    combined = pd.DataFrame({
        'Problematic': problem_stats,
        'Normal': normal_stats
    })
    
    # Calculate percentage difference
    combined['Percent_Difference'] = abs(combined['Problematic'] - combined['Normal']) / normal_stats * 100
    
    # Conduct a t-test
    try:
        t_stat, p_value = stats.ttest_ind(
            df[df['is_problematic']][column].dropna(),
            df[~df['is_problematic']][column].dropna(),
            equal_var=False  # Use Welch's t-test
        )
        
        # Add these as scalar values, not Series
        combined.loc['t_stat', 'Problematic'] = t_stat
        combined.loc['p_value', 'Problematic'] = p_value
    except:
        combined.loc['t_stat', 'Problematic'] = np.nan
        combined.loc['p_value', 'Problematic'] = np.nan
    
    return combined

# Identify all numerical and categorical columns
numerical_columns = []
categorical_columns = []

for col in df.columns:
    # Skip the is_problematic column we added
    if col == 'is_problematic':
        continue
        
    # Try to convert to numeric
    try:
        pd.to_numeric(df[col], errors='raise')
        numerical_columns.append(col)
    except:
        categorical_columns.append(col)

# Analyze key numerical attributes
print("\n=== NUMERICAL ATTRIBUTES ANALYSIS ===")
significant_numerical = {}

for col in numerical_columns:
    result = analyze_numerical_differences(df, col)
    if result is not None and not pd.isna(result.loc['p_value', 'Problematic']) and result.loc['p_value', 'Problematic'] < 0.05:
        significant_numerical[col] = result.loc['p_value', 'Problematic']

# Sort and display significant numerical differences
print("\nStatistically significant differences in numerical attributes:")
for col, p_value in sorted(significant_numerical.items(), key=lambda x: x[1]):
    print(f"{col}: p-value = {p_value:.4f}")
    print(analyze_numerical_differences(df, col)[['Problematic', 'Normal']])
    print()

# Analyze key categorical attributes
print("\n=== CATEGORICAL ATTRIBUTES ANALYSIS ===")
significant_categorical = {}

for col in categorical_columns:
    result = analyze_categorical_differences(df, col)
    if result is not None and result['Difference'].max() > 0.2:  # Notable difference (>20%)
        significant_categorical[col] = result['Difference'].max()

# Sort and display significant categorical differences
print("\nNotable differences in categorical attributes:")
for col, diff in sorted(significant_categorical.items(), key=lambda x: x[1], reverse=True):
    print(f"{col}: max difference = {diff:.2f}")
    print(analyze_categorical_differences(df, col))
    print()

# Additional analysis for specific fields that might be important for kidney imaging
kidney_related_fields = [
    'Manufacturer', 'ManufacturerModelName', 'ConvolutionKernel_0018_1210',
    'SliceThickness_0018_0050', 'KVP_0018_0060', 'XRayTubeCurrent_0018_1151',
    'ExposureTime_0018_1150', 'CTDIvol_0018_9345', 'SeriesDescription', 'ImageComments_0020_4000'
]

print("\n=== KIDNEY IMAGING SPECIFIC PARAMETERS ===")
for field in kidney_related_fields:
    if field in numerical_columns:
        result = analyze_numerical_differences(df, field)
        if result is not None:
            print(f"\n{field}:")
            print(result[['Problematic', 'Normal', 'Percent_Difference']])
    elif field in categorical_columns:
        result = analyze_categorical_differences(df, field)
        if result is not None:
            print(f"\n{field}:")
            print(result)

# Create visualizations for key differences
plt.figure(figsize=(12, 10))

# Select top numerical features to visualize
top_numerical = list(significant_numerical.keys())[:5]
if top_numerical:
    for i, col in enumerate(top_numerical):
        plt.subplot(len(top_numerical), 1, i+1)
        sns.boxplot(x='is_problematic', y=col, data=df)
        plt.title(f'Distribution of {col} by Problematic Status')
        plt.xlabel('Is Problematic')
        plt.tight_layout()

    plt.savefig('numerical_features_comparison.png')
    print("\nSaved boxplot visualization to 'numerical_features_comparison.png'")

# Visualize manufacturer and model distribution
plt.figure(figsize=(12, 6))
if 'Manufacturer' in df.columns:
    plt.subplot(1, 2, 1)
    df_grouped = df.groupby(['Manufacturer', 'is_problematic']).size().unstack().fillna(0)
    df_grouped.plot(kind='bar', stacked=True)
    plt.title('Distribution by Manufacturer')
    plt.tight_layout()

if 'ManufacturerModelName' in df.columns:
    plt.subplot(1, 2, 2)
    df_grouped = df.groupby(['ManufacturerModelName', 'is_problematic']).size().unstack().fillna(0)
    df_grouped.plot(kind='bar', stacked=True)
    plt.title('Distribution by Model Name')
    plt.tight_layout()

plt.savefig('manufacturer_model_distribution.png')
print("Saved manufacturer/model visualization to 'manufacturer_model_distribution.png'")

# Print summary of findings
print("\n=== SUMMARY OF FINDINGS ===")
print("1. Key differences between problematic and normal cases:")
for col, p_value in list(significant_numerical.items())[:3]:
    result = analyze_numerical_differences(df, col)
    p_diff = result['Percent_Difference']['mean']
    print(f"   - {col}: {p_diff:.1f}% difference in means (p-value: {p_value:.4f})")

for col, diff in list(significant_categorical.items())[:3]:
    print(f"   - {col}: {diff:.2f} difference in distribution")

print("\n2. Imaging parameters that might affect kidney detection:")
for field in kidney_related_fields:
    if field in significant_numerical:
        print(f"   - {field}: Significant difference with p-value {significant_numerical[field]:.4f}")
    elif field in significant_categorical:
        print(f"   - {field}: Notable difference of {significant_categorical[field]:.2f}") 
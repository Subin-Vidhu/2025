import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.cluster import DBSCAN
from sklearn.decomposition import PCA
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Load the DICOM metadata
df = pd.read_csv('orthanc_series_metadata.csv')

print(f"Total records: {len(df)}")
print(f"Unique patients: {df['PatientName'].nunique()}")
print(f"Columns available: {len(df.columns)}")

# Step 1: Identify and prepare key segmentation-relevant parameters
segmentation_critical_params = [
    'SliceThickness_0018_0050',
    'PixelSpacing_0028_0030', 
    'ReconstructionDiameter_0018_1100',
    'KVP_0018_0060',
    'XRayTubeCurrent_0018_1151',
    'ExposureTime_0018_1150',
    'GeneratorPower_0018_1170',
    'CTDIvol_0018_9345',
    'ConvolutionKernel_0018_1210',
    'FilterType_0018_1160',
    'Manufacturer_0008_0070',
    'ManufacturerModelName_0008_1090',
    'SeriesDescription',
    'ImageComments_0020_4000'
]

# Check which parameters are available
available_params = [col for col in segmentation_critical_params if col in df.columns]
print(f"\nAvailable critical parameters: {len(available_params)}")
for param in available_params:
    print(f"  - {param}")

# Step 2: Prepare numerical features for outlier detection
def prepare_numerical_features(df, columns):
    """Convert and clean numerical columns for analysis"""
    numerical_data = pd.DataFrame()
    
    for col in columns:
        if col in df.columns:
            # Try to convert to numeric
            try:
                # Handle special cases like PixelSpacing which might have multiple values
                if 'PixelSpacing' in col:
                    # Extract first value if it's a string like "0.7\\0.7"
                    temp_series = df[col].astype(str).str.split('\\').str[0]
                    numerical_data[col] = pd.to_numeric(temp_series, errors='coerce')
                else:
                    numerical_data[col] = pd.to_numeric(df[col], errors='coerce')
            except:
                continue
    
    return numerical_data

# Step 3: Prepare categorical features
def prepare_categorical_features(df, columns):
    """Encode categorical columns for analysis"""
    categorical_data = pd.DataFrame()
    label_encoders = {}
    
    for col in columns:
        if col in df.columns:
            # Fill NaN values with 'Unknown'
            temp_series = df[col].fillna('Unknown').astype(str)
            
            # Only encode if there are multiple unique values
            if temp_series.nunique() > 1:
                le = LabelEncoder()
                categorical_data[col] = le.fit_transform(temp_series)
                label_encoders[col] = le
    
    return categorical_data, label_encoders

# Prepare the data
numerical_cols = [col for col in available_params if col not in ['ConvolutionKernel_0018_1210', 'FilterType_0018_1160', 'Manufacturer_0008_0070', 'ManufacturerModelName_0008_1090', 'SeriesDescription', 'ImageComments_0020_4000']]
categorical_cols = [col for col in available_params if col in ['ConvolutionKernel_0018_1210', 'FilterType_0018_1160', 'Manufacturer_0008_0070', 'ManufacturerModelName_0008_1090', 'SeriesDescription', 'ImageComments_0020_4000']]

numerical_features = prepare_numerical_features(df, numerical_cols)
categorical_features, encoders = prepare_categorical_features(df, categorical_cols)

print(f"\nNumerical features prepared: {numerical_features.shape[1]}")
print(f"Categorical features prepared: {categorical_features.shape[1]}")

# Step 4: Statistical outlier detection for each numerical parameter
def detect_statistical_outliers(data, method='iqr', threshold=2.5):
    """Detect outliers using IQR or Z-score methods"""
    outliers = pd.DataFrame(index=data.index)
    
    for col in data.columns:
        if data[col].notna().sum() < 3:  # Skip if too few valid values
            continue
            
        if method == 'iqr':
            Q1 = data[col].quantile(0.25)
            Q3 = data[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers[f'{col}_outlier'] = (data[col] < lower_bound) | (data[col] > upper_bound)
        
        elif method == 'zscore':
            z_scores = np.abs(stats.zscore(data[col], nan_policy='omit'))
            outliers[f'{col}_outlier'] = z_scores > threshold
    
    return outliers

# Detect outliers for numerical features
numerical_outliers = detect_statistical_outliers(numerical_features, method='iqr')
zscore_outliers = detect_statistical_outliers(numerical_features, method='zscore', threshold=2.0)

# Count outliers per case
outlier_counts = numerical_outliers.sum(axis=1)
zscore_counts = zscore_outliers.sum(axis=1)

# Step 5: Multi-dimensional outlier detection using clustering
def detect_multivariate_outliers(numerical_data, categorical_data):
    """Use DBSCAN clustering to identify multivariate outliers"""
    
    # Combine features
    combined_features = pd.concat([numerical_data, categorical_data], axis=1)
    
    # Drop rows with too many NaN values (keep rows with at least 50% valid data)
    min_valid_cols = max(1, int(len(combined_features.columns) * 0.5))
    combined_features = combined_features.dropna(thresh=min_valid_cols)
    
    if combined_features.empty or combined_features.shape[0] < 5:
        print("Warning: Not enough data for multivariate outlier detection")
        return pd.Series(False, index=numerical_data.index)
    
    print(f"Multivariate analysis: Using {combined_features.shape[0]} rows with {combined_features.shape[1]} features")
    
    # Handle remaining NaN values more robustly
    for col in combined_features.columns:
        if combined_features[col].dtype in ['float64', 'int64']:
            # For numerical: use median, if all NaN use 0
            median_val = combined_features[col].median()
            if pd.isna(median_val):
                median_val = 0
            combined_features[col] = combined_features[col].fillna(median_val)
        else:
            # For categorical: use mode, if no mode use most frequent or 0
            try:
                mode_val = combined_features[col].mode()
                if len(mode_val) > 0 and not pd.isna(mode_val.iloc[0]):
                    fill_val = mode_val.iloc[0]
                else:
                    fill_val = 0
            except:
                fill_val = 0
            combined_features[col] = combined_features[col].fillna(fill_val)
    
    # Double-check for any remaining NaN values
    if combined_features.isnull().any().any():
        print("Warning: Still have NaN values, filling with 0")
        combined_features = combined_features.fillna(0)
    
    # Verify no infinite values
    if np.isinf(combined_features.select_dtypes(include=[np.number])).any().any():
        print("Warning: Infinite values detected, replacing with median")
        for col in combined_features.select_dtypes(include=[np.number]).columns:
            median_val = combined_features[col].replace([np.inf, -np.inf], np.nan).median()
            if pd.isna(median_val):
                median_val = 0
            combined_features[col] = combined_features[col].replace([np.inf, -np.inf], median_val)
    
    try:
        # Standardize features
        scaler = StandardScaler()
        scaled_features = scaler.fit_transform(combined_features)
        
        # Check for NaN in scaled features
        if np.isnan(scaled_features).any():
            print("Warning: NaN in scaled features, filling with 0")
            scaled_features = np.nan_to_num(scaled_features, nan=0.0, posinf=0.0, neginf=0.0)
        
        # Apply DBSCAN with adjusted parameters
        dbscan = DBSCAN(eps=1.2, min_samples=max(2, int(len(scaled_features) * 0.05)))
        clusters = dbscan.fit_predict(scaled_features)
        
        # Outliers are labeled as -1
        outlier_mask = clusters == -1
        
        print(f"DBSCAN found {sum(outlier_mask)} outliers out of {len(outlier_mask)} cases")
        
    except Exception as e:
        print(f"Error in DBSCAN: {e}")
        print("Falling back to isolation forest or simple method")
        outlier_mask = np.zeros(len(combined_features), dtype=bool)
    
    # Create full series with False for dropped indices
    full_outlier_series = pd.Series(False, index=numerical_data.index)
    full_outlier_series.loc[combined_features.index] = outlier_mask
    
    return full_outlier_series

multivariate_outliers = detect_multivariate_outliers(numerical_features, categorical_features)

# Step 6: Create comprehensive outlier scoring
df['statistical_outlier_count'] = outlier_counts
df['zscore_outlier_count'] = zscore_counts
df['multivariate_outlier'] = multivariate_outliers
df['total_outlier_score'] = outlier_counts + zscore_counts + multivariate_outliers.astype(int)

# Step 7: Identify most problematic cases
print("\n" + "="*60)
print("OUTLIER DETECTION RESULTS")
print("="*60)

# Sort by total outlier score
problematic_cases = df.sort_values('total_outlier_score', ascending=False)

print(f"\nTop 15 cases most likely to have segmentation issues:")
print("-" * 60)
top_cases = problematic_cases.head(15)[['PatientName', 'statistical_outlier_count', 'zscore_outlier_count', 'multivariate_outlier', 'total_outlier_score']]
print(top_cases.to_string(index=False))

# Step 8: Detailed analysis of top problematic cases
print(f"\n\nDETAILED ANALYSIS OF TOP 10 PROBLEMATIC CASES:")
print("="*60)

top_10_patients = problematic_cases.head(10)['PatientName'].tolist()

for patient in top_10_patients:
    patient_data = df[df['PatientName'] == patient].iloc[0]
    print(f"\nPatient: {patient}")
    print(f"Total Outlier Score: {patient_data['total_outlier_score']}")
    
    # Show specific outlier parameters
    outlier_params = []
    
    # Check which numerical parameters are outliers
    for col in numerical_features.columns:
        if f'{col}_outlier' in numerical_outliers.columns:
            if numerical_outliers.loc[patient_data.name, f'{col}_outlier']:
                value = numerical_features.loc[patient_data.name, col]
                median_val = numerical_features[col].median()
                outlier_params.append(f"  - {col}: {value:.2f} (median: {median_val:.2f})")
    
    if outlier_params:
        print("Outlier Parameters:")
        for param in outlier_params:
            print(param)
    
    # Show key technical parameters
    key_params = ['SliceThickness_0018_0050', 'KVP_0018_0060', 'ReconstructionDiameter_0018_1100', 'ConvolutionKernel_0018_1210']
    print("Key Technical Parameters:")
    for param in key_params:
        if param in df.columns:
            value = patient_data[param]
            print(f"  - {param}: {value}")

# Step 9: Parameter-specific outlier analysis
print(f"\n\nPARAMETER-SPECIFIC OUTLIER ANALYSIS:")
print("="*60)

for col in numerical_features.columns:
    if numerical_features[col].notna().sum() < 5:
        continue
        
    outlier_col = f'{col}_outlier'
    if outlier_col in numerical_outliers.columns:
        outlier_count = numerical_outliers[outlier_col].sum()
        if outlier_count > 0:
            print(f"\n{col}: {outlier_count} outliers detected")
            
            # Show outlier values vs normal range
            outlier_values = numerical_features[numerical_outliers[outlier_col]][col].dropna()
            normal_values = numerical_features[~numerical_outliers[outlier_col]][col].dropna()
            
            if len(outlier_values) > 0 and len(normal_values) > 0:
                print(f"  Normal range: {normal_values.min():.2f} - {normal_values.max():.2f} (median: {normal_values.median():.2f})")
                print(f"  Outlier range: {outlier_values.min():.2f} - {outlier_values.max():.2f}")
                
                # Show which patients have these outliers
                outlier_patients = df[numerical_outliers[outlier_col]]['PatientName'].tolist()
                if len(outlier_patients) <= 5:
                    print(f"  Patients: {', '.join(outlier_patients)}")
                else:
                    print(f"  Patients (first 5): {', '.join(outlier_patients[:5])}")

# Step 10: Create visualization
plt.figure(figsize=(15, 10))

# Plot 1: Outlier score distribution
plt.subplot(2, 3, 1)
plt.hist(df['total_outlier_score'], bins=10, edgecolor='black', alpha=0.7)
plt.xlabel('Total Outlier Score')
plt.ylabel('Number of Cases')
plt.title('Distribution of Outlier Scores')

# Plot 2: Top parameters causing outliers
plt.subplot(2, 3, 2)
outlier_param_counts = numerical_outliers.sum().sort_values(ascending=False)
if len(outlier_param_counts) > 0:
    top_params = outlier_param_counts.head(8)
    plt.barh(range(len(top_params)), top_params.values)
    plt.yticks(range(len(top_params)), [param.replace('_outlier', '').replace('_', ' ') for param in top_params.index])
    plt.xlabel('Number of Outliers')
    plt.title('Parameters with Most Outliers')

# Plot 3-6: Key parameter distributions with outliers highlighted
key_numerical_params = [col for col in ['SliceThickness_0018_0050', 'KVP_0018_0060', 'ReconstructionDiameter_0018_1100', 'GeneratorPower_0018_1170'] if col in numerical_features.columns]

for i, param in enumerate(key_numerical_params[:4]):
    plt.subplot(2, 3, i+3)
    
    # Plot normal values
    normal_mask = ~numerical_outliers.get(f'{param}_outlier', pd.Series(False, index=df.index))
    outlier_mask = numerical_outliers.get(f'{param}_outlier', pd.Series(False, index=df.index))
    
    normal_values = numerical_features[normal_mask][param].dropna()
    outlier_values = numerical_features[outlier_mask][param].dropna()
    
    if len(normal_values) > 0:
        plt.hist(normal_values, bins=15, alpha=0.7, label='Normal', color='blue')
    if len(outlier_values) > 0:
        plt.hist(outlier_values, bins=5, alpha=0.7, label='Outliers', color='red')
    
    plt.xlabel(param.replace('_', ' '))
    plt.ylabel('Frequency')
    plt.title(f'{param.split("_")[0]} Distribution')
    plt.legend()

plt.tight_layout()
plt.savefig('dicom_outlier_analysis.png', dpi=300, bbox_inches='tight')
print(f"\n\nVisualization saved as 'dicom_outlier_analysis.png'")

# Step 11: Generate final recommendations
print(f"\n\nRECOMMENDATIONS FOR SEGMENTATION QUALITY:")
print("="*60)

high_risk_patients = df[df['total_outlier_score'] >= 3]['PatientName'].tolist()
medium_risk_patients = df[df['total_outlier_score'] == 2]['PatientName'].tolist()

print(f"HIGH RISK cases (score ≥3): {len(high_risk_patients)} cases")
if len(high_risk_patients) <= 10:
    print(f"  Patients: {', '.join(high_risk_patients)}")
else:
    print(f"  Patients (first 10): {', '.join(high_risk_patients[:10])}")

print(f"\nMEDIUM RISK cases (score =2): {len(medium_risk_patients)} cases")
if len(medium_risk_patients) <= 10:
    print(f"  Patients: {', '.join(medium_risk_patients)}")

print(f"\nLOW RISK cases (score ≤1): {len(df[df['total_outlier_score'] <= 1])} cases")

print(f"\nKEY FINDINGS:")
print(f"- {len(df[df['multivariate_outlier']])} cases are multivariate outliers")
print(f"- Most common outlier parameters: {', '.join(outlier_param_counts.head(3).index)}")
print(f"- {(df['total_outlier_score'] == 0).sum()} cases have no outlier flags")

print(f"\nSUGGESTED ACTIONS:")
print("1. Review HIGH RISK cases manually before automated segmentation")
print("2. Consider separate segmentation models for different scanner types")
print("3. Implement preprocessing normalization for outlier parameters")
print("4. Set up automated quality control flags for future scans")# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from scipy import stats
# from sklearn.preprocessing import StandardScaler, LabelEncoder
# from sklearn.cluster import DBSCAN
# from sklearn.decomposition import PCA
# import seaborn as sns
# import warnings
# warnings.filterwarnings('ignore')

# # Load the DICOM metadata
# df = pd.read_csv('orthanc_series_metadata.csv')

# print(f"Total records: {len(df)}")
# print(f"Unique patients: {df['PatientName'].nunique()}")
# print(f"Columns available: {len(df.columns)}")

# # Step 1: Identify and prepare key segmentation-relevant parameters
# segmentation_critical_params = [
#     'SliceThickness_0018_0050',
#     'PixelSpacing_0028_0030', 
#     'ReconstructionDiameter_0018_1100',
#     'KVP_0018_0060',
#     'XRayTubeCurrent_0018_1151',
#     'ExposureTime_0018_1150',
#     'GeneratorPower_0018_1170',
#     'CTDIvol_0018_9345',
#     'ConvolutionKernel_0018_1210',
#     'FilterType_0018_1160',
#     'Manufacturer_0008_0070',
#     'ManufacturerModelName_0008_1090'
# ]

# # Check which parameters are available
# available_params = [col for col in segmentation_critical_params if col in df.columns]
# print(f"\nAvailable critical parameters: {len(available_params)}")
# for param in available_params:
#     print(f"  - {param}")

# # Step 2: Prepare numerical features for outlier detection
# def prepare_numerical_features(df, columns):
#     """Convert and clean numerical columns for analysis"""
#     numerical_data = pd.DataFrame()
    
#     for col in columns:
#         if col in df.columns:
#             # Try to convert to numeric
#             try:
#                 # Handle special cases like PixelSpacing which might have multiple values
#                 if 'PixelSpacing' in col:
#                     # Extract first value if it's a string like "0.7\\0.7"
#                     temp_series = df[col].astype(str).str.split('\\').str[0]
#                     numerical_data[col] = pd.to_numeric(temp_series, errors='coerce')
#                 else:
#                     numerical_data[col] = pd.to_numeric(df[col], errors='coerce')
#             except:
#                 continue
    
#     return numerical_data

# # Step 3: Prepare categorical features
# def prepare_categorical_features(df, columns):
#     """Encode categorical columns for analysis"""
#     categorical_data = pd.DataFrame()
#     label_encoders = {}
    
#     for col in columns:
#         if col in df.columns:
#             # Fill NaN values with 'Unknown'
#             temp_series = df[col].fillna('Unknown').astype(str)
            
#             # Only encode if there are multiple unique values
#             if temp_series.nunique() > 1:
#                 le = LabelEncoder()
#                 categorical_data[col] = le.fit_transform(temp_series)
#                 label_encoders[col] = le
    
#     return categorical_data, label_encoders

# # Prepare the data
# numerical_cols = [col for col in available_params if col not in ['ConvolutionKernel_0018_1210', 'FilterType_0018_1160', 'Manufacturer_0008_0070', 'ManufacturerModelName_0008_1090']]
# categorical_cols = [col for col in available_params if col in ['ConvolutionKernel_0018_1210', 'FilterType_0018_1160', 'Manufacturer_0008_0070', 'ManufacturerModelName_0008_1090']]

# numerical_features = prepare_numerical_features(df, numerical_cols)
# categorical_features, encoders = prepare_categorical_features(df, categorical_cols)

# print(f"\nNumerical features prepared: {numerical_features.shape[1]}")
# print(f"Categorical features prepared: {categorical_features.shape[1]}")

# # Step 4: Statistical outlier detection for each numerical parameter
# def detect_statistical_outliers(data, method='iqr', threshold=2.5):
#     """Detect outliers using IQR or Z-score methods"""
#     outliers = pd.DataFrame(index=data.index)
    
#     for col in data.columns:
#         if data[col].notna().sum() < 3:  # Skip if too few valid values
#             continue
            
#         if method == 'iqr':
#             Q1 = data[col].quantile(0.25)
#             Q3 = data[col].quantile(0.75)
#             IQR = Q3 - Q1
#             lower_bound = Q1 - 1.5 * IQR
#             upper_bound = Q3 + 1.5 * IQR
#             outliers[f'{col}_outlier'] = (data[col] < lower_bound) | (data[col] > upper_bound)
        
#         elif method == 'zscore':
#             z_scores = np.abs(stats.zscore(data[col], nan_policy='omit'))
#             outliers[f'{col}_outlier'] = z_scores > threshold
    
#     return outliers

# # Detect outliers for numerical features
# numerical_outliers = detect_statistical_outliers(numerical_features, method='iqr')
# zscore_outliers = detect_statistical_outliers(numerical_features, method='zscore', threshold=2.0)

# # Count outliers per case
# outlier_counts = numerical_outliers.sum(axis=1)
# zscore_counts = zscore_outliers.sum(axis=1)

# # Step 5: Multi-dimensional outlier detection using clustering
# def detect_multivariate_outliers(numerical_data, categorical_data):
#     """Use DBSCAN clustering to identify multivariate outliers"""
    
#     # Combine and standardize features
#     combined_features = pd.concat([numerical_data, categorical_data], axis=1)
    
#     # Remove rows with too many NaN values
#     combined_features = combined_features.dropna(thresh=len(combined_features.columns) * 0.5)
    
#     if combined_features.empty or combined_features.shape[0] < 5:
#         return pd.Series(False, index=numerical_data.index)
    
#     # Fill remaining NaN with median/mode
#     for col in combined_features.columns:
#         if combined_features[col].dtype in ['float64', 'int64']:
#             combined_features[col].fillna(combined_features[col].median(), inplace=True)
#         else:
#             combined_features[col].fillna(combined_features[col].mode()[0] if not combined_features[col].mode().empty else 0, inplace=True)
    
#     # Standardize features
#     scaler = StandardScaler()
#     scaled_features = scaler.fit_transform(combined_features)
    
#     # Apply DBSCAN
#     dbscan = DBSCAN(eps=1.5, min_samples=3)
#     clusters = dbscan.fit_predict(scaled_features)
    
#     # Outliers are labeled as -1
#     outlier_mask = clusters == -1
    
#     # Create full series with False for dropped indices
#     full_outlier_series = pd.Series(False, index=numerical_data.index)
#     full_outlier_series.loc[combined_features.index] = outlier_mask
    
#     return full_outlier_series

# multivariate_outliers = detect_multivariate_outliers(numerical_features, categorical_features)

# # Step 6: Create comprehensive outlier scoring
# df['statistical_outlier_count'] = outlier_counts
# df['zscore_outlier_count'] = zscore_counts
# df['multivariate_outlier'] = multivariate_outliers
# df['total_outlier_score'] = outlier_counts + zscore_counts + multivariate_outliers.astype(int)

# # Step 7: Identify most problematic cases
# print("\n" + "="*60)
# print("OUTLIER DETECTION RESULTS")
# print("="*60)

# # Sort by total outlier score
# problematic_cases = df.sort_values('total_outlier_score', ascending=False)

# print(f"\nTop 15 cases most likely to have segmentation issues:")
# print("-" * 60)
# top_cases = problematic_cases.head(15)[['PatientName', 'statistical_outlier_count', 'zscore_outlier_count', 'multivariate_outlier', 'total_outlier_score']]
# print(top_cases.to_string(index=False))

# # Step 8: Detailed analysis of top problematic cases
# print(f"\n\nDETAILED ANALYSIS OF TOP 10 PROBLEMATIC CASES:")
# print("="*60)

# top_10_patients = problematic_cases.head(10)['PatientName'].tolist()

# for patient in top_10_patients:
#     patient_data = df[df['PatientName'] == patient].iloc[0]
#     print(f"\nPatient: {patient}")
#     print(f"Total Outlier Score: {patient_data['total_outlier_score']}")
    
#     # Show specific outlier parameters
#     outlier_params = []
    
#     # Check which numerical parameters are outliers
#     for col in numerical_features.columns:
#         if f'{col}_outlier' in numerical_outliers.columns:
#             if numerical_outliers.loc[patient_data.name, f'{col}_outlier']:
#                 value = numerical_features.loc[patient_data.name, col]
#                 median_val = numerical_features[col].median()
#                 outlier_params.append(f"  - {col}: {value:.2f} (median: {median_val:.2f})")
    
#     if outlier_params:
#         print("Outlier Parameters:")
#         for param in outlier_params:
#             print(param)
    
#     # Show key technical parameters
#     key_params = ['SliceThickness_0018_0050', 'KVP_0018_0060', 'ReconstructionDiameter_0018_1100', 'ConvolutionKernel_0018_1210']
#     print("Key Technical Parameters:")
#     for param in key_params:
#         if param in df.columns:
#             value = patient_data[param]
#             print(f"  - {param}: {value}")

# # Step 9: Parameter-specific outlier analysis
# print(f"\n\nPARAMETER-SPECIFIC OUTLIER ANALYSIS:")
# print("="*60)

# for col in numerical_features.columns:
#     if numerical_features[col].notna().sum() < 5:
#         continue
        
#     outlier_col = f'{col}_outlier'
#     if outlier_col in numerical_outliers.columns:
#         outlier_count = numerical_outliers[outlier_col].sum()
#         if outlier_count > 0:
#             print(f"\n{col}: {outlier_count} outliers detected")
            
#             # Show outlier values vs normal range
#             outlier_values = numerical_features[numerical_outliers[outlier_col]][col].dropna()
#             normal_values = numerical_features[~numerical_outliers[outlier_col]][col].dropna()
            
#             if len(outlier_values) > 0 and len(normal_values) > 0:
#                 print(f"  Normal range: {normal_values.min():.2f} - {normal_values.max():.2f} (median: {normal_values.median():.2f})")
#                 print(f"  Outlier range: {outlier_values.min():.2f} - {outlier_values.max():.2f}")
                
#                 # Show which patients have these outliers
#                 outlier_patients = df[numerical_outliers[outlier_col]]['PatientName'].tolist()
#                 if len(outlier_patients) <= 5:
#                     print(f"  Patients: {', '.join(outlier_patients)}")
#                 else:
#                     print(f"  Patients (first 5): {', '.join(outlier_patients[:5])}")

# # Step 10: Create visualization
# plt.figure(figsize=(15, 10))

# # Plot 1: Outlier score distribution
# plt.subplot(2, 3, 1)
# plt.hist(df['total_outlier_score'], bins=10, edgecolor='black', alpha=0.7)
# plt.xlabel('Total Outlier Score')
# plt.ylabel('Number of Cases')
# plt.title('Distribution of Outlier Scores')

# # Plot 2: Top parameters causing outliers
# plt.subplot(2, 3, 2)
# outlier_param_counts = numerical_outliers.sum().sort_values(ascending=False)
# if len(outlier_param_counts) > 0:
#     top_params = outlier_param_counts.head(8)
#     plt.barh(range(len(top_params)), top_params.values)
#     plt.yticks(range(len(top_params)), [param.replace('_outlier', '').replace('_', ' ') for param in top_params.index])
#     plt.xlabel('Number of Outliers')
#     plt.title('Parameters with Most Outliers')

# # Plot 3-6: Key parameter distributions with outliers highlighted
# key_numerical_params = [col for col in ['SliceThickness_0018_0050', 'KVP_0018_0060', 'ReconstructionDiameter_0018_1100', 'GeneratorPower_0018_1170'] if col in numerical_features.columns]

# for i, param in enumerate(key_numerical_params[:4]):
#     plt.subplot(2, 3, i+3)
    
#     # Plot normal values
#     normal_mask = ~numerical_outliers.get(f'{param}_outlier', pd.Series(False, index=df.index))
#     outlier_mask = numerical_outliers.get(f'{param}_outlier', pd.Series(False, index=df.index))
    
#     normal_values = numerical_features[normal_mask][param].dropna()
#     outlier_values = numerical_features[outlier_mask][param].dropna()
    
#     if len(normal_values) > 0:
#         plt.hist(normal_values, bins=15, alpha=0.7, label='Normal', color='blue')
#     if len(outlier_values) > 0:
#         plt.hist(outlier_values, bins=5, alpha=0.7, label='Outliers', color='red')
    
#     plt.xlabel(param.replace('_', ' '))
#     plt.ylabel('Frequency')
#     plt.title(f'{param.split("_")[0]} Distribution')
#     plt.legend()

# plt.tight_layout()
# plt.savefig('dicom_outlier_analysis.png', dpi=300, bbox_inches='tight')
# print(f"\n\nVisualization saved as 'dicom_outlier_analysis.png'")

# # Step 11: Generate final recommendations
# print(f"\n\nRECOMMENDATIONS FOR SEGMENTATION QUALITY:")
# print("="*60)

# high_risk_patients = df[df['total_outlier_score'] >= 3]['PatientName'].tolist()
# medium_risk_patients = df[df['total_outlier_score'] == 2]['PatientName'].tolist()

# print(f"HIGH RISK cases (score ≥3): {len(high_risk_patients)} cases")
# if len(high_risk_patients) <= 10:
#     print(f"  Patients: {', '.join(high_risk_patients)}")
# else:
#     print(f"  Patients (first 10): {', '.join(high_risk_patients[:10])}")

# print(f"\nMEDIUM RISK cases (score =2): {len(medium_risk_patients)} cases")
# if len(medium_risk_patients) <= 10:
#     print(f"  Patients: {', '.join(medium_risk_patients)}")

# print(f"\nLOW RISK cases (score ≤1): {len(df[df['total_outlier_score'] <= 1])} cases")

# print(f"\nKEY FINDINGS:")
# print(f"- {len(df[df['multivariate_outlier']])} cases are multivariate outliers")
# print(f"- Most common outlier parameters: {', '.join(outlier_param_counts.head(3).index)}")
# print(f"- {(df['total_outlier_score'] == 0).sum()} cases have no outlier flags")

# print(f"\nSUGGESTED ACTIONS:")
# print("1. Review HIGH RISK cases manually before automated segmentation")
# print("2. Consider separate segmentation models for different scanner types")
# print("3. Implement preprocessing normalization for outlier parameters")
# print("4. Set up automated quality control flags for future scans")
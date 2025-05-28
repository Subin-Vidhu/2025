import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
from scipy import stats
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os
from itertools import combinations

# Global configuration for observers
OBSERVER_CONFIG = {
    'observers': ['AIRA', 'SREENADH', 'ANISH'],  # Add 'ANISH', 'DOCTOR' when data is available
    'column_indices': {
        'AIRA': {'Right': 2, 'Left': 3},
        'SREENADH': {'Right': 5, 'Left': 6},
        'ANISH': {'Right': 7, 'Left': 8},
        'DOCTOR': {'Right': 9, 'Left': 10}
    }
}

# Comparison configuration
COMPARISON_CONFIG = {
    'threshold_percentage': 15,  # Threshold for flagging large differences
    'sides': ['Right', 'Left']  # Kidney sides to analyze
}

def get_available_observers(df):
    """Get list of observers that have any data (either Right or Left measurements)"""
    available_observers = []
    for observer in OBSERVER_CONFIG['observers']:
        # Check if columns exist and have any non-null data
        has_data = False
        for side in COMPARISON_CONFIG['sides']:
            col_name = f"{observer}_{side}"
            if col_name in df.columns and not df[col_name].isna().all():
                has_data = True
                break
        if has_data:
            available_observers.append(observer)
    return available_observers

def get_observer_pairs(df):
    """Generate all possible pairs of observers that have at least one common kidney side"""
    available_observers = get_available_observers(df)
    print(f"\nAvailable observers with data: {available_observers}")
    pairs = []
    for obs1, obs2 in combinations(available_observers, 2):
        # Check if they share at least one common kidney side with valid data
        for side in COMPARISON_CONFIG['sides']:
            col1 = f"{obs1}_{side}"
            col2 = f"{obs2}_{side}"
            if (col1 in df.columns and col2 in df.columns and
                not df[col1].isna().all() and not df[col2].isna().all()):
                pairs.append((obs1, obs2))
                break
    return pairs

def load_and_process_data(file_path):
    """Load and process the CSV file containing observer measurements"""
    try:
        # Read CSV file with no header first to see the structure
        df = pd.read_csv(file_path, header=None)
        print("Raw data shape:", df.shape)
        print("Raw columns:", df.columns.tolist())
        
        # Extract the data rows (skip the header rows)
        data = df.iloc[2:].copy()
        
        # Reset index after slicing
        data = data.reset_index(drop=True)
        
        # Remove any completely empty rows
        data = data.dropna(how='all')
        
        # Remove rows where Case Number is empty/NaN
        data = data[data[0].notna()]
        
        # Create processed dataframe
        processed_df = pd.DataFrame()
        processed_df['CASE NO:'] = data[0]
        processed_df['SLICE NO:'] = data[1]
        
        # Add observer measurements
        for observer, sides in OBSERVER_CONFIG['column_indices'].items():
            for side, col_idx in sides.items():
                try:
                    if col_idx < len(data.columns):  # Check if column exists
                        processed_df[f"{observer}_{side}"] = pd.to_numeric(data[col_idx], errors='coerce')
                    else:
                        print(f"Warning: Column index {col_idx} out of bounds for {observer} {side}")
                except Exception as e:
                    print(f"Warning: Error processing column {col_idx} for {observer} {side}: {str(e)}")
                    continue
        
        print(f"\nSuccessfully loaded {file_path}")
        print(f"Shape: {processed_df.shape}")
        print(f"Available columns: {processed_df.columns.tolist()}")
        
        return processed_df
        
    except Exception as e:
        print(f"Error reading file {file_path}: {str(e)}")
        raise

def create_detailed_comparison_csv(df, output_folder):
    """Create detailed CSVs with case-by-case measurements and differences between observers"""
    
    # Create case-by-case comparison DataFrame
    detailed_df = pd.DataFrame()
    
    # Add case and slice information
    detailed_df['Case_Number'] = df['CASE NO:']
    detailed_df['Slice_Number'] = df['SLICE NO:']
    
    # Process each observer pair
    observer_pairs = get_observer_pairs(df)
    if not observer_pairs:
        print("No valid observer pairs found with complete data.")
        return detailed_df
    
    for obs1, obs2 in observer_pairs:
        print(f"\nProcessing comparison between {obs1} and {obs2}")
        # Add measurements for each kidney (round to 2 decimal places)
        for side in COMPARISON_CONFIG['sides']:
            # Skip if either observer has no data for this side
            if df[f"{obs1}_{side}"].isna().all() or df[f"{obs2}_{side}"].isna().all():
                print(f"Skipping {side} kidney comparison for {obs1} vs {obs2} - insufficient data")
                continue
                
            detailed_df[f'{obs1}_{side}'] = df[f'{obs1}_{side}'].round(2)
            detailed_df[f'{obs2}_{side}'] = df[f'{obs2}_{side}'].round(2)
            
            # Absolute differences (round to 2 decimal places)
            detailed_df[f'{side}_Kidney_Difference_{obs1}_vs_{obs2}'] = (
                df[f'{obs1}_{side}'] - df[f'{obs2}_{side}']
            ).round(2)
            
            # Percentage differences (round to 2 decimal places)
            detailed_df[f'{side}_Kidney_Percent_Diff_{obs1}_vs_{obs2}'] = (
                ((df[f'{obs1}_{side}'] - df[f'{obs2}_{side}']) / df[f'{obs1}_{side}'] * 100)
            ).round(2)
            
            # Mean volumes (round to 2 decimal places)
            detailed_df[f'{side}_Kidney_Mean_{obs1}_vs_{obs2}'] = (
                (df[f'{obs1}_{side}'] + df[f'{obs2}_{side}']) / 2
            ).round(2)
        
        # Only calculate totals if both Right and Left measurements exist
        if not (df[f"{obs1}_Right"].isna().all() or df[f"{obs1}_Left"].isna().all()):
            detailed_df[f'{obs1}_Total'] = (
                df[f'{obs1}_Right'] + df[f'{obs1}_Left']
            ).round(2)
        
        if not (df[f"{obs2}_Right"].isna().all() or df[f"{obs2}_Left"].isna().all()):
            detailed_df[f'{obs2}_Total'] = (
                df[f'{obs2}_Right'] + df[f'{obs2}_Left']
            ).round(2)
        
        # Only calculate total differences if both observers have total volumes
        if f'{obs1}_Total' in detailed_df.columns and f'{obs2}_Total' in detailed_df.columns:
            detailed_df[f'Total_Volume_Difference_{obs1}_vs_{obs2}'] = (
                detailed_df[f'{obs1}_Total'] - detailed_df[f'{obs2}_Total']
            ).round(2)
            detailed_df[f'Total_Volume_Percent_Diff_{obs1}_vs_{obs2}'] = (
                (detailed_df[f'Total_Volume_Difference_{obs1}_vs_{obs2}'] / detailed_df[f'{obs1}_Total'] * 100)
            ).round(2)
        
        # Add threshold exceeded flags
        threshold = COMPARISON_CONFIG['threshold_percentage']
        for side in COMPARISON_CONFIG['sides']:
            if f'{side}_Kidney_Percent_Diff_{obs1}_vs_{obs2}' in detailed_df.columns:
                detailed_df[f'{side}_Exceeds_Threshold_{obs1}_vs_{obs2}'] = (
                    abs(detailed_df[f'{side}_Kidney_Percent_Diff_{obs1}_vs_{obs2}']) > threshold
                )
    
    if not detailed_df.empty:
        # Save detailed comparison to CSV
        output_file = os.path.join(output_folder, 'observer_detailed_comparison.csv')
        detailed_df.to_csv(output_file, index=False, float_format='%.2f')
        
        # Create and save threshold exceeded cases for each observer pair
        for obs1, obs2 in observer_pairs:
            threshold_columns = [col for col in detailed_df.columns if f'Exceeds_Threshold_{obs1}_vs_{obs2}' in col]
            if threshold_columns:
                threshold_mask = detailed_df[threshold_columns].any(axis=1)
                threshold_cases = detailed_df[threshold_mask].copy()
                
                if not threshold_cases.empty:
                    threshold_file = os.path.join(output_folder, f'observer_threshold_exceeded_cases_{obs1}_vs_{obs2}.csv')
                    threshold_cases.to_csv(threshold_file, index=False, float_format='%.2f')
                    print(f"Found {len(threshold_cases)} cases exceeding {threshold}% difference threshold for {obs1} vs {obs2}")
                    print(f"Saved to: {threshold_file}")
    
    return detailed_df

def create_metrics_report(df, output_folder):
    """Create a detailed metrics report for all observer pairs"""
    
    # Get all observer pairs
    observer_pairs = get_observer_pairs(df)
    if not observer_pairs:
        print("No valid observer pairs found with complete data.")
        return
    
    # Open file for writing metrics
    with open(os.path.join(output_folder, 'observer_metrics_report.txt'), 'w') as f:
        f.write("Observer Comparison Metrics:\n")
        f.write("=" * 50 + "\n\n")
        
        # Process each observer pair
        for obs1, obs2 in observer_pairs:
            f.write(f"Comparison between {obs1} and {obs2}:\n")
            f.write("=" * 50 + "\n\n")
            
            for side in COMPARISON_CONFIG['sides']:
                f.write(f"{side} Kidney Measurements:\n")
                f.write("-" * 30 + "\n")
                
                # Skip if either observer has no data for this side
                if df[f"{obs1}_{side}"].isna().all() or df[f"{obs2}_{side}"].isna().all():
                    f.write(f"No valid data available for comparison - missing measurements\n")
                    continue
                
                # Get valid data for this side (non-null values only)
                valid_data = df[
                    df[f"{obs1}_{side}"].notna() & 
                    df[f"{obs2}_{side}"].notna()
                ].copy()
                
                if len(valid_data) > 0:
                    # Calculate all metrics
                    abs_diff = (valid_data[f"{obs1}_{side}"] - valid_data[f"{obs2}_{side}"]).round(2)
                    percent_diff = ((abs_diff / valid_data[f"{obs1}_{side}"]) * 100).round(2)
                    
                    try:
                        metrics = {
                            'Number of Valid Cases': len(valid_data),
                            'Mean Absolute Error': round(mean_absolute_error(
                                valid_data[f"{obs1}_{side}"], valid_data[f"{obs2}_{side}"]
                            ), 3),
                            'Root Mean Squared Error': round(np.sqrt(mean_squared_error(
                                valid_data[f"{obs1}_{side}"], valid_data[f"{obs2}_{side}"]
                            )), 3),
                            'R-squared Score': round(r2_score(
                                valid_data[f"{obs1}_{side}"], valid_data[f"{obs2}_{side}"]
                            ), 3),
                            'Pearson Correlation': round(stats.pearsonr(
                                valid_data[f"{obs1}_{side}"], valid_data[f"{obs2}_{side}"]
                            )[0], 3),
                            'Spearman Correlation': round(stats.spearmanr(
                                valid_data[f"{obs1}_{side}"], valid_data[f"{obs2}_{side}"]
                            )[0], 3),
                            f'Mean Difference ({obs1} - {obs2})': round(np.mean(abs_diff), 2),
                            'Median Difference': round(np.median(abs_diff), 2),
                            'Mean Percentage Difference': round(np.mean(np.abs(percent_diff)), 2),
                            'Standard Deviation of Differences': round(np.std(abs_diff), 2),
                            f'{obs1} Mean Volume': round(np.mean(valid_data[f"{obs1}_{side}"]), 2),
                            f'{obs2} Mean Volume': round(np.mean(valid_data[f"{obs2}_{side}"]), 2),
                            f'{obs1} Volume Range': f"{np.min(valid_data[f'{obs1}_{side}']):.2f} - {np.max(valid_data[f'{obs1}_{side}']):.2f}",
                            f'{obs2} Volume Range': f"{np.min(valid_data[f'{obs2}_{side}']):.2f} - {np.max(valid_data[f'{obs2}_{side}']):.2f}"
                        }
                        
                        # Write metrics with appropriate formatting
                        for metric, value in metrics.items():
                            if isinstance(value, (int, np.integer)):
                                f.write(f"{metric}: {value}\n")
                            elif isinstance(value, str):
                                f.write(f"{metric}: {value}\n")
                            else:
                                if metric in ['Pearson Correlation', 'Spearman Correlation', 'R-squared Score', 
                                            'Mean Absolute Error', 'Root Mean Squared Error']:
                                    f.write(f"{metric}: {value:.3f}\n")
                                else:
                                    f.write(f"{metric}: {value:.2f}\n")
                        
                        # Add t-test results
                        t_stat, p_value = stats.ttest_rel(
                            valid_data[f"{obs1}_{side}"], 
                            valid_data[f"{obs2}_{side}"]
                        )
                        f.write(f"Paired t-test p-value: {p_value:.3f}\n")
                        f.write(f"t-statistic: {t_stat:.3f}\n")
                        
                        # Add interpretation
                        f.write("\nInterpretation:\n")
                        f.write("-" * 15 + "\n")
                        
                        # Correlation interpretation
                        if abs(metrics['Pearson Correlation']) > 0.9:
                            f.write("- Very strong correlation between observers\n")
                        elif abs(metrics['Pearson Correlation']) > 0.7:
                            f.write("- Strong correlation between observers\n")
                        else:
                            f.write("- Moderate to weak correlation between observers\n")
                        
                        # Agreement interpretation
                        if abs(metrics['Mean Percentage Difference']) < 5:
                            f.write("- Excellent agreement between observers (Mean % diff < 5%)\n")
                        elif abs(metrics['Mean Percentage Difference']) < 10:
                            f.write("- Good agreement between observers (Mean % diff < 10%)\n")
                        else:
                            f.write("- Notable differences between observers (Mean % diff > 10%)\n")
                        
                        # Statistical significance
                        if p_value < 0.05:
                            f.write("- Statistically significant differences between observers (p < 0.05)\n")
                        else:
                            f.write("- No statistically significant differences between observers (p >= 0.05)\n")
                    
                    except Exception as e:
                        f.write(f"Error calculating metrics: {str(e)}\n")
                    
                else:
                    f.write("No valid data available for comparison - all values are null\n")
                
                f.write("\n" + "=" * 50 + "\n\n")

def create_visualizations(df, output_folder):
    """Create visualization plots for all observer pairs"""
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all observer pairs
    observer_pairs = get_observer_pairs(df)
    if not observer_pairs:
        print("No valid observer pairs found with complete data.")
        return
    
    try:
        for obs1, obs2 in observer_pairs:
            for side in COMPARISON_CONFIG['sides']:
                # Skip if either observer has no data for this side
                if df[f"{obs1}_{side}"].isna().all() or df[f"{obs2}_{side}"].isna().all():
                    print(f"Skipping visualization for {side} kidney ({obs1} vs {obs2}) - insufficient data")
                    continue
                
                # Get valid data for this pair and side (non-null values only)
                valid_data = df[
                    df[f"{obs1}_{side}"].notna() & 
                    df[f"{obs2}_{side}"].notna()
                ].copy()
                
                if len(valid_data) > 0:
                    try:
                        # 1. Scatter plot comparing observers
                        plt.figure(figsize=(10, 8))
                        sns.regplot(data=valid_data, 
                                  x=f"{obs1}_{side}", 
                                  y=f"{obs2}_{side}",
                                  scatter_kws={'alpha':0.5})
                        
                        plt.title(f'{side} Kidney: {obs1} vs {obs2}', fontsize=12)
                        plt.xlabel(f'{obs1} Volume (ml)', fontsize=10)
                        plt.ylabel(f'{obs2} Volume (ml)', fontsize=10)
                        plt.xticks(fontsize=10)
                        plt.yticks(fontsize=10)
                        plt.tight_layout()
                        plt.savefig(os.path.join(output_folder, f'scatter_comparison_{side.lower()}_{obs1}_vs_{obs2}.png'),
                                  dpi=300, bbox_inches='tight')
                        plt.close()
                        
                        # 2. Bland-Altman Plot
                        plt.figure(figsize=(10, 8))
                        mean_volumes = (valid_data[f"{obs1}_{side}"] + valid_data[f"{obs2}_{side}"]) / 2
                        diff_volumes = valid_data[f"{obs1}_{side}"] - valid_data[f"{obs2}_{side}"]
                        
                        plt.scatter(mean_volumes, diff_volumes, alpha=0.5)
                        mean_diff = np.mean(diff_volumes)
                        std_diff = np.std(diff_volumes)
                        
                        plt.axhline(y=mean_diff, color='r', linestyle='--',
                                  label=f'Mean diff: {mean_diff:.2f}')
                        plt.axhline(y=mean_diff + 1.96*std_diff, color='g', linestyle='--',
                                  label=f'95% limits: ±{(1.96*std_diff):.2f}')
                        plt.axhline(y=mean_diff - 1.96*std_diff, color='g', linestyle='--')
                        
                        plt.title(f'Bland-Altman Plot: {side} Kidney ({obs1} vs {obs2})', fontsize=12)
                        plt.xlabel(f'Mean of {obs1} and {obs2} (ml)', fontsize=10)
                        plt.ylabel(f'Difference ({obs1} - {obs2}) (ml)', fontsize=10)
                        plt.legend(fontsize=10)
                        plt.xticks(fontsize=10)
                        plt.yticks(fontsize=10)
                        plt.tight_layout()
                        plt.savefig(os.path.join(output_folder, f'bland_altman_{side.lower()}_{obs1}_vs_{obs2}.png'),
                                  dpi=300, bbox_inches='tight')
                        plt.close()
                        
                        # 3. Box plot
                        plt.figure(figsize=(8, 6))
                        data_to_plot = {
                            f'{obs1} {side}\n(n={len(valid_data)})': valid_data[f"{obs1}_{side}"],
                            f'{obs2} {side}\n(n={len(valid_data)})': valid_data[f"{obs2}_{side}"]
                        }
                        plt.boxplot(data_to_plot.values(), labels=data_to_plot.keys())
                        plt.title(f'Distribution of {side} Kidney Volumes ({obs1} vs {obs2})', fontsize=12)
                        plt.ylabel('Volume (ml)', fontsize=10)
                        plt.xticks(rotation=45, ha='right', fontsize=10)
                        plt.yticks(fontsize=10)
                        plt.grid(True, alpha=0.3)
                        plt.tight_layout()
                        plt.savefig(os.path.join(output_folder, f'boxplot_{side.lower()}_{obs1}_vs_{obs2}.png'),
                                  dpi=300, bbox_inches='tight')
                        plt.close()
                        
                        # 4. Case-wise comparison
                        plt.figure(figsize=(15, 6))
                        
                        plt.plot(valid_data['CASE NO:'], valid_data[f"{obs1}_{side}"], 
                               color='#FF0000', linestyle='-', marker='o', markersize=8,
                               label=f'{obs1} {side} (n={len(valid_data)})', linewidth=2)
                        plt.plot(valid_data['CASE NO:'], valid_data[f"{obs2}_{side}"], 
                               color='#0000FF', linestyle='--', marker='s', markersize=8,
                               label=f'{obs2} {side} (n={len(valid_data)})', linewidth=2)
                        
                        plt.title(f'Case-wise Comparison of {side} Kidney Volumes ({obs1} vs {obs2})', 
                                fontsize=12, pad=20)
                        plt.xlabel('Case Number', fontsize=10)
                        plt.ylabel('Volume (ml)', fontsize=10)
                        plt.legend(fontsize=10)
                        plt.grid(True, alpha=0.3)
                        
                        # Set x-axis ticks to show all case numbers
                        case_numbers = sorted(list(valid_data['CASE NO:'].unique()))
                        plt.xticks(case_numbers, case_numbers, rotation=45, ha='right', fontsize=10)
                        plt.yticks(fontsize=10)
                        
                        plt.tight_layout()
                        plt.savefig(os.path.join(output_folder, f'case_comparison_{side.lower()}_{obs1}_vs_{obs2}.png'),
                                  dpi=300, bbox_inches='tight')
                        plt.close()
                    
                    except Exception as e:
                        print(f"Error creating visualization for {side} kidney ({obs1} vs {obs2}): {str(e)}")
                
                else:
                    print(f"No valid data available for {side} kidney ({obs1} vs {obs2})")

    except Exception as e:
        print(f"Error creating visualizations: {str(e)}")
        raise

def create_combined_visualizations(df, output_folder):
    """Create combined visualization plots for all observers"""
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all available observers
    available_observers = get_available_observers(df)
    if not available_observers:
        print("No observers with valid data found.")
        return
    
    try:
        for side in COMPARISON_CONFIG['sides']:
            # Get observers that have data for this side
            side_observers = []
            for obs in available_observers:
                col_name = f"{obs}_{side}"
                if col_name in df.columns and not df[col_name].isna().all():
                    side_observers.append(obs)
            
            if side_observers:
                print(f"\nCreating combined plots for {side} kidney with observers: {side_observers}")
                
                # 1. Combined Case-wise comparison
                plt.figure(figsize=(15, 8))
                
                # Define distinct colors for each observer
                observer_colors = {
                    'AIRA': '#FF0000',      # Bright Red
                    'SREENADH': '#0000FF',  # Bright Blue
                    'ANISH': '#00CC00',     # Bright Green
                    'DOCTOR': '#9933FF'     # Purple
                }
                
                markers = {
                    'AIRA': 'o',        # Circle
                    'SREENADH': 's',    # Square
                    'ANISH': '^',       # Triangle
                    'DOCTOR': 'D'       # Diamond
                }
                
                # Keep track of all case numbers
                all_case_numbers = set()
                
                # Plot data for each observer
                for observer in side_observers:
                    # Get valid data for this observer
                    valid_data = df[df[f"{observer}_{side}"].notna()].copy()
                    if not valid_data.empty:
                        color = observer_colors.get(observer, '#000000')
                        marker = markers.get(observer, 'o')
                        
                        plt.plot(valid_data['CASE NO:'], valid_data[f"{observer}_{side}"],
                                color=color, linestyle='-', marker=marker, markersize=8,
                                label=f'{observer} {side} (n={len(valid_data)})',
                                linewidth=2)
                        all_case_numbers.update(valid_data['CASE NO:'])
                
                plt.title(f'Case-wise Comparison of {side} Kidney Volumes (All Available Data)',
                         fontsize=14, pad=20)
                plt.xlabel('Case Number', fontsize=12)
                plt.ylabel('Volume (ml)', fontsize=12)
                plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
                plt.grid(True, alpha=0.3)
                
                # Set x-axis ticks to show all case numbers
                case_numbers = sorted(list(all_case_numbers))
                plt.xticks(case_numbers, case_numbers, rotation=45, ha='right', fontsize=10)
                plt.yticks(fontsize=10)
                
                plt.tight_layout()
                plt.savefig(os.path.join(output_folder, f'combined_case_comparison_{side.lower()}.png'),
                          bbox_inches='tight', dpi=300)
                plt.close()
                
                # 2. Combined Box plot
                plt.figure(figsize=(10, 6))
                data_to_plot = {
                    f'{obs} {side}\n(n={len(df[df[f"{obs}_{side}"].notna()])})': 
                    df[f"{obs}_{side}"].dropna()
                    for obs in side_observers
                }
                plt.boxplot(data_to_plot.values(), labels=data_to_plot.keys())
                plt.title(f'Distribution of {side} Kidney Volumes (All Available Data)',
                         fontsize=12, pad=20)
                plt.ylabel('Volume (ml)', fontsize=10)
                plt.xticks(rotation=45, ha='right', fontsize=10)
                plt.yticks(fontsize=10)
                plt.grid(True, alpha=0.3)
                plt.tight_layout()
                plt.savefig(os.path.join(output_folder, f'combined_boxplot_{side.lower()}.png'),
                          bbox_inches='tight', dpi=300)
                plt.close()
            else:
                print(f"No observers have valid data for {side} kidney")

    except Exception as e:
        print(f"Error creating combined visualizations: {str(e)}")
        raise

def create_combined_kidney_plot(df, output_folder):
    """Create a combined plot showing all kidney volumes (Left and Right) from all observers"""
    os.makedirs(output_folder, exist_ok=True)
    
    # Get all available observers
    available_observers = get_available_observers(df)
    if not available_observers:
        print("No observers with valid data found.")
        return
    
    try:
        plt.figure(figsize=(15, 8))
        
        # Define distinct colors for each observer
        observer_colors = {
            'AIRA': '#FF0000',      # Bright Red
            'SREENADH': '#0000FF',  # Bright Blue
            'ANISH': '#00CC00',     # Bright Green
            'DOCTOR': '#9933FF'     # Purple
        }
        
        markers = {
            'AIRA': 'o',        # Circle
            'SREENADH': 's',    # Square
            'ANISH': '^',       # Triangle
            'DOCTOR': 'D'       # Diamond
        }
        
        # Keep track of all x values for axis labels
        all_case_numbers = set()
        
        # Plot data for each observer
        for observer in available_observers:
            color = observer_colors.get(observer, '#000000')  # Default to black if observer not in dict
            marker = markers.get(observer, 'o')               # Default to circle if observer not in dict
            
            # Plot Right kidney data
            if f"{observer}_Right" in df.columns:
                valid_data = df[df[f"{observer}_Right"].notna()].copy()
                if not valid_data.empty:
                    plt.plot(valid_data['CASE NO:'], valid_data[f"{observer}_Right"],
                            color=color, linestyle='-', marker=marker, markersize=8,
                            label=f'{observer} Right (n={len(valid_data)})',
                            linewidth=2)
                    all_case_numbers.update(valid_data['CASE NO:'])
            
            # Plot Left kidney data
            if f"{observer}_Left" in df.columns:
                valid_data = df[df[f"{observer}_Left"].notna()].copy()
                if not valid_data.empty:
                    plt.plot(valid_data['CASE NO:'], valid_data[f"{observer}_Left"],
                            color=color, linestyle='--', marker=marker, markersize=8,
                            label=f'{observer} Left (n={len(valid_data)})',
                            linewidth=2)
                    all_case_numbers.update(valid_data['CASE NO:'])
        
        plt.title('Combined Kidney Volume Measurements (All Observers)', fontsize=14, pad=20)
        plt.xlabel('Case Number', fontsize=12)
        plt.ylabel('Volume (ml)', fontsize=12)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
        plt.grid(True, alpha=0.3)
        
        # Set x-axis ticks to show all case numbers
        case_numbers = sorted(list(all_case_numbers))
        plt.xticks(case_numbers, case_numbers, rotation=45, ha='right')
        
        # Increase font size of tick labels
        plt.xticks(fontsize=10)
        plt.yticks(fontsize=10)
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, 'combined_all_kidneys.png'),
                   bbox_inches='tight', dpi=300)
        plt.close()

    except Exception as e:
        print(f"Error creating combined kidney plot: {str(e)}")
        raise

def main():
    try:
        # File path and output folder
        file_path = r"D:/__SHARED__/Chippy/___FDA___/ARAMIS BATCH 1 - FDA_2.5mm_final.csv"
        output_folder = "observer_analysis_results"
        os.makedirs(output_folder, exist_ok=True)
        
        print(f"Loading data from: {file_path}")
        # Load and process data
        df = load_and_process_data(file_path)
        
        print("\nData loaded successfully. Shape:", df.shape)
        print("\nColumns in the data:", df.columns.tolist())
        
        # Create detailed comparison CSV
        print("\nCreating detailed comparison CSV...")
        comparison_df = create_detailed_comparison_csv(df, output_folder)
        
        # Create metrics report
        print("\nGenerating metrics report...")
        create_metrics_report(df, output_folder)
        
        # Create individual pair visualizations
        print("\nCreating pair-wise visualizations...")
        create_visualizations(df, output_folder)
        
        # Create combined visualizations
        print("\nCreating combined visualizations...")
        create_combined_visualizations(df, output_folder)
        
        # Create combined kidney plot
        print("\nCreating combined kidney plot...")
        create_combined_kidney_plot(df, output_folder)
        
        print(f"\nAnalysis complete! Results saved in: {output_folder}")
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main() 
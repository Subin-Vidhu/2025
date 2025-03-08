import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
from scipy import stats
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os

def load_and_process_data(file_path):
    """Load and process the CSV file containing observer measurements"""
    try:
        # Read CSV file with no header first to see the structure
        df = pd.read_csv(file_path, header=None)
        
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
        
        # Column indices for each observer's measurements
        observer_columns = {
            'AIRA': {'Right': 2, 'Left': 3},
            'SREENADH': {'Right': 5, 'Left': 6},
            'ANISH': {'Right': 8, 'Left': 9},
            'DOCTOR': {'Right': 11, 'Left': 12}
        }
        
        # Add observer measurements
        for observer, sides in observer_columns.items():
            for side, col_idx in sides.items():
                try:
                    processed_df[f"{observer}_{side}"] = pd.to_numeric(data[col_idx], errors='coerce')
                except KeyError as e:
                    print(f"Warning: Could not find column {col_idx} for {observer} {side}")
                    continue
        
        print(f"Successfully loaded {file_path}")
        print(f"Shape: {processed_df.shape}")
        
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
    
    # Add measurements for each kidney (round to 2 decimal places)
    detailed_df['AIRA_Right'] = df['AIRA_Right'].round(2)
    detailed_df['SREENADH_Right'] = df['SREENADH_Right'].round(2)
    detailed_df['AIRA_Left'] = df['AIRA_Left'].round(2)
    detailed_df['SREENADH_Left'] = df['SREENADH_Left'].round(2)
    
    # Calculate differences and percentage differences
    for side in ['Right', 'Left']:
        # Absolute differences (round to 2 decimal places)
        detailed_df[f'{side}_Kidney_Difference'] = (
            df[f'AIRA_{side}'] - df[f'SREENADH_{side}']
        ).round(2)
        
        # Percentage differences (round to 2 decimal places)
        detailed_df[f'{side}_Kidney_Percent_Diff'] = (
            ((df[f'AIRA_{side}'] - df[f'SREENADH_{side}']) / df[f'AIRA_{side}'] * 100)
        ).round(2)
        
        # Mean volumes (round to 2 decimal places)
        detailed_df[f'{side}_Kidney_Mean'] = (
            (df[f'AIRA_{side}'] + df[f'SREENADH_{side}']) / 2
        ).round(2)
    
    # Calculate total volumes for each observer (round to 2 decimal places)
    detailed_df['AIRA_Total'] = (df['AIRA_Right'] + df['AIRA_Left']).round(2)
    detailed_df['SREENADH_Total'] = (df['SREENADH_Right'] + df['SREENADH_Left']).round(2)
    
    # Calculate total volume differences (round to 2 decimal places)
    detailed_df['Total_Volume_Difference'] = (
        detailed_df['AIRA_Total'] - detailed_df['SREENADH_Total']
    ).round(2)
    detailed_df['Total_Volume_Percent_Diff'] = (
        (detailed_df['Total_Volume_Difference'] / detailed_df['AIRA_Total'] * 100)
    ).round(2)
    
    # Add threshold exceeded flags (15% difference threshold)
    detailed_df['Right_Exceeds_Threshold'] = abs(detailed_df['Right_Kidney_Percent_Diff']) > 15
    detailed_df['Left_Exceeds_Threshold'] = abs(detailed_df['Left_Kidney_Percent_Diff']) > 15
    
    # Save detailed comparison to CSV
    output_file = os.path.join(output_folder, 'observer_detailed_comparison.csv')
    detailed_df.to_csv(output_file, index=False, float_format='%.2f')
    
    # Create and save threshold exceeded cases
    threshold_cases = detailed_df[
        (detailed_df['Right_Exceeds_Threshold']) | 
        (detailed_df['Left_Exceeds_Threshold'])
    ].copy()
    
    if not threshold_cases.empty:
        threshold_file = os.path.join(output_folder, 'observer_threshold_exceeded_cases.csv')
        threshold_cases.to_csv(threshold_file, index=False, float_format='%.2f')
        print(f"\nFound {len(threshold_cases)} cases exceeding 15% difference threshold")
        print(f"Saved to: {threshold_file}")
    
    # Create summary metrics DataFrame
    summary_metrics = []
    for side in ['Right', 'Left']:
        valid_data = df[df[f'AIRA_{side}'].notna() & df[f'SREENADH_{side}'].notna()]
        if len(valid_data) > 0:
            metrics = {
                'Kidney_Side': side,
                'Number_of_Cases': len(valid_data),
                'Mean_Absolute_Error': round(mean_absolute_error(
                    valid_data[f'AIRA_{side}'], 
                    valid_data[f'SREENADH_{side}']
                ), 3),
                'Root_Mean_Squared_Error': round(np.sqrt(mean_squared_error(
                    valid_data[f'AIRA_{side}'], 
                    valid_data[f'SREENADH_{side}']
                )), 3),
                'R_squared': round(r2_score(
                    valid_data[f'AIRA_{side}'], 
                    valid_data[f'SREENADH_{side}']
                ), 3),
                'Pearson_Correlation': round(stats.pearsonr(
                    valid_data[f'AIRA_{side}'], 
                    valid_data[f'SREENADH_{side}']
                )[0], 3),
                'Cases_Exceeding_Threshold': sum(abs(detailed_df[f'{side}_Kidney_Percent_Diff']) > 15)
            }
            summary_metrics.append(metrics)
    
    # Save summary metrics
    summary_df = pd.DataFrame(summary_metrics)
    summary_file = os.path.join(output_folder, 'observer_comparison_summary.csv')
    summary_df.to_csv(summary_file, index=False, float_format='%.3f')
    
    return detailed_df

def create_metrics_report(df, output_folder):
    """Create a detailed metrics report similar to the kidney analysis report"""
    
    observers = ['AIRA', 'SREENADH']  # Add 'ANISH', 'DOCTOR' later if data available
    sides = ['Right', 'Left']
    
    # Open file for writing metrics
    with open(os.path.join(output_folder, 'observer_metrics_report.txt'), 'w') as f:
        f.write("Observer Comparison Metrics:\n")
        f.write("=" * 50 + "\n\n")
        
        for side in sides:
            f.write(f"{side} Kidney Measurements:\n")
            f.write("-" * 30 + "\n")
            
            # Get valid data for this side
            valid_data = df[df[f"AIRA_{side}"].notna() & df[f"SREENADH_{side}"].notna()]
            
            if len(valid_data) > 0:
                # Calculate all metrics
                abs_diff = (valid_data[f"AIRA_{side}"] - valid_data[f"SREENADH_{side}"]).round(2)
                percent_diff = ((abs_diff / valid_data[f"AIRA_{side}"]) * 100).round(2)
                
                metrics = {
                    'Number of Valid Cases': len(valid_data),
                    'Mean Absolute Error': round(mean_absolute_error(
                        valid_data[f"AIRA_{side}"], valid_data[f"SREENADH_{side}"]
                    ), 3),
                    'Root Mean Squared Error': round(np.sqrt(mean_squared_error(
                        valid_data[f"AIRA_{side}"], valid_data[f"SREENADH_{side}"]
                    )), 3),
                    'R-squared Score': round(r2_score(
                        valid_data[f"AIRA_{side}"], valid_data[f"SREENADH_{side}"]
                    ), 3),
                    'Pearson Correlation': round(stats.pearsonr(
                        valid_data[f"AIRA_{side}"], valid_data[f"SREENADH_{side}"]
                    )[0], 3),
                    'Spearman Correlation': round(stats.spearmanr(
                        valid_data[f"AIRA_{side}"], valid_data[f"SREENADH_{side}"]
                    )[0], 3),
                    'Mean Difference (AIRA - SREENADH)': round(np.mean(abs_diff), 2),
                    'Median Difference': round(np.median(abs_diff), 2),
                    'Mean Percentage Difference': round(np.mean(np.abs(percent_diff)), 2),
                    'Standard Deviation of Differences': round(np.std(abs_diff), 2),
                    'AIRA Mean Volume': round(np.mean(valid_data[f"AIRA_{side}"]), 2),
                    'SREENADH Mean Volume': round(np.mean(valid_data[f"SREENADH_{side}"]), 2),
                    'AIRA Volume Range': f"{np.min(valid_data[f'AIRA_{side}']):.2f} - {np.max(valid_data[f'AIRA_{side}']):.2f}",
                    'SREENADH Volume Range': f"{np.min(valid_data[f'SREENADH_{side}']):.2f} - {np.max(valid_data[f'SREENADH_{side}']):.2f}"
                }
                
                # Write metrics
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
                t_stat, p_value = stats.ttest_rel(valid_data[f"AIRA_{side}"], valid_data[f"SREENADH_{side}"])
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
                
            else:
                f.write("No valid data available for comparison\n")
            
            f.write("\n" + "=" * 50 + "\n\n")

def create_visualizations(df, output_folder):
    """Create visualization plots for observer comparisons"""
    os.makedirs(output_folder, exist_ok=True)
    
    observers = ['AIRA', 'SREENADH']  # Add 'ANISH', 'DOCTOR' later if data available
    sides = ['Right', 'Left']
    
    try:
        for side in sides:
            # 1. Scatter plot comparing observers
            plt.figure(figsize=(10, 8))
            valid_data = df[df[f"AIRA_{side}"].notna() & df[f"SREENADH_{side}"].notna()]
            
            sns.regplot(data=valid_data, 
                       x=f"AIRA_{side}", 
                       y=f"SREENADH_{side}",
                       scatter_kws={'alpha':0.5})
            
            plt.title(f'{side} Kidney: AIRA vs SREENADH')
            plt.xlabel('AIRA Volume (ml)')
            plt.ylabel('SREENADH Volume (ml)')
            plt.tight_layout()
            plt.savefig(os.path.join(output_folder, f'scatter_comparison_{side.lower()}.png'))
            plt.close()
            
            # 2. Bland-Altman Plot
            plt.figure(figsize=(10, 8))
            mean_volumes = (valid_data[f"AIRA_{side}"] + valid_data[f"SREENADH_{side}"]) / 2
            diff_volumes = valid_data[f"AIRA_{side}"] - valid_data[f"SREENADH_{side}"]
            
            plt.scatter(mean_volumes, diff_volumes, alpha=0.5)
            mean_diff = np.mean(diff_volumes)
            std_diff = np.std(diff_volumes)
            
            plt.axhline(y=mean_diff, color='r', linestyle='--',
                       label=f'Mean diff: {mean_diff:.2f}')
            plt.axhline(y=mean_diff + 1.96*std_diff, color='g', linestyle='--',
                       label=f'95% limits: ±{(1.96*std_diff):.2f}')
            plt.axhline(y=mean_diff - 1.96*std_diff, color='g', linestyle='--')
            
            plt.title(f'Bland-Altman Plot: {side} Kidney')
            plt.xlabel('Mean of AIRA and SREENADH (ml)')
            plt.ylabel('Difference (AIRA - SREENADH) (ml)')
            plt.legend()
            plt.tight_layout()
            plt.savefig(os.path.join(output_folder, f'bland_altman_{side.lower()}.png'))
            plt.close()
            
            # 3. Box plot
            plt.figure(figsize=(8, 6))
            data_to_plot = {
                f'AIRA {side}': valid_data[f"AIRA_{side}"],
                f'SREENADH {side}': valid_data[f"SREENADH_{side}"]
            }
            plt.boxplot(data_to_plot.values(), labels=data_to_plot.keys())
            plt.title(f'Distribution of {side} Kidney Volumes')
            plt.ylabel('Volume (ml)')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(output_folder, f'boxplot_{side.lower()}.png'))
            plt.close()
            
            # 4. Case-wise comparison
            plt.figure(figsize=(15, 6))
            x = range(len(valid_data))
            
            plt.plot(x, valid_data[f"AIRA_{side}"], 'b-', label=f'AIRA {side}', marker='o')
            plt.plot(x, valid_data[f"SREENADH_{side}"], 'r--', label=f'SREENADH {side}', marker='s')
            
            plt.title(f'Case-wise Comparison of {side} Kidney Volumes')
            plt.xlabel('Case Number')
            plt.ylabel('Volume (ml)')
            plt.legend()
            plt.grid(True)
            plt.xticks(x, valid_data['CASE NO:'], rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(output_folder, f'case_comparison_{side.lower()}.png'))
            plt.close()

    except Exception as e:
        print(f"Error creating visualizations: {str(e)}")
        raise

def main():
    try:
        # File path and output folder
        file_path = r"D:/__SHARED__/Chippy/___FDA___/ARAMIS BATCH 1 - FDA_2.5mm.csv"
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
        
        # Create visualizations
        print("\nCreating visualizations...")
        create_visualizations(df, output_folder)
        
        print(f"\nAnalysis complete! Results saved in: {output_folder}")
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main() 
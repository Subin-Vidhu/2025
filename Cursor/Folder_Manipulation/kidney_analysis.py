import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import numpy as np
from scipy import stats
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import os

# Set style for better visualizations
plt.style.use('default')
sns.set_theme()

def load_and_process_data(folder_path):
    # Get the two CSV files
    csv_files = list(Path(folder_path).glob('*.csv'))
    
    if len(csv_files) != 2:
        raise ValueError(f"Expected 2 CSV files, found {len(csv_files)}")
    
    dataframes = {}
    for file in csv_files:
        try:
            # Read CSV file with no header first to see the structure
            df = pd.read_csv(file, header=None)
            
            # Find the actual data rows (skip the header rows)
            data = df.iloc[2:].copy()
            
            # Extract only the columns we need (first 5 columns contain the data we want)
            data = data.iloc[:, :5]
            
            # Set the column names
            data.columns = ['CASE NO:', 'SLICE NO:', 'Right', 'Left', 'Time(s)']
            
            # Convert volume and time columns to numeric
            data['Right'] = pd.to_numeric(data['Right'], errors='coerce')
            data['Left'] = pd.to_numeric(data['Left'], errors='coerce')
            data['Time(s)'] = pd.to_numeric(data['Time(s)'], errors='coerce')
            
            # Create processed dataframe with only the columns we need
            processed_df = pd.DataFrame({
                'CASE NO:': data['CASE NO:'],
                'SLICE NO:': data['SLICE NO:'],
                'Right': data['Right'],
                'Left': data['Left'],
                'Time': data['Time(s)']
            })
            
            # Store with file identifier (2.5mm or 5.0mm)
            if '2.5mm' in str(file):
                dataframes['2.5mm'] = processed_df
            else:
                dataframes['5.0mm'] = processed_df
            
            print(f"Successfully loaded {file.name}")
            print(f"Shape: {processed_df.shape}")
            
        except Exception as e:
            print(f"Error reading file {file}: {str(e)}")
    
    if len(dataframes) != 2:
        raise ValueError("Could not load both CSV files properly")
    
    # Merge the two dataframes on CASE NO:
    print("\nMerging dataframes...")
    merged_df = pd.merge(dataframes['2.5mm'], dataframes['5.0mm'], 
                        on='CASE NO:', suffixes=('_2.5mm', '_5.0mm'))
    
    print(f"Merged shape: {merged_df.shape}")
    
    # Remove any rows with missing values
    merged_df = merged_df.dropna(subset=[
        'Right_2.5mm', 'Left_2.5mm', 'Right_5.0mm', 'Left_5.0mm'
    ])
    
    print(f"Final shape after removing missing values: {merged_df.shape}")
    
    return merged_df

def create_detailed_comparison_csv(df, output_folder):
    """Create a detailed CSV with all measurements and differences"""
    
    # Calculate differences and percentage differences
    detailed_df = pd.DataFrame({
        'Case_Number': df['CASE NO:'],
        'Slice_Number_2.5mm': df['SLICE NO:_2.5mm'],
        'Slice_Number_5.0mm': df['SLICE NO:_5.0mm'],
        
        # Original measurements
        'Right_Kidney_2.5mm': df['Right_2.5mm'],
        'Right_Kidney_5.0mm': df['Right_5.0mm'],
        'Left_Kidney_2.5mm': df['Left_2.5mm'],
        'Left_Kidney_5.0mm': df['Left_5.0mm'],
        
        # Absolute differences
        'Right_Kidney_Difference': df['Right_2.5mm'] - df['Right_5.0mm'],
        'Left_Kidney_Difference': df['Left_2.5mm'] - df['Left_5.0mm'],
        
        # Percentage differences
        'Right_Kidney_Percent_Diff': ((df['Right_2.5mm'] - df['Right_5.0mm']) / df['Right_2.5mm']) * 100,
        'Left_Kidney_Percent_Diff': ((df['Left_2.5mm'] - df['Left_5.0mm']) / df['Left_2.5mm']) * 100,
        
        # Mean volumes
        'Right_Kidney_Mean': (df['Right_2.5mm'] + df['Right_5.0mm']) / 2,
        'Left_Kidney_Mean': (df['Left_2.5mm'] + df['Left_5.0mm']) / 2,
        
        # Processing times
        'Processing_Time_2.5mm': df['Time_2.5mm'],
        'Processing_Time_5.0mm': df['Time_5.0mm'],
        'Processing_Time_Difference': df['Time_2.5mm'] - df['Time_5.0mm']
    })
    
    # Add summary statistics for each case
    detailed_df['Total_Volume_2.5mm'] = detailed_df['Right_Kidney_2.5mm'] + detailed_df['Left_Kidney_2.5mm']
    detailed_df['Total_Volume_5.0mm'] = detailed_df['Right_Kidney_5.0mm'] + detailed_df['Left_Kidney_5.0mm']
    detailed_df['Total_Volume_Difference'] = detailed_df['Total_Volume_2.5mm'] - detailed_df['Total_Volume_5.0mm']
    detailed_df['Total_Volume_Percent_Diff'] = (detailed_df['Total_Volume_Difference'] / detailed_df['Total_Volume_2.5mm']) * 100
    
    # Calculate if differences exceed thresholds
    detailed_df['Right_Exceeds_Threshold'] = abs(detailed_df['Right_Kidney_Percent_Diff']) > 15
    detailed_df['Left_Exceeds_Threshold'] = abs(detailed_df['Left_Kidney_Percent_Diff']) > 15
    
    # Sort by case number
    detailed_df = detailed_df.sort_values('Case_Number')
    
    # Save to CSV
    output_file = os.path.join(output_folder, 'detailed_comparison.csv')
    detailed_df.to_csv(output_file, index=False)
    
    # Create a summary of cases exceeding thresholds
    threshold_cases = detailed_df[
        (detailed_df['Right_Exceeds_Threshold']) | 
        (detailed_df['Left_Exceeds_Threshold'])
    ]
    
    if not threshold_cases.empty:
        threshold_file = os.path.join(output_folder, 'threshold_exceeded_cases.csv')
        threshold_cases.to_csv(threshold_file, index=False)
        print(f"\nFound {len(threshold_cases)} cases exceeding 15% difference threshold")
        print(f"Saved to: {threshold_file}")
    
    return detailed_df

def calculate_metrics(df):
    metrics = {}
    
    # Compare 2.5mm vs 5.0mm for Right kidney
    metrics['Right Kidney'] = {
        'Mean Absolute Error': mean_absolute_error(df['Right_2.5mm'], df['Right_5.0mm']),
        'Mean Squared Error': mean_squared_error(df['Right_2.5mm'], df['Right_5.0mm']),
        'Root Mean Squared Error': np.sqrt(mean_squared_error(df['Right_2.5mm'], df['Right_5.0mm'])),
        'R-squared Score': r2_score(df['Right_2.5mm'], df['Right_5.0mm']),
        'Pearson Correlation': stats.pearsonr(df['Right_2.5mm'], df['Right_5.0mm'])[0],
        'Spearman Correlation': stats.spearmanr(df['Right_2.5mm'], df['Right_5.0mm'])[0],
        'Mean Percentage Error': np.mean(np.abs((df['Right_2.5mm'] - df['Right_5.0mm']) / df['Right_2.5mm'])) * 100,
        'Mean Volume Difference': np.mean(df['Right_2.5mm'] - df['Right_5.0mm']),
        'Median Volume Difference': np.median(df['Right_2.5mm'] - df['Right_5.0mm'])
    }
    
    # Compare 2.5mm vs 5.0mm for Left kidney
    metrics['Left Kidney'] = {
        'Mean Absolute Error': mean_absolute_error(df['Left_2.5mm'], df['Left_5.0mm']),
        'Mean Squared Error': mean_squared_error(df['Left_2.5mm'], df['Left_5.0mm']),
        'Root Mean Squared Error': np.sqrt(mean_squared_error(df['Left_2.5mm'], df['Left_5.0mm'])),
        'R-squared Score': r2_score(df['Left_2.5mm'], df['Left_5.0mm']),
        'Pearson Correlation': stats.pearsonr(df['Left_2.5mm'], df['Left_5.0mm'])[0],
        'Spearman Correlation': stats.spearmanr(df['Left_2.5mm'], df['Left_5.0mm'])[0],
        'Mean Percentage Error': np.mean(np.abs((df['Left_2.5mm'] - df['Left_5.0mm']) / df['Left_2.5mm'])) * 100,
        'Mean Volume Difference': np.mean(df['Left_2.5mm'] - df['Left_5.0mm']),
        'Median Volume Difference': np.median(df['Left_2.5mm'] - df['Left_5.0mm'])
    }
    
    return metrics

def create_visualizations(df, output_folder):
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        # 1. Scatter plots comparing 2.5mm vs 5.0mm
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Right kidney comparison
        sns.regplot(data=df, x='Right_2.5mm', y='Right_5.0mm', ax=ax1)
        ax1.set_title('Right Kidney: 2.5mm vs 5.0mm')
        ax1.set_xlabel('Volume at 2.5mm (ml)')
        ax1.set_ylabel('Volume at 5.0mm (ml)')
        
        # Left kidney comparison
        sns.regplot(data=df, x='Left_2.5mm', y='Left_5.0mm', ax=ax2)
        ax2.set_title('Left Kidney: 2.5mm vs 5.0mm')
        ax2.set_xlabel('Volume at 2.5mm (ml)')
        ax2.set_ylabel('Volume at 5.0mm (ml)')
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, 'scatter_comparison.png'))
        plt.close()

        # 2. Bland-Altman Plots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # Right kidney
        mean_volumes_right = (df['Right_2.5mm'] + df['Right_5.0mm']) / 2
        diff_volumes_right = df['Right_2.5mm'] - df['Right_5.0mm']
        
        ax1.scatter(mean_volumes_right, diff_volumes_right, alpha=0.5)
        mean_diff_right = np.mean(diff_volumes_right)
        std_diff_right = np.std(diff_volumes_right)
        ax1.axhline(y=mean_diff_right, color='r', linestyle='--', 
                   label=f'Mean diff: {mean_diff_right:.2f}')
        ax1.axhline(y=mean_diff_right + 1.96*std_diff_right, color='g', linestyle='--',
                   label=f'95% limits: ±{(1.96*std_diff_right):.2f}')
        ax1.axhline(y=mean_diff_right - 1.96*std_diff_right, color='g', linestyle='--')
        ax1.set_title('Bland-Altman Plot: Right Kidney')
        ax1.set_xlabel('Mean of 2.5mm and 5.0mm (ml)')
        ax1.set_ylabel('Difference (2.5mm - 5.0mm) (ml)')
        ax1.legend()
        
        # Left kidney
        mean_volumes_left = (df['Left_2.5mm'] + df['Left_5.0mm']) / 2
        diff_volumes_left = df['Left_2.5mm'] - df['Left_5.0mm']
        
        ax2.scatter(mean_volumes_left, diff_volumes_left, alpha=0.5)
        mean_diff_left = np.mean(diff_volumes_left)
        std_diff_left = np.std(diff_volumes_left)
        ax2.axhline(y=mean_diff_left, color='r', linestyle='--',
                   label=f'Mean diff: {mean_diff_left:.2f}')
        ax2.axhline(y=mean_diff_left + 1.96*std_diff_left, color='g', linestyle='--',
                   label=f'95% limits: ±{(1.96*std_diff_left):.2f}')
        ax2.axhline(y=mean_diff_left - 1.96*std_diff_left, color='g', linestyle='--')
        ax2.set_title('Bland-Altman Plot: Left Kidney')
        ax2.set_xlabel('Mean of 2.5mm and 5.0mm (ml)')
        ax2.set_ylabel('Difference (2.5mm - 5.0mm) (ml)')
        ax2.legend()
        
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, 'bland_altman_comparison.png'))
        plt.close()

        # 3. Box plots
        plt.figure(figsize=(12, 6))
        data_to_plot = {
            'Right 2.5mm': df['Right_2.5mm'],
            'Right 5.0mm': df['Right_5.0mm'],
            'Left 2.5mm': df['Left_2.5mm'],
            'Left 5.0mm': df['Left_5.0mm']
        }
        plt.boxplot(data_to_plot.values(), labels=data_to_plot.keys())
        plt.title('Distribution of Kidney Volumes')
        plt.ylabel('Volume (ml)')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, 'boxplot_comparison.png'))
        plt.close()

        # 4. Case-wise comparison
        plt.figure(figsize=(15, 6))
        x = range(len(df))
        
        plt.plot(x, df['Right_2.5mm'], 'b-', label='Right 2.5mm', marker='o')
        plt.plot(x, df['Right_5.0mm'], 'b--', label='Right 5.0mm', marker='s')
        plt.plot(x, df['Left_2.5mm'], 'r-', label='Left 2.5mm', marker='o')
        plt.plot(x, df['Left_5.0mm'], 'r--', label='Left 5.0mm', marker='s')
        
        plt.title('Case-wise Comparison of Kidney Volumes')
        plt.xlabel('Case Number')
        plt.ylabel('Volume (ml)')
        plt.legend()
        plt.grid(True)
        plt.xticks(x, df['CASE NO:'], rotation=45)
        plt.tight_layout()
        plt.savefig(os.path.join(output_folder, 'case_comparison.png'))
        plt.close()

    except Exception as e:
        print(f"Error creating visualizations: {str(e)}")
        raise

def main():
    try:
        # Folder containing the CSV files
        folder_path = r"D:\__SHARED__\Chippy\___FDA___"
        output_folder = "analysis_results"
        
        print(f"Loading data from: {folder_path}")
        # Load and process data
        df = load_and_process_data(folder_path)
        
        print("\nData loaded successfully. Shape:", df.shape)
        print("\nColumns in the data:", df.columns.tolist())
        
        # Create detailed comparison CSV
        print("\nCreating detailed comparison CSV...")
        detailed_df = create_detailed_comparison_csv(df, output_folder)
        
        # Calculate metrics
        metrics = calculate_metrics(df)
        
        # Print metrics
        print("\nAnalysis Metrics:")
        print("-" * 50)
        for kidney, kidney_metrics in metrics.items():
            print(f"\n{kidney}:")
            print("-" * 30)
            for metric, value in kidney_metrics.items():
                print(f"{metric}: {value:.4f}")
        
        # Create visualizations
        print("\nCreating visualizations...")
        create_visualizations(df, output_folder)
        
        # Additional statistical tests
        print("\nStatistical Tests:")
        print("-" * 50)
        
        # Paired t-tests
        t_stat_right, p_value_right = stats.ttest_rel(df['Right_2.5mm'], df['Right_5.0mm'])
        t_stat_left, p_value_left = stats.ttest_rel(df['Left_2.5mm'], df['Left_5.0mm'])
        
        print(f"Right Kidney - Paired t-test p-value: {p_value_right:.4f}")
        print(f"Left Kidney - Paired t-test p-value: {p_value_left:.4f}")
        
        # Save metrics to file
        metrics_file = os.path.join(output_folder, 'metrics_report.txt')
        with open(metrics_file, 'w') as f:
            f.write("Analysis Metrics:\n")
            f.write("-" * 50 + "\n")
            
            for kidney, kidney_metrics in metrics.items():
                f.write(f"\n{kidney}:\n")
                f.write("-" * 30 + "\n")
                for metric, value in kidney_metrics.items():
                    f.write(f"{metric}: {value:.4f}\n")
            
            f.write("\nStatistical Tests:\n")
            f.write("-" * 50 + "\n")
            f.write(f"Right Kidney - Paired t-test p-value: {p_value_right:.4f}\n")
            f.write(f"Left Kidney - Paired t-test p-value: {p_value_left:.4f}\n")
        
        print(f"\nAnalysis complete! Results saved in: {output_folder}")
        
    except Exception as e:
        print(f"\nError during analysis: {str(e)}")
        raise

if __name__ == "__main__":
    main() 
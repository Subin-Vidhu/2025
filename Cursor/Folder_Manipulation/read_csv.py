import pandas as pd

# Read the CSV file and display its structure
file_path = r"D:\__SHARED__\Chippy\___FDA___\ARAMIS BATCH 1 - FDA_2.5mm.csv"
df = pd.read_csv(file_path)
print("Columns:")
print(df.columns.tolist())
print("\nFirst few rows:")
print(df.head()) 
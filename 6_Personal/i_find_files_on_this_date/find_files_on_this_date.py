# -*- coding: utf-8 -*-
"""
Created on Wed May 28 11:21:42 2025

@author: Subin-PC
"""

#!/usr/bin/env python3
"""
Script to find files modified on March 8th (any year) with focus on .csv and .py files
Searches all local drives on Windows system
"""

import os
import sys
import datetime
import argparse
from pathlib import Path
import csv
from collections import defaultdict
import psutil
from colorama import init, Fore, Style

# Initialize colorama for colored output on Windows
init(autoreset=True)

def get_local_drives():
    """Get all local drive letters (excluding network drives)"""
    drives = []
    for partition in psutil.disk_partitions():
        if 'fixed' in partition.opts:  # Local drives only
            drives.append(partition.mountpoint)
    return drives

def format_size(size_bytes):
    """Convert bytes to KB with 2 decimal places"""
    return round(size_bytes / 1024, 2)

def search_files_modified_on_date(target_date):
    """Search for files modified on the target date across all local drives"""
    print(f"{Fore.GREEN}Searching for files modified on {target_date.strftime('%B %d, %Y')}...")
    print("=" * 60)
    
    # Get local drives
    local_drives = get_local_drives()
    print(f"{Fore.YELLOW}Local drives found: {', '.join(local_drives)}")
    print()
    
    # Initialize collections for results
    csv_files = []
    py_files = []
    other_files = []
    
    for drive in local_drives:
        print(f"{Fore.CYAN}Searching drive {drive}...")
        
        try:
            # Walk through all directories in the drive
            for root, dirs, files in os.walk(drive):
                try:
                    for file in files:
                        file_path = os.path.join(root, file)
                        
                        try:
                            # Get file modification time
                            mod_time = datetime.datetime.fromtimestamp(os.path.getmtime(file_path))
                            
                            # Check if modified on target date
                            if mod_time.date() == target_date.date():
                                file_info = {
                                    'name': file,
                                    'full_path': file_path,
                                    'size_kb': format_size(os.path.getsize(file_path)),
                                    'last_modified': mod_time,
                                    'extension': Path(file).suffix.lower()
                                }
                                
                                # Categorize by extension
                                if file_info['extension'] == '.csv':
                                    csv_files.append(file_info)
                                elif file_info['extension'] == '.py':
                                    py_files.append(file_info)
                                else:
                                    other_files.append(file_info)
                                    
                        except (OSError, PermissionError):
                            # Skip files we can't access
                            continue
                            
                except (OSError, PermissionError):
                    # Skip directories we can't access
                    continue
                    
            print(f"{Fore.GREEN}Drive {drive} completed.")
            
        except Exception as e:
            print(f"{Fore.RED}Error accessing drive {drive}: {str(e)}")
    
    return csv_files, py_files, other_files

def print_file_list(files, title, color=Fore.GREEN):
    """Print formatted list of files"""
    if files:
        print(f"\n{color}{title} ({len(files)} found):")
        print("-" * 50)
        
        # Sort files by full path
        files.sort(key=lambda x: x['full_path'])
        
        # Print header
        print(f"{'Name':<30} {'Size(KB)':<10} {'Last Modified':<20} {'Full Path'}")
        print("-" * 100)
        
        # Print file details
        for file_info in files:
            name = file_info['name'][:29] if len(file_info['name']) > 29 else file_info['name']
            size = str(file_info['size_kb'])
            mod_time = file_info['last_modified'].strftime('%Y-%m-%d %H:%M:%S')
            path = file_info['full_path']
            
            print(f"{name:<30} {size:<10} {mod_time:<20} {path}")
    else:
        print(f"\n{Fore.YELLOW}No {title.lower()} found")

def export_to_csv(all_files, year):
    """Export results to CSV file"""
    if not all_files:
        print(f"{Fore.YELLOW}No files to export.")
        return
    
    filename = f"March8_ModifiedFiles_{year}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'extension', 'size_kb', 'last_modified', 'full_path']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for file_info in all_files:
                writer.writerow(file_info)
        
        print(f"{Fore.GREEN}Results exported to: {filename}")
        
    except Exception as e:
        print(f"{Fore.RED}Error exporting to CSV: {str(e)}")

def main():
    parser = argparse.ArgumentParser(description='Find files modified on March 8th')
    parser.add_argument('--year', type=int, default=datetime.datetime.now().year,
                      help='Year to search for (default: current year)')
    
    args = parser.parse_args()
    
    # Create target date (March 8th of specified year)
    target_date = datetime.datetime(args.year, 3, 8)
    
    try:
        # Search for files
        csv_files, py_files, other_files = search_files_modified_on_date(target_date)
        
        # Display results
        print(f"\n{Fore.MAGENTA}RESULTS SUMMARY")
        print("=" * 60)
        
        # Display CSV files
        print_file_list(csv_files, f"CSV FILES MODIFIED ON MARCH 8, {args.year}")
        
        # Display Python files  
        print_file_list(py_files, f"PYTHON FILES MODIFIED ON MARCH 8, {args.year}")
        
        # Display other files
        if other_files:
            print_file_list(other_files, f"OTHER FILES MODIFIED ON MARCH 8, {args.year}")
        
        # Summary statistics
        total_files = len(csv_files) + len(py_files) + len(other_files)
        print(f"\n{Fore.MAGENTA}TOTAL SUMMARY:")
        print(f"CSV files: {len(csv_files)}")
        print(f"Python files: {len(py_files)}")
        print(f"Other files: {len(other_files)}")
        print(f"Total files: {total_files}")
        
        # Option to export results
        if total_files > 0:
            export_choice = input(f"\n{Fore.CYAN}Would you like to export results to a CSV file? (y/n): ")
            if export_choice.lower() in ['y', 'yes']:
                all_files = csv_files + py_files + other_files
                export_to_csv(all_files, args.year)
        
        print(f"\n{Fore.GREEN}Search completed!")
        
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Search interrupted by user.")
    except Exception as e:
        print(f"\n{Fore.RED}An error occurred: {str(e)}")

if __name__ == "__main__":
    # Check if required modules are available
    try:
        import psutil
        import colorama
    except ImportError as e:
        print(f"Missing required module: {e}")
        print("Please install required modules:")
        print("pip install psutil colorama")
        sys.exit(1)
    
    main()
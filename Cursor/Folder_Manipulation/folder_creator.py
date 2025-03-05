import os

def create_aira_folders(base_path):
    # Keep track of created and existing folders
    created_count = 0
    existing_count = 0
    
    # Check if base path exists
    if not os.path.exists(base_path):
        print(f"Error: The path {base_path} does not exist!")
        return
    
    # Get all immediate subdirectories
    try:
        subdirs = [d for d in os.listdir(base_path) if os.path.isdir(os.path.join(base_path, d))]
        
        # Process each subdirectory
        for subdir in subdirs:
            aira_path = os.path.join(base_path, subdir, "AIRA")
            
            # Check if AIRA folder already exists
            if os.path.exists(aira_path):
                print(f"AIRA folder already exists in {subdir}")
                existing_count += 1
            else:
                try:
                    os.makedirs(aira_path)
                    print(f"Created AIRA folder in {subdir}")
                    created_count += 1
                except Exception as e:
                    print(f"Error creating AIRA folder in {subdir}: {str(e)}")
        
        # Print summary
        print("\nSummary:")
        print(f"Total AIRA folders created: {created_count}")
        print(f"AIRA folders already existing: {existing_count}")
        
    except Exception as e:
        print(f"Error accessing the directory: {str(e)}")

if __name__ == "__main__":
    base_path = r"F:\PROJECT B\5_0"
    create_aira_folders(base_path) 
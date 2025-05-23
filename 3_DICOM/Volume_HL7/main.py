import requests
import os
import zipfile
import io
from pydicom import dcmread, dcmwrite
from pydicom.tag import Tag
from pydicom.uid import generate_uid

# Configuration
ORTHANC_URL = "http://localhost:8042"  # Change if hosted elsewhere
AUTH = ('admin', 'password')
KIDNEY_DATA = {
    "Right Kidney": "125 ml",
    "Left Kidney": "132 ml"
}
SAVE_DIR = "study_files"

# Step 1: Get list of studies
def get_study_list():
    response = requests.get(f"{ORTHANC_URL}/studies", auth=AUTH)
    response.raise_for_status()
    return response.json()

# Step 2: Download study
def download_study(study_id):
    response = requests.get(f"{ORTHANC_URL}/studies/{study_id}/archive", auth=AUTH)
    response.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(SAVE_DIR)

# Step 3: Add private tags to DICOM files
def modify_dicom_files():
    modified_count = 0
    for root, _, files in os.walk(SAVE_DIR):
        for file in files:
            if file.endswith(".dcm"):
                path = os.path.join(root, file)
                try:
                    ds = dcmread(path)

                    # Reserve private creator tag (0011,0010)
                    private_creator_tag = Tag(0x0011, 0x0010)
                    private_creator = "KidneyVolInfo"
                    ds.add_new(private_creator_tag, 'LO', private_creator)

                    # Now you can use (0011,1010) and (0011,1011) under that creator
                    ds.add_new(Tag(0x0011, 0x1010), 'LO', f"Right Kidney: {KIDNEY_DATA['Right Kidney']}")
                    ds.add_new(Tag(0x0011, 0x1011), 'LO', f"Left Kidney: {KIDNEY_DATA['Left Kidney']}")

                    # Generate new UIDs to avoid conflicts when sending back
                    ds.SOPInstanceUID = generate_uid()
                    
                    dcmwrite(path, ds)
                    modified_count += 1
                    print(f"Modified: {path}")
                except Exception as e:
                    print(f"Error modifying {path}: {e}")
    
    print(f"Total files modified: {modified_count}")

# Step 4: Send modified files back to PACS (Fixed version)
def send_back_to_pacs():
    uploaded_count = 0
    failed_count = 0
    
    # Walk through all directories to find DICOM files
    for root, _, files in os.walk(SAVE_DIR):
        for file in files:
            if file.endswith(".dcm"):
                path = os.path.join(root, file)
                try:
                    with open(path, 'rb') as f:
                        response = requests.post(f"{ORTHANC_URL}/instances", 
                                               auth=AUTH, 
                                               data=f.read(),
                                               headers={'Content-Type': 'application/dicom'})
                        
                        if response.status_code == 200:
                            uploaded_count += 1
                            print(f"Successfully uploaded: {file}")
                        else:
                            failed_count += 1
                            print(f"Failed to upload {file}: {response.status_code} - {response.text}")
                            
                except Exception as e:
                    failed_count += 1
                    print(f"Error uploading {path}: {e}")
    
    print(f"Upload summary: {uploaded_count} successful, {failed_count} failed")

# Helper function to verify modifications
def verify_modifications():
    print("Verifying modifications...")
    for root, _, files in os.walk(SAVE_DIR):
        for file in files:
            if file.endswith(".dcm"):
                path = os.path.join(root, file)
                try:
                    ds = dcmread(path)
                    right_kidney = ds.get((0x0011, 0x1010))
                    left_kidney = ds.get((0x0011, 0x1011))
                    
                    if right_kidney and left_kidney:
                        print(f"✓ {file}: Right Kidney: {right_kidney.value}, Left Kidney: {left_kidney.value}")
                    else:
                        print(f"✗ {file}: Missing kidney volume tags")
                except Exception as e:
                    print(f"Error reading {path}: {e}")

# Alternative: Send back with series organization
def send_back_to_pacs_organized():
    """
    Alternative method that groups files by series before sending
    """
    series_groups = {}
    
    # Group files by series
    for root, _, files in os.walk(SAVE_DIR):
        for file in files:
            if file.endswith(".dcm"):
                path = os.path.join(root, file)
                try:
                    ds = dcmread(path)
                    series_uid = ds.SeriesInstanceUID
                    
                    if series_uid not in series_groups:
                        series_groups[series_uid] = []
                    series_groups[series_uid].append(path)
                except Exception as e:
                    print(f"Error reading {path}: {e}")
    
    # Send each series
    for series_uid, file_paths in series_groups.items():
        print(f"Uploading series {series_uid} ({len(file_paths)} files)")
        
        for path in file_paths:
            try:
                with open(path, 'rb') as f:
                    response = requests.post(f"{ORTHANC_URL}/instances", 
                                           auth=AUTH, 
                                           data=f.read(),
                                           headers={'Content-Type': 'application/dicom'})
                    
                    if response.status_code != 200:
                        print(f"Failed to upload {os.path.basename(path)}: {response.status_code}")
            except Exception as e:
                print(f"Error uploading {path}: {e}")

# Main pipeline
def main():
    studies = get_study_list()
    if not studies:
        print("No studies found on PACS.")
        return

    # Use your specific study ID or pick the first one
    study_id = "6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6"  # Your study ID
    # study_id = studies[0]  # Or pick the first one
    print(f"Working on Study ID: {study_id}")

    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)

    print("Step 1: Downloading study...")
    download_study(study_id)
    
    print("Step 2: Modifying DICOM files...")
    modify_dicom_files()
    
    print("Step 3: Verifying modifications...")
    verify_modifications()
    
    print("Step 4: Sending back to PACS...")
    send_back_to_pacs()
    
    print("Completed: JSON data added and pushed back to PACS.")

# Test function to check specific file
def test_specific_file():
    test_file = "C:/Users/User/Downloads/bfa69214-4625-4ee6-84c7-983cb5e4b5f9.dcm"
    if os.path.exists(test_file):
        ds = dcmread(test_file)
        print("Tag Right Kidney:", ds.get((0x0011, 0x1010)))
        print("Tag Left Kidney:", ds.get((0x0011, 0x1011)))
    else:
        print(f"File not found: {test_file}")

if __name__ == "__main__":
    main()
    # Uncomment the line below to test a specific file
    # test_specific_file()



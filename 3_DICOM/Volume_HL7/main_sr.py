import requests
import os
import zipfile
import io
import json
import xml.etree.ElementTree as ET
from datetime import datetime
from pydicom import dcmread, dcmwrite, Dataset
from pydicom.tag import Tag
from pydicom.uid import generate_uid
from pydicom.sequence import Sequence
from pyorthanc import Orthanc
import time
import shutil

# Configuration
ORTHANC_URL = "http://localhost:8042"
ORTHANC_USER = 'admin'
ORTHANC_PASSWORD = 'password'
KIDNEY_DATA = {
    "Right Kidney": "125 ml",
    "Left Kidney": "132 ml"
}
SAVE_DIR = "study_files"

# Initialize Orthanc client
orthanc = Orthanc(ORTHANC_URL, username=ORTHANC_USER, password=ORTHANC_PASSWORD)

def modify_dicom_files():
    """
    Step 3: Add private tags to DICOM files (keeping original UIDs)
    """
    modified_count = 0
    for root, _, files in os.walk(SAVE_DIR):
        for file in files:
            if file.endswith(".dcm") or file.endswith(".IMA") or file.count(".") == 0:
                path = os.path.join(root, file)
                try:
                    ds = dcmread(path)

                    # Store original SOP Instance UID for reference
                    original_sop_uid = ds.SOPInstanceUID
                    
                    # Reserve private creator tag (0011,0010)
                    private_creator_tag = Tag(0x0011, 0x0010)
                    private_creator = "KidneyVolInfo"
                    ds.add_new(private_creator_tag, 'LO', private_creator)

                    # Add kidney volume data using private tags
                    ds.add_new(Tag(0x0011, 0x1010), 'LO', f"Right Kidney: {KIDNEY_DATA['Right Kidney']}")
                    ds.add_new(Tag(0x0011, 0x1011), 'LO', f"Left Kidney: {KIDNEY_DATA['Left Kidney']}")

                    # Keep all original UIDs - just adding tags
                    print(f"Modified: {path}")
                    print(f"  SOP Instance UID: {original_sop_uid} (unchanged)")
                    print(f"  Added kidney volume tags")
                    
                    dcmwrite(path, ds)
                    modified_count += 1
                    
                except Exception as e:
                    print(f"Error modifying {path}: {e}")
    
    print(f"Total files modified: {modified_count}")
    return modified_count

def delete_original_instances_from_orthanc(study_id):
    """
    Delete original instances before uploading modified ones
    This is necessary because Orthanc won't overwrite instances with same UID
    """
    try:
        # Get all instances in the study
        instances = orthanc.get_studies_id_instances(study_id)
        
        print(f"Deleting {len(instances)} original instances to allow updates...")
        
        deleted_count = 0
        for instance in instances:
            instance_id = instance['ID']
            try:
                orthanc.delete_instances_id(instance_id)
                deleted_count += 1
                print(f"Deleted original instance: {instance_id}")
            except Exception as e:
                print(f"Error deleting instance {instance_id}: {e}")
        
        print(f"Successfully deleted {deleted_count} original instances")
        return deleted_count
                
    except Exception as e:
        print(f"Error deleting original instances: {e}")
        return 0

def upload_modified_files_to_orthanc_fixed(folder_path, progress_callback=None):
    """
    Upload modified DICOM files to Orthanc with proper error handling
    """
    initial_time = time.perf_counter()
    
    # Get list of DICOM files
    dicom_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if file.endswith(".dcm") or file.endswith(".IMA") or file.count(".") == 0:
                dicom_files.append(os.path.join(root, file))
    
    total_steps = len(dicom_files)
    print(f"Total files to upload: {total_steps}")
    
    uploaded_count = 0
    failed_count = 0
    uploaded_instances = []
    
    for i, file_path in enumerate(dicom_files):
        try:
            with open(file_path, "rb") as f:
                # Send the DICOM file to the Orthanc server
                result = orthanc.post_instances(f.read())
                uploaded_instances.append(result)
                uploaded_count += 1
                
                progress = round((i + 1) / total_steps * 100, 2)
                print(f'Uploaded: {os.path.basename(file_path)} - Progress: {progress}%')
                print(f'  Instance ID: {result.get("ID", "Unknown")}')
                
                # Call progress callback if provided
                if progress_callback:
                    progress_callback(progress, i + 1, total_steps)
                    
        except Exception as e:
            failed_count += 1
            print(f"Error uploading {file_path}: {e}")
    
    final_time = time.perf_counter()
    time_duration = final_time - initial_time
    
    print(f"Upload completed in {time_duration:.2f} seconds")
    print(f"Upload summary: {uploaded_count} successful, {failed_count} failed")
    
    return {
        "uploaded": uploaded_count, 
        "failed": failed_count, 
        "duration": time_duration,
        "instances": uploaded_instances
    }

def verify_measurements_in_orthanc_fixed(study_id=None, instance_ids=None):
    """
    Verify that uploaded files contain the measurement data
    Can verify by study ID or specific instance IDs
    """
    try:
        if instance_ids:
            # Verify specific instances
            instances_to_check = [{'ID': iid} for iid in instance_ids]
            print(f"Checking specific {len(instances_to_check)} instances for measurement data...")
        elif study_id:
            # Get all instances in the study
            instances_to_check = orthanc.get_studies_id_instances(study_id)
            print(f"Checking {len(instances_to_check)} instances in study for measurement data...")
        else:
            print("No study ID or instance IDs provided for verification")
            return
        
        print(f"\n=== MEASUREMENT DATA VERIFICATION ===")
        
        verified_count = 0
        for i, instance in enumerate(instances_to_check[:5]):  # Check first 5 instances
            instance_id = instance['ID']
            print(f"\nInstance {i+1}: {instance_id}")
            
            try:
                # Get DICOM tags using Orthanc library
                tags = orthanc.get_instances_id_tags(instance_id, params={'simplify': ''})
                
                found_measurements = False
                
                # Check for our specific private tags
                private_tags_found = []
                
                # Look for our private creator
                if '0011,0010' in tags:
                    creator_value = tags['0011,0010']
                    print(f"  ✓ Private Creator (0011,0010): {creator_value}")
                    if 'KidneyVolInfo' in creator_value:
                        private_tags_found.append(f"Correct Private Creator: {creator_value}")
                        found_measurements = True
                
                # Look for our kidney volume tags
                if '0011,1010' in tags:
                    right_kidney = tags['0011,1010']
                    print(f"  ✓ Right Kidney (0011,1010): {right_kidney}")
                    private_tags_found.append(f"Right Kidney Data: {right_kidney}")
                    found_measurements = True
                
                if '0011,1011' in tags:
                    left_kidney = tags['0011,1011']
                    print(f"  ✓ Left Kidney (0011,1011): {left_kidney}")
                    private_tags_found.append(f"Left Kidney Data: {left_kidney}")
                    found_measurements = True
                
                # Also check other tags where kidney data might appear
                for tag_name, tag_value in tags.items():
                    if isinstance(tag_value, str) and 'kidney' in tag_value.lower():
                        if tag_name not in ['0011,1010', '0011,1011']:  # Don't duplicate our private tags
                            print(f"  ✓ Found kidney data in {tag_name}: {tag_value}")
                            found_measurements = True
                
                if found_measurements:
                    verified_count += 1
                    print(f"  ✓ MEASUREMENT DATA CONFIRMED")
                else:
                    print(f"  ✗ No measurement data found")
                    
            except Exception as e:
                print(f"  ✗ Could not retrieve tags: {e}")
        
        print(f"\n=== VERIFICATION SUMMARY ===")
        print(f"Instances with measurement data: {verified_count}/{min(5, len(instances_to_check))} checked")
        
        return verified_count > 0
        
    except Exception as e:
        print(f"Error during verification: {e}")
        return False

def approach_3_standard_tags_fixed(study_id):
    """
    FIXED: Add kidney volume tags to existing instances (keeping original UIDs)
    """
    print("=== APPROACH 3: Adding Kidney Volume Tags to Existing Instances ===")
    
    try:
        # Create save directory
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        else:
            # Clean existing files
            shutil.rmtree(SAVE_DIR)
            os.makedirs(SAVE_DIR)
        
        # Download study
        print("Downloading study files...")
        response = requests.get(f"{ORTHANC_URL}/studies/{study_id}/archive", 
                              auth=(ORTHANC_USER, ORTHANC_PASSWORD))
        response.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall(SAVE_DIR)
        print(f"Downloaded study files to {SAVE_DIR}")
        
        # Modify files (keeping original UIDs, just adding tags)
        print("Adding kidney volume tags to DICOM files...")
        modified_count = modify_dicom_files()
        
        if modified_count == 0:
            print("No files were modified - check file paths and formats")
            return None
        
        # CRITICAL: Delete original instances first 
        # (Orthanc won't overwrite instances with same SOP Instance UID)
        print("Deleting original instances from Orthanc...")
        deleted_count = delete_original_instances_from_orthanc(study_id)
        
        if deleted_count == 0:
            print("WARNING: No original instances were deleted - upload may fail")
        
        # Upload modified files (same UIDs, but now with kidney volume tags)
        print("Uploading modified files back to Orthanc...")
        upload_result = upload_modified_files_to_orthanc_fixed(SAVE_DIR)
        
        if upload_result["uploaded"] == 0:
            print("No files were uploaded - check for errors")
            return None
        
        # Verify the instances now contain measurement data
        print("Verifying instances contain kidney volume data...")
        verification_result = verify_measurements_in_orthanc_fixed(study_id=study_id)
        
        if verification_result:
            print("✓ SUCCESS: Existing instances now contain kidney volume data")
        else:
            print("✗ WARNING: Instances uploaded but measurement data not found")
        
        return {
            "modified": modified_count, 
            "deleted_original": deleted_count,
            "uploaded": upload_result["uploaded"], 
            "failed": upload_result["failed"],
            "duration": upload_result["duration"]
        }
        
    except Exception as e:
        print(f"Error in Approach 3: {e}")
        import traceback
        traceback.print_exc()
        return None

def main():
    """Main function to run the kidney volume integration"""
    # Check if PACS is accessible
    try:
        system_info = orthanc.get_system()
        print("✓ Connected to Orthanc PACS")
        print(f"Orthanc Version: {system_info.get('Version', 'Unknown')}")
    except Exception as e:
        print(f"✗ Cannot connect to Orthanc PACS: {e}")
        return
    
    # Get available studies
    try:
        studies = orthanc.get_studies()
        if not studies:
            print("No studies found on PACS.")
            return
        
        print(f"Found {len(studies)} studies on PACS")
        
        # Show available studies
        print("\nAvailable studies:")
        for i, study in enumerate(studies[:5]):  # Show first 5 studies
            study_info = orthanc.get_studies_id(study)
            patient_name = study_info.get('PatientMainDicomTags', {}).get('PatientName', 'Unknown')
            study_date = study_info.get('MainDicomTags', {}).get('StudyDate', 'Unknown')
            print(f"{i+1}. Study ID: {study} - Patient: {patient_name} - Date: {study_date}")
        
        # Use your specific study ID or let user choose
        study_id = "6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6"  # Your study ID
        
        # Verify study exists
        try:
            study_info = orthanc.get_studies_id(study_id)
            print(f"\nWorking with Study ID: {study_id}")
            print(f"Patient: {study_info.get('PatientMainDicomTags', {}).get('PatientName', 'Unknown')}")
        except:
            print(f"Study {study_id} not found. Please choose from available studies.")
            return
        
        # Run the fixed approach
        result = approach_3_standard_tags_fixed(study_id)
        
        if result:
            print(f"\n=== FINAL RESULTS ===")
            print(f"Modified files: {result['modified']}")
            print(f"Deleted original instances: {result['deleted_original']}")
            print(f"Uploaded files: {result['uploaded']}")
            print(f"Failed uploads: {result['failed']}")
            print(f"Duration: {result['duration']:.2f} seconds")
            print("✓ Original instances now contain kidney volume data")
        else:
            print("Process failed - check error messages above")
            
    except Exception as e:
        print(f"Error in main execution: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
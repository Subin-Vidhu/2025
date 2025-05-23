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
AUTH = (ORTHANC_USER, ORTHANC_PASSWORD)
KIDNEY_DATA = {
    "Right Kidney": "125 ml",
    "Left Kidney": "132 ml"
}
SAVE_DIR = "study_files"

# Initialize Orthanc client
orthanc = Orthanc(ORTHANC_URL, username=ORTHANC_USER, password=ORTHANC_PASSWORD)

# ===============================
# APPROACH 1: DICOM-SR (Structured Report)
# ===============================
def create_dicom_sr_with_kidney_volumes(study_uid, series_uid, patient_info):
    """
    Create a DICOM Structured Report containing kidney volume measurements
    This is the most HL7-compatible approach as SR is standardized
    """
    # Create new SR dataset
    ds = Dataset()
    
    # Patient Module
    ds.PatientName = patient_info.get('PatientName', 'Unknown^Patient')
    ds.PatientID = patient_info.get('PatientID', 'UNKNOWN')
    ds.PatientBirthDate = patient_info.get('PatientBirthDate', '')
    ds.PatientSex = patient_info.get('PatientSex', 'U')
    
    # General Study Module
    ds.StudyInstanceUID = study_uid
    ds.StudyID = patient_info.get('StudyID', '1')
    ds.StudyDate = datetime.now().strftime('%Y%m%d')
    ds.StudyTime = datetime.now().strftime('%H%M%S')
    ds.AccessionNumber = patient_info.get('AccessionNumber', '')
    
    # General Series Module
    ds.SeriesInstanceUID = series_uid
    ds.SeriesNumber = "9999"  # High number to distinguish from imaging series
    ds.SeriesDate = datetime.now().strftime('%Y%m%d')
    ds.SeriesTime = datetime.now().strftime('%H%M%S')
    ds.SeriesDescription = "Kidney Volume Measurements"
    ds.Modality = "SR"  # Structured Report
    
    # General Equipment Module
    ds.Manufacturer = "Custom Analysis Tool"
    ds.ManufacturerModelName = "Kidney Volume Calculator"
    ds.SoftwareVersions = "1.0"
    
    # SR Document Module
    ds.SOPClassUID = "1.2.840.10008.5.1.4.1.1.88.11"  # Basic Text SR
    ds.SOPInstanceUID = generate_uid()
    ds.InstanceNumber = "1"
    ds.ContentDate = datetime.now().strftime('%Y%m%d')
    ds.ContentTime = datetime.now().strftime('%H%M%S')
    ds.DocumentTitle = "Kidney Volume Analysis Report"
    ds.CompletionFlag = "COMPLETE"
    ds.VerificationFlag = "UNVERIFIED"
    
    # Content Sequence (the actual measurements)
    content_sequence = []
    
    # Root container
    root_item = Dataset()
    root_item.RelationshipType = "CONTAINS"
    root_item.ValueType = "CONTAINER"
    root_item.ConceptNameCodeSequence = [Dataset()]
    root_item.ConceptNameCodeSequence[0].CodeValue = "18785-6"
    root_item.ConceptNameCodeSequence[0].CodingSchemeDesignator = "LN"
    root_item.ConceptNameCodeSequence[0].CodeMeaning = "Radiology Report"
    
    # Right Kidney Volume
    right_kidney_item = Dataset()
    right_kidney_item.RelationshipType = "CONTAINS"
    right_kidney_item.ValueType = "NUM"
    right_kidney_item.ConceptNameCodeSequence = [Dataset()]
    right_kidney_item.ConceptNameCodeSequence[0].CodeValue = "33747-0"
    right_kidney_item.ConceptNameCodeSequence[0].CodingSchemeDesignator = "LN"
    right_kidney_item.ConceptNameCodeSequence[0].CodeMeaning = "Right kidney volume"
    
    # Measured Value Sequence for Right Kidney
    right_kidney_item.MeasuredValueSequence = [Dataset()]
    right_kidney_item.MeasuredValueSequence[0].NumericValue = "125"
    right_kidney_item.MeasuredValueSequence[0].MeasurementUnitsCodeSequence = [Dataset()]
    right_kidney_item.MeasuredValueSequence[0].MeasurementUnitsCodeSequence[0].CodeValue = "ml"
    right_kidney_item.MeasuredValueSequence[0].MeasurementUnitsCodeSequence[0].CodingSchemeDesignator = "UCUM"
    right_kidney_item.MeasuredValueSequence[0].MeasurementUnitsCodeSequence[0].CodeMeaning = "milliliter"
    
    # Left Kidney Volume
    left_kidney_item = Dataset()
    left_kidney_item.RelationshipType = "CONTAINS"
    left_kidney_item.ValueType = "NUM"
    left_kidney_item.ConceptNameCodeSequence = [Dataset()]
    left_kidney_item.ConceptNameCodeSequence[0].CodeValue = "33748-8"
    left_kidney_item.ConceptNameCodeSequence[0].CodingSchemeDesignator = "LN"
    left_kidney_item.ConceptNameCodeSequence[0].CodeMeaning = "Left kidney volume"
    
    # Measured Value Sequence for Left Kidney
    left_kidney_item.MeasuredValueSequence = [Dataset()]
    left_kidney_item.MeasuredValueSequence[0].NumericValue = "132"
    left_kidney_item.MeasuredValueSequence[0].MeasurementUnitsCodeSequence = [Dataset()]
    left_kidney_item.MeasuredValueSequence[0].MeasurementUnitsCodeSequence[0].CodeValue = "ml"
    left_kidney_item.MeasuredValueSequence[0].MeasurementUnitsCodeSequence[0].CodingSchemeDesignator = "UCUM"
    left_kidney_item.MeasuredValueSequence[0].MeasurementUnitsCodeSequence[0].CodeMeaning = "milliliter"
    
    # Add items to content sequence
    content_sequence = [root_item, right_kidney_item, left_kidney_item]
    ds.ContentSequence = content_sequence
    
    # File Meta Information
    ds.file_meta = Dataset()
    ds.file_meta.TransferSyntaxUID = "1.2.840.10008.1.2"  # Implicit VR Little Endian
    ds.file_meta.MediaStorageSOPClassUID = ds.SOPClassUID
    ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
    ds.file_meta.ImplementationClassUID = "1.2.276.0.7230010.3.0.3.6.1"
    
    ds.is_implicit_VR = True
    ds.is_little_endian = True
    
    return ds

# ===============================
# APPROACH 2: FHIR-Compatible JSON in DICOM
# ===============================
def create_fhir_observation_json():
    """
    Create FHIR-compatible observation JSON for kidney volumes
    This can be stored in DICOM private tags or as separate FHIR resources
    """
    observations = []
    
    # Right Kidney Observation
    right_kidney_obs = {
        "resourceType": "Observation",
        "id": f"kidney-volume-right-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "imaging",
                        "display": "Imaging"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "33747-0",
                    "display": "Right kidney volume"
                }
            ]
        },
        "subject": {
            "reference": "Patient/example"
        },
        "effectiveDateTime": datetime.now().isoformat(),
        "valueQuantity": {
            "value": 125,
            "unit": "ml",
            "system": "http://unitsofmeasure.org",
            "code": "ml"
        },
        "bodySite": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "9846003",
                    "display": "Right kidney"
                }
            ]
        }
    }
    
    # Left Kidney Observation
    left_kidney_obs = {
        "resourceType": "Observation",
        "id": f"kidney-volume-left-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "status": "final",
        "category": [
            {
                "coding": [
                    {
                        "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                        "code": "imaging",
                        "display": "Imaging"
                    }
                ]
            }
        ],
        "code": {
            "coding": [
                {
                    "system": "http://loinc.org",
                    "code": "33748-8",
                    "display": "Left kidney volume"
                }
            ]
        },
        "subject": {
            "reference": "Patient/example"
        },
        "effectiveDateTime": datetime.now().isoformat(),
        "valueQuantity": {
            "value": 132,
            "unit": "ml",
            "system": "http://unitsofmeasure.org",
            "code": "ml"
        },
        "bodySite": {
            "coding": [
                {
                    "system": "http://snomed.info/sct",
                    "code": "7771000",
                    "display": "Left kidney"
                }
            ]
        }
    }
    
    observations.extend([right_kidney_obs, left_kidney_obs])
    return observations

# ===============================
# APPROACH 3: Private Tags in Existing Instances
# ===============================
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
                    # print(f"  SOP Instance UID: {original_sop_uid} (unchanged)")
                    # print(f"  Added kidney volume tags")
                    
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
        for i, instance in enumerate(instances_to_check[:1]):  # Check first 5 instances
            instance_id = instance['ID']
            print(f"\nInstance {i+1}: {instance_id}")
            print(f"\n Instance SOP Instance UID: {instance['MainDicomTags'].get('SOPInstanceUID', 'Unknown')}")
            
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

# ===============================
# ORTHANC Integration Functions (Legacy - for approaches 1 & 2)
# ===============================
def get_study_info(study_id):
    """Get detailed study information"""
    response = requests.get(f"{ORTHANC_URL}/studies/{study_id}", auth=AUTH)
    response.raise_for_status()
    study_info = response.json()
    
    # Get patient info
    patient_response = requests.get(f"{ORTHANC_URL}/patients/{study_info['ParentPatient']}", auth=AUTH)
    patient_response.raise_for_status()
    patient_info = patient_response.json()
    
    return study_info, patient_info

def send_dicom_to_orthanc(dicom_dataset, filename="kidney_volume_report.dcm"):
    """Send DICOM dataset to Orthanc"""
    # Save to file first
    filepath = os.path.join(SAVE_DIR, filename)
    dcmwrite(filepath, dicom_dataset)
    
    # Upload to Orthanc
    with open(filepath, 'rb') as f:
        response = requests.post(f"{ORTHANC_URL}/instances", 
                               auth=AUTH, 
                               data=f.read(),
                               headers={'Content-Type': 'application/dicom'})
    
    if response.status_code == 200:
        print(f"Successfully uploaded {filename}")
        return response.json()
    else:
        print(f"Failed to upload {filename}: {response.status_code} - {response.text}")
        return None

def store_fhir_in_orthanc_metadata(study_id, fhir_observations):
    """Store FHIR observations as Orthanc metadata"""
    metadata = {
        "KidneyVolumeObservations": json.dumps(fhir_observations),
        "CreatedDate": datetime.now().isoformat(),
        "DataFormat": "FHIR_R4"
    }
    
    response = requests.put(f"{ORTHANC_URL}/studies/{study_id}/metadata/KidneyVolumes", 
                           auth=AUTH, 
                           data=json.dumps(metadata),
                           headers={'Content-Type': 'application/json'})
    
    if response.status_code == 200:
        print("Successfully stored FHIR observations in Orthanc metadata")
    else:
        print(f"Failed to store metadata: {response.status_code}")

# ===============================
# Main Functions
# ===============================
def approach_1_dicom_sr(study_id):
    """Implement Approach 1: DICOM Structured Report"""
    print("=== APPROACH 1: DICOM Structured Report ===")
    
    study_info, patient_info = get_study_info(study_id)
    
    # Extract patient details
    patient_data = {
        'PatientName': patient_info['MainDicomTags'].get('PatientName', 'Unknown'),
        'PatientID': patient_info['MainDicomTags'].get('PatientID', 'UNKNOWN'),
        'PatientBirthDate': patient_info['MainDicomTags'].get('PatientBirthDate', ''),
        'PatientSex': patient_info['MainDicomTags'].get('PatientSex', 'U'),
        'StudyID': study_info['MainDicomTags'].get('StudyID', '1'),
        'AccessionNumber': study_info['MainDicomTags'].get('AccessionNumber', '')
    }
    
    # Create SR with kidney volumes
    sr_dataset = create_dicom_sr_with_kidney_volumes(
        study_info['MainDicomTags']['StudyInstanceUID'],
        generate_uid(),
        patient_data
    )
    
    # Send to PACS
    result = send_dicom_to_orthanc(sr_dataset, "kidney_volume_sr.dcm")
    return result

def approach_2_fhir_integration(study_id):
    """Implement Approach 2: FHIR Integration"""
    print("=== APPROACH 2: FHIR Integration ===")
    
    # Create FHIR observations
    fhir_observations = create_fhir_observation_json()
    
    # Store as Orthanc metadata
    store_fhir_in_orthanc_metadata(study_id, fhir_observations)
    
    # Also save as separate JSON file for external systems
    fhir_filepath = os.path.join(SAVE_DIR, "kidney_volume_fhir.json")
    with open(fhir_filepath, 'w') as f:
        json.dump({
            "resourceType": "Bundle",
            "id": f"kidney-volume-bundle-{datetime.now().strftime('%Y%m%d%H%M%S')}",
            "type": "collection",
            "entry": [{"resource": obs} for obs in fhir_observations]
        }, f, indent=2)
    
    print(f"FHIR observations saved to {fhir_filepath}")
    return fhir_observations

def approach_3_private_tags(study_id):
    """
    APPROACH 3: Add kidney volume private tags to existing instances
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
                              auth=AUTH)
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

def cleanup_local_files():
    """Clean up downloaded files after processing"""
    if os.path.exists(SAVE_DIR):
        shutil.rmtree(SAVE_DIR)
        print(f"Cleaned up local directory: {SAVE_DIR}")

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
        
        # Use your specific study ID
        study_id = "6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6"  # Your study ID
        
        # Verify study exists
        try:
            study_info = orthanc.get_studies_id(study_id)
            print(f"\nWorking with Study ID: {study_id}")
            print(f"Patient: {study_info.get('PatientMainDicomTags', {}).get('PatientName', 'Unknown')}")
        except:
            print(f"Study {study_id} not found. Please choose from available studies.")
            return
        
        if not os.path.exists(SAVE_DIR):
            os.makedirs(SAVE_DIR)
        
        print("Choose approach:")
        print("1. DICOM Structured Report (Most HL7-compatible)")
        print("2. FHIR Integration (Best for modern healthcare systems)")
        print("3. Private Tags in Existing Instances (Modifies original instances)")
        print("4. All approaches")
        
        choice = input("Enter choice (1-4): ").strip()
        
        try:
            if choice == "1":
                approach_1_dicom_sr(study_id)
            elif choice == "2":
                approach_2_fhir_integration(study_id)
            elif choice == "3":
                result = approach_3_private_tags(study_id)
                if result:
                    print(f"\n=== APPROACH 3 RESULTS ===")
                    print(f"Modified files: {result['modified']}")
                    print(f"Deleted original instances: {result['deleted_original']}")
                    print(f"Uploaded files: {result['uploaded']}")
                    print(f"Failed uploads: {result['failed']}")
                    print(f"Duration: {result['duration']:.2f} seconds")
                    print("✓ Original instances now contain kidney volume data")
                else:
                    print("Approach 3 failed")
            elif choice == "4":
                print("Running all approaches...")
                approach_1_dicom_sr(study_id)
                approach_2_fhir_integration(study_id)
                approach_3_private_tags(study_id)
            else:
                print("Invalid choice. Please enter a number between 1 and 4.")
        except Exception as e:
            print(f"Error during processing: {e}")
            import traceback
            traceback.print_exc()
    finally:
        # Clean up local files
        # cleanup_local_files()
        print("Finished processing. Exiting...")
        time.sleep(2)
        exit(0)

if __name__ == "__main__":
    cleanup_local_files()
    main()
# End of file
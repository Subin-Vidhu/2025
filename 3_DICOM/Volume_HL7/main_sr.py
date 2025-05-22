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

# Configuration
ORTHANC_URL = "http://localhost:8042"
AUTH = ('admin', 'password')
KIDNEY_DATA = {
    "Right Kidney": "125 ml",
    "Left Kidney": "132 ml"
}
SAVE_DIR = "study_files"

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
# APPROACH 3: Standard DICOM Tags for Measurements - SIMPLIFIED VERSION
# ===============================

# ===============================
# Modified DICOM file processing function
# ===============================
def modify_dicom_files():
    """
    Step 3: Add private tags to DICOM files
    """
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
    return modified_count

# ===============================
# ORTHANC Integration Functions
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

def approach_3_standard_tags(study_id):
    """Implement Approach 3: Standard DICOM Measurement Tags with New Private Tag Method"""
    print("=== APPROACH 3: Standard DICOM Measurement Tags (With New Private Tag Method) ===")
    
    # Create save directory
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    # Download study
    print("Downloading study files...")
    response = requests.get(f"{ORTHANC_URL}/studies/{study_id}/archive", auth=AUTH)
    response.raise_for_status()
    with zipfile.ZipFile(io.BytesIO(response.content)) as z:
        z.extractall(SAVE_DIR)
    
    # Modify files using your specific private tag approach
    print("Modifying DICOM files with private tags (0011,0010), (0011,1010), (0011,1011)...")
    modified_count = modify_dicom_files()
    
    # Send modified files back to Orthanc
    print("Sending modified files back to Orthanc...")
    uploaded_count = 0
    failed_count = 0
    
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
    
    # Verify the modifications were preserved
    print("Verifying uploaded files contain measurement data...")
    verify_measurements_in_orthanc(study_id)
    
    return {"modified": modified_count, "uploaded": uploaded_count, "failed": failed_count}

def verify_measurements_in_orthanc(study_id):
    """Verify that uploaded files contain the measurement data with new private tags"""
    try:
        # Get all instances in the study
        response = requests.get(f"{ORTHANC_URL}/studies/{study_id}/instances", auth=AUTH)
        response.raise_for_status()
        instances = response.json()
        
        print(f"\n=== MEASUREMENT DATA VERIFICATION (NEW PRIVATE TAG METHOD) ===")
        print(f"Checking {len(instances)} instances for measurement data...\n")
        
        verified_count = 0
        for i, instance in enumerate(instances[:3]):  # Check first 3 instances as examples
            instance_id = instance['ID']
            print(f"Instance {i+1}: {instance_id}")
            
            # Get DICOM tags
            tags_response = requests.get(f"{ORTHANC_URL}/instances/{instance_id}/tags?simplify", auth=AUTH)
            if tags_response.status_code == 200:
                tags = tags_response.json()
                
                found_measurements = False
                
                # Check for Image Comments (most visible)
                if 'ImageComments' in tags and 'KIDNEY' in tags['ImageComments'].upper():
                    print(f"  ✓ Image Comments (0020,4000): {tags['ImageComments']}")
                    found_measurements = True
                
                # Check for Study Comments
                if 'StudyComments' in tags and 'KIDNEY' in tags['StudyComments'].upper():
                    print(f"  ✓ Study Comments (0032,4000): {tags['StudyComments']}")
                    found_measurements = True
                
                # Check for Content Description
                if 'ContentDescription' in tags:
                    print(f"  ✓ Content Description (0070,0081): {tags['ContentDescription']}")
                    found_measurements = True
                
                # Check for Content Label
                if 'ContentLabel' in tags:
                    print(f"  ✓ Content Label (0070,0080): {tags['ContentLabel']}")
                    found_measurements = True
                
                # Check for our specific private tags (0011,0010), (0011,1010), (0011,1011)
                private_tags_found = []
                
                # Look for private creator tag
                if '00110010' in tags or any('0011' in str(k) and 'KidneyVolInfo' in str(v) for k, v in tags.items()):
                    private_tags_found.append("Private Creator (0011,0010): KidneyVolInfo")
                
                # Look for kidney data tags
                for tag_name, tag_value in tags.items():
                    if ('00111010' in str(tag_name) or '00111011' in str(tag_name)) and isinstance(tag_value, str):
                        private_tags_found.append(f"Kidney Data ({tag_name}): {tag_value}")
                    elif isinstance(tag_value, str) and 'kidney' in tag_value.lower():
                        private_tags_found.append(f"Found kidney data in {tag_name}: {tag_value}")
                
                if private_tags_found:
                    print(f"  ✓ Private Tags Found:")
                    for tag in private_tags_found:
                        print(f"    {tag}")
                    found_measurements = True
                
                if found_measurements:
                    verified_count += 1
                    print(f"  ✓ MEASUREMENT DATA FOUND\n")
                else:
                    print(f"  ✗ No measurement data found\n")
            else:
                print(f"  ✗ Could not retrieve tags\n")
        
        print(f"=== SUMMARY ===")
        print(f"Instances with measurement data: {verified_count}/{min(3, len(instances))} checked")
        print(f"\nTo view measurement data in DICOM viewers, look for:")
        print(f"  • Image Comments (Tag 0020,4000) - Most widely supported")
        print(f"  • Study Comments (Tag 0032,4000) - Visible in study info")  
        print(f"  • Content Description (Tag 0070,0081) - Standard content tag")
        print(f"  • Content Label (Tag 0070,0080) - Standard content tag")
        print(f"  • Private Creator (Tag 0011,0010) - Should show 'KidneyVolInfo'")
        print(f"  • Right Kidney Data (Tag 0011,1010) - Right kidney volume")
        print(f"  • Left Kidney Data (Tag 0011,1011) - Left kidney volume")
        print(f"  • Measurement Sequence (Tag 0011,1020) - Structured measurements")
        
    except Exception as e:
        print(f"Error during verification: {e}")

def cleanup_local_files():
    """Clean up downloaded files after processing"""
    import shutil
    if os.path.exists(SAVE_DIR):
        shutil.rmtree(SAVE_DIR)
        print(f"Cleaned up local directory: {SAVE_DIR}")

def main():
    """Main function to run the kidney volume integration"""
    # Check if PACS is accessible
    try:
        response = requests.get(f"{ORTHANC_URL}/system", auth=AUTH)
        response.raise_for_status()
        print("✓ Connected to Orthanc PACS")
    except Exception as e:
        print(f"✗ Cannot connect to Orthanc PACS: {e}")
        return
    
    # Get available studies
    studies = requests.get(f"{ORTHANC_URL}/studies", auth=AUTH).json()
    if not studies:
        print("No studies found on PACS.")
        return
    
    study_id = "6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6"  # Your study ID
    print(f"Working with Study ID: {study_id}")
    
    if not os.path.exists(SAVE_DIR):
        os.makedirs(SAVE_DIR)
    
    print("Choose approach:")
    print("1. DICOM Structured Report (Most HL7-compatible)")
    print("2. FHIR Integration (Best for modern healthcare systems)")
    print("3. Standard DICOM Measurement Tags (NEW Private Tag Method)")
    print("4. All approaches")
    
    choice = input("Enter choice (1-4): ").strip()
    
    try:
        if choice == "1":
            approach_1_dicom_sr(study_id)
        elif choice == "2":
            approach_2_fhir_integration(study_id)
        elif choice == "3":
            approach_3_standard_tags(study_id)
        elif choice == "4":
            approach_1_dicom_sr(study_id)
            approach_2_fhir_integration(study_id)
            approach_3_standard_tags(study_id)
        else:
            print("Invalid choice")
        
    finally:
        # Clean up local files
        print("Clean up local files case...")
        # cleanup_local_files()

if __name__ == "__main__":
    cleanup_local_files()
    main()
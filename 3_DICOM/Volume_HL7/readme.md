# Kidney Volume DICOM Integration Tool

## Overview
This script allows you to add kidney volume measurement data to DICOM medical imaging studies using three different approaches, making the data accessible to other healthcare systems. It works with an Orthanc PACS (Picture Archiving and Communication System) server to retrieve, modify, and store DICOM files.

## What Does This Tool Do?
When doctors perform kidney volume measurements, these measurements need to be stored alongside the imaging studies. This script provides three ways to integrate these measurements:

1. **DICOM Structured Reports (SR)**: Creates a new standardized report document within the study
2. **FHIR-Compatible JSON**: Stores data in a format compatible with modern healthcare data standards
3. **Private Tags**: Modifies the original DICOM files to include measurement data

## Prerequisites
- Python 3.6+
- Orthanc PACS server running locally (or accessible via network)
- The following Python packages:
  - `pydicom`
  - `pyorthanc`
  - `requests`

To install required packages:
```
pip install pydicom pyorthanc requests
```

## Configuration
At the top of the script, you'll find configuration settings you may need to modify:

```python
# Configuration
ORTHANC_URL = "http://localhost:8042"  # Change if your Orthanc server is elsewhere
ORTHANC_USER = 'admin'
ORTHANC_PASSWORD = 'password'
KIDNEY_DATA = {
    "Right Kidney": "125 ml",
    "Left Kidney": "132 ml"
}
SAVE_DIR = "study_files"  # Temporary directory for file operations
```

## How It Works: The Three Approaches

### Approach 1: DICOM Structured Reports (SR)
This approach creates a new standardized document within the DICOM study specifically designed to hold measurements. This is the most compatible with existing healthcare systems.

**Benefits:**
- Follows standard DICOM format for measurements
- Easily recognized by most DICOM viewers
- Clear separation of measurements from images

**Process:**
1. Retrieves study information from Orthanc
2. Creates a new DICOM SR document with kidney measurements
3. Uploads this new document back to the study

### Approach 2: FHIR Integration
FHIR (Fast Healthcare Interoperability Resources) is a modern standard for healthcare data exchange. This approach creates FHIR-compatible observation resources.

**Benefits:**
- Compatible with modern healthcare data systems
- Well-structured data format
- Easier integration with electronic health records

**Process:**
1. Creates FHIR Observation resources for kidney measurements
2. Stores them as metadata in Orthanc
3. Also saves them as a separate JSON file for external systems

### Approach 3: Private Tags
This approach modifies the original DICOM files by adding private tags containing kidney measurements.

**Benefits:**
- Measurements stay with the original images
- No additional documents to manage
- Direct access to measurements when viewing images

**Process:**
1. Downloads all DICOM files in the study
2. Adds private tags with kidney volume data
3. Replaces the original files in Orthanc with modified versions

## Usage Instructions

### Running the Script
1. Ensure Orthanc is running and accessible
2. Run the script with Python:
   ```
   python main_sr.py
   ```
3. The script will connect to Orthanc and list available studies
4. Choose which approach you want to use:
   - Option 1: DICOM Structured Report
   - Option 2: FHIR Integration
   - Option 3: Private Tags in Existing Instances
   - Option 4: All approaches

### Specifying a Study
By default, the script looks for a specific study ID. You can modify this line to use your own study ID:
```python
study_id = "6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6"  # Your study ID
```

## Key Functions Explained

### General Functions
- `main()`: The entry point that coordinates the entire process
- `cleanup_local_files()`: Removes temporary files after processing
- `get_study_info()`: Retrieves information about a study from Orthanc

### Approach 1: DICOM SR Functions
- `create_dicom_sr_with_kidney_volumes()`: Creates a structured report dataset
- `send_dicom_to_orthanc()`: Uploads the SR document to Orthanc

### Approach 2: FHIR Functions
- `create_fhir_observation_json()`: Creates FHIR-compatible observation data
- `store_fhir_in_orthanc_metadata()`: Stores FHIR data as Orthanc metadata

### Approach 3: Private Tags Functions
- `modify_dicom_files()`: Adds private tags to DICOM files
- `delete_original_instances_from_orthanc()`: Removes original files before uploading
- `upload_modified_files_to_orthanc_fixed()`: Uploads modified files to Orthanc
- `verify_measurements_in_orthanc_fixed()`: Confirms data was properly added

## Common Issues and Solutions

### Cannot connect to Orthanc
- Check if Orthanc is running
- Verify URL, username, and password in configuration
- Ensure network connectivity if Orthanc is on another machine

### No studies found
- Check that Orthanc contains DICOM studies
- Verify authentication credentials

### Upload failures
- Ensure the script has permission to write temporary files
- Check disk space for temporary file storage
- Increase timeout settings if dealing with large studies

## Understanding the Code Structure

The script is organized into several sections:
1. Configuration and imports
2. Functions for each approach
3. Helper functions for file and DICOM operations
4. Main execution function

Each approach is implemented as a separate function that can be called independently, making the code modular and easier to adapt for different use cases.

## Output Examples

When running the script successfully, you'll see progress information like:
```
✓ Connected to Orthanc PACS
Orthanc Version: 1.9.7
Found 12 studies on PACS

Available studies:
1. Study ID: abc123 - Patient: SMITH^JOHN - Date: 20230215
...

Working with Study ID: 6627b6ac-b846cbe0-a0af01cc-f94a6bd0-990a57c6
Patient: DOE^JANE

Choose approach:
1. DICOM Structured Report (Most HL7-compatible)
2. FHIR Integration (Best for modern healthcare systems)
3. Private Tags in Existing Instances (Modifies original instances)
4. All approaches
```

## Conclusion

This script provides flexible options for integrating kidney volume measurements with DICOM studies. Choose the approach that best fits your workflow and system compatibility needs.
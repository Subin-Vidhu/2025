Kidney Volume DICOM Integration Tool
A comprehensive Python tool for integrating kidney volume measurements into DICOM studies using multiple HL7-compatible approaches. This tool supports DICOM Structured Reports, FHIR integration, and private DICOM tags to ensure maximum compatibility across different healthcare systems.
🏥 Overview
This tool provides three different approaches to store kidney volume measurements in DICOM studies:

DICOM Structured Report (SR) - Creates standardized DICOM-SR documents
FHIR Integration - Generates FHIR R4-compliant observations
Private DICOM Tags - Embeds measurements directly into existing DICOM files

📋 Features

Multi-approach compatibility - Choose the best method for your healthcare system
HL7 FHIR R4 compliant - Uses standard LOINC codes and UCUM units
DICOM SR support - Creates proper structured reports with measurement sequences
Private tag preservation - Uses registered private creator tags to avoid conflicts
Orthanc PACS integration - Direct upload and metadata storage
Automatic verification - Validates that measurements are properly stored
UID management - Handles DICOM UID generation and conflict resolution

🛠️ Prerequisites
Required Python Packages
bashpip install requests pydicom
System Requirements

Python 3.7+
Access to an Orthanc PACS server
Network connectivity to PACS system

PACS Configuration

Orthanc PACS server running on localhost:8042 (default)
Authentication credentials (default: admin/password)
Write permissions to upload DICOM instances

⚙️ Configuration
Edit the configuration section in the script:
python# Configuration
ORTHANC_URL = "http://localhost:8042"  # Your Orthanc server URL
AUTH = ('admin', 'password')           # Your credentials
KIDNEY_DATA = {
    "Right Kidney": "125 ml",          # Right kidney volume
    "Left Kidney": "132 ml"            # Left kidney volume
}
SAVE_DIR = "study_files"               # Local working directory
🚀 Usage
Basic Usage
bashpython kidney_volume_integration.py
Interactive Menu
The tool presents an interactive menu with four options:
Choose approach:
1. DICOM Structured Report (Most HL7-compatible)
2. FHIR Integration (Best for modern healthcare systems)
3. Standard DICOM Measurement Tags (Private Tag Method)
4. All approaches
Study ID Configuration
Update the study ID in the main() function:
pythonstudy_id = "your-study-id-here"
📊 Approach Details
Approach 1: DICOM Structured Report (SR)
Best for: HL7 compliance, standardized reporting, enterprise PACS systems
Features:

Creates DICOM-SR with SOP Class UID 1.2.840.10008.5.1.4.1.1.88.11
Uses LOINC codes for kidney measurements:

Right Kidney: 33747-0
Left Kidney: 33748-8


UCUM units (ml for milliliters)
Proper measurement sequences with coded concepts
New series in existing study (Series Number: 9999)

Output: kidney_volume_sr.dcm
Approach 2: FHIR Integration
Best for: Modern healthcare systems, interoperability, cloud platforms
Features:

FHIR R4 compliant Observation resources
Stores as Orthanc metadata for API access
Uses standard terminologies:

LOINC codes for measurements
SNOMED CT for body sites
UCUM for units


JSON Bundle format for external systems

Output:

Orthanc metadata: /studies/{id}/metadata/KidneyVolumes
JSON file: kidney_volume_fhir.json

Approach 3: Private DICOM Tags
Best for: Direct DICOM viewer compatibility, embedded measurements, legacy systems
Features:

Registers private creator: "KidneyVolInfo" at tag (0011,0010)
Stores measurements in private tags:

(0011,1010): Right Kidney volume
(0011,1011): Left Kidney volume


Generates new SOPInstanceUIDs to avoid conflicts
Preserves all original DICOM data

Tags Used:
(0011,0010) LO "KidneyVolInfo"                    # Private Creator
(0011,1010) LO "Right Kidney: 125 ml"            # Right kidney data
(0011,1011) LO "Left Kidney: 132 ml"             # Left kidney data
🔍 Verification
The tool automatically verifies that measurements are properly stored by checking:

Private Creator Tags: Confirms "KidneyVolInfo" registration
Measurement Data: Validates kidney volume values are present
Tag Accessibility: Ensures data is readable via DICOM APIs

📁 File Structure
project/
├── kidney_volume_integration.py    # Main script
├── study_files/                   # Temporary working directory
│   ├── *.dcm                     # Downloaded/modified DICOM files
│   ├── kidney_volume_sr.dcm      # Generated SR document
│   └── kidney_volume_fhir.json   # FHIR observations
└── README.md                     # This file
🏥 Healthcare Integration
PACS Systems

Orthanc: Direct integration via REST API
dcm4che: Compatible via DICOM C-STORE
Conquest: Standard DICOM storage
Commercial PACS: Supports any DICOM-compliant system

EHR/EMR Systems

FHIR-enabled: Direct FHIR R4 observation import
HL7 v2: Can extract from DICOM-SR OBX segments
Legacy: DICOM tag-based data extraction

Viewing Software

DICOM Viewers: All approaches visible in metadata/tags
Web Viewers: FHIR JSON easily consumable
Radiology Workstations: SR documents appear as reports

🔧 Troubleshooting
Connection Issues
✗ Cannot connect to Orthanc PACS: Connection refused
Solution: Verify Orthanc is running and accessible at configured URL
Authentication Errors
Failed to upload: 401 Unauthorized
Solution: Check credentials in AUTH tuple
Study Not Found
No studies found on PACS
Solution: Upload test studies or verify study ID exists
Private Tag Conflicts
Error modifying DICOM: Tag already exists
Solution: Tool handles this automatically by generating new UIDs
Upload Failures
Failed to upload file: 400 Bad Request
Solution: Check DICOM file validity and PACS storage configuration
📋 DICOM Compliance
Standards Compliance

DICOM PS3.3: Information Object Definitions
DICOM PS3.5: Data Structures and Encoding
DICOM PS3.6: Data Dictionary
DICOM PS3.10: Media Storage and File Format

Private Tag Registration

Follows DICOM PS3.5 Section 7.8 for private data elements
Uses proper private creator registration
Avoids conflicts with standard and other private tags

SOP Classes Used

Basic Text SR: 1.2.840.10008.5.1.4.1.1.88.11
CT Image Storage: 1.2.840.10008.5.1.4.1.1.2 (modified files)
MR Image Storage: 1.2.840.10008.5.1.4.1.1.4 (modified files)

🔒 Security Considerations
Data Privacy

All processing done locally or on configured PACS
No external data transmission
Maintains original patient data integrity

Authentication

Uses configurable credentials
Supports basic HTTP authentication
Can be extended for certificate-based auth

Audit Trail

Logs all operations and modifications
Tracks uploaded instances
Maintains verification records

🚀 Advanced Usage
Batch Processing
Modify the script to process multiple studies:
pythonstudy_ids = ["study1", "study2", "study3"]
for study_id in study_ids:
    approach_3_standard_tags(study_id)
Custom Measurements
Update KIDNEY_DATA for different measurements:
pythonKIDNEY_DATA = {
    "Right Kidney": "128.5 ml",
    "Left Kidney": "135.2 ml",
    "Total Volume": "263.7 ml"
}
Integration with Analysis Tools
python# Example: Integration with AI analysis results
def process_ai_results(analysis_output):
    global KIDNEY_DATA
    KIDNEY_DATA = {
        "Right Kidney": f"{analysis_output['right_volume']:.1f} ml",
        "Left Kidney": f"{analysis_output['left_volume']:.1f} ml"
    }
    return KIDNEY_DATA
📈 Performance Considerations
Memory Usage

Downloads entire study to local storage
Memory usage proportional to study size
Automatic cleanup after processing

Network Bandwidth

Downloads full DICOM study initially
Uploads modified files back to PACS
Consider compression for large studies

Processing Time

Linear with number of DICOM instances
Typical processing: 1-5 seconds per file
Network latency affects total time

🔄 Version History
v1.0.0

Initial release with three integration approaches
Private tag method using (0011,xxxx) tags
FHIR R4 and DICOM-SR support
Orthanc PACS integration

🤝 Contributing
Development Setup

Clone repository
Install dependencies: pip install -r requirements.txt
Configure test PACS environment
Run tests: python -m pytest tests/

Code Standards

Follow PEP 8 style guidelines
Add docstrings for all functions
Include error handling and logging
Write unit tests for new features

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
📞 Support
Documentation

DICOM Standard: https://dicom.nema.org/
FHIR R4: https://hl7.org/fhir/R4/
Orthanc Documentation: https://book.orthanc-server.com/

Issues
For bugs and feature requests, please create an issue in the project repository.
Professional Support
For enterprise deployment and custom integration, contact your healthcare IT team or PACS vendor.

⚠️ Important: This tool is designed for development and testing purposes. Ensure compliance with your healthcare organization's policies and regulatory requirements before using in production environments.
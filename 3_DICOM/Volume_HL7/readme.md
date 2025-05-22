Approach 1: DICOM Structured Report (SR)
This is the most HL7-compatible approach:

Creates a standard DICOM SR document
Uses LOINC codes (33747-0 for right kidney, 33748-8 for left kidney)
Structured measurements with proper units (UCUM)
Fully standardized and interoperable with HL7 systems

Approach 2: FHIR Integration
Modern healthcare interoperability standard:

Creates FHIR R4 Observation resources
Uses standard terminologies (LOINC, SNOMED CT)
Can be stored as Orthanc metadata or external FHIR server
Perfect for integration with modern EHR systems

Approach 3: Standard DICOM Measurement Sequences
Uses standard DICOM tags instead of private ones:

MeasurementSequence with proper anatomical coding
SNOMED CT codes for kidney identification
Compatible with DICOM viewers and analysis tools

Key Improvements Over Your Original Code:

Standards Compliance: Uses LOINC, SNOMED CT, and UCUM standards
Interoperability: All approaches work with HL7-compatible systems
Multiple Options: Choose based on your specific requirements
Proper Coding: Uses standardized medical terminology
Future-Proof: FHIR approach ready for modern healthcare systems

Recommendations:

Use Approach 1 if you need maximum compatibility with existing HL7 systems
Use Approach 2 if you're working with modern healthcare infrastructure
Use Approach 3 if you want to enhance existing DICOM files without creating new documents
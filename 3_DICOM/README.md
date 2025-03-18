# DICOM Pixel Data and Frame Offset Analyzer

This Python script analyzes DICOM files to extract and verify pixel data offsets and frame positions. It's particularly useful for:
- Analyzing both single-frame and multi-frame DICOM images
- Working with compressed and uncompressed transfer syntaxes
- Verifying pixel data positions in DICOM files
- Detecting frame boundaries in multi-frame images
- Generating detailed analysis reports in JSON format

## Features

- **Comprehensive DICOM Analysis**
  - Extracts pixel data offsets
  - Analyzes frame positions in multi-frame images
  - Supports various DICOM transfer syntaxes
  - Handles both compressed and uncompressed data

- **Detailed Reporting**
  - Generates JSON reports with detailed analysis
  - Includes file information, DICOM identifiers, and pixel data details
  - Provides frame offset information for multi-frame images
  - Includes hex editor guides for manual verification

- **Robust Error Handling**
  - Gracefully handles missing DICOM headers
  - Provides detailed error reporting
  - Supports force reading of non-standard DICOM files

## Prerequisites

### Python Version
- Python 3.6 or higher

### Required Libraries
```bash
pip install pydicom
pip install numpy
```

## Installation

1. Clone or download this repository
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Project Structure

```
project_root/
├── Data/                      # Directory containing DICOM files
│   ├── CT000000.dcm          # Example CT image
│   ├── DX000000.dcm          # Example DX image
│   └── Test_Multiple_Slices/ # Directory for multi-slice analysis
├── JSON/                      # Directory for analysis results
│   ├── CT000000.dcm_analysis.json
│   ├── DX000000.dcm_analysis.json
│   └── series_analysis.json
├── Pixel_Offset_and_Image_Offset.py
└── README.md
```

## Usage

### Basic Usage

1. Place your DICOM files in the `Data` directory
2. Run the script:
```bash
python Pixel_Offset_and_Image_Offset.py
```

The script will:
- Analyze each DICOM file in the Data directory
- Generate individual JSON analysis files in the JSON directory
- Create a combined series_analysis.json file

### Command Line Arguments

The script supports the following command line arguments:
- `--force`: Force reading files with missing DICOM headers (default: True)
- `--input-dir`: Specify input directory (default: "Data")
- `--output-dir`: Specify output directory (default: "JSON")

Example:
```bash
python Pixel_Offset_and_Image_Offset.py --force True --input-dir "Data" --output-dir "JSON"
```

## Output Format

The script generates JSON files with the following structure:

```json
{
  "file_info": {
    "filename": "example.dcm",
    "filepath": "Data/example.dcm",
    "filesize": 1234567,
    "analysis_date": "2025-03-18 13:00:12"
  },
  "dicom_identifiers": {
    "SOPInstanceUID": "1.2.3.4.5",
    "SOPClassUID": "1.2.3.4.6",
    "StudyInstanceUID": "1.2.3.4.7",
    "SeriesInstanceUID": "1.2.3.4.8",
    "Modality": "CT",
    "TransferSyntaxUID": "1.2.840.10008.1.2",
    "TransferSyntaxName": "ImplicitVRLittleEndian",
    "ImplicitVR": true,
    "Compressed": false
  },
  "patient_info": {
    "PatientID": "12345",
    "PatientName": "John Doe",
    "PatientBirthDate": "19800101",
    "PatientSex": "M",
    "StudyDate": "20250318",
    "StudyTime": "130012",
    "StudyDescription": "CT Scan",
    "SeriesDescription": "Axial"
  },
  "pixel_data_info": {
    "pixel_data_offset": 1234,
    "pixel_data_tag_offset": 1234,
    "rows": 512,
    "columns": 512,
    "bits_allocated": 16,
    "bits_stored": 12,
    "high_bit": 11,
    "samples_per_pixel": 1,
    "photometric_interpretation": "MONOCHROME2",
    "pixel_representation": 0,
    "expected_frame_size": 524288,
    "actual_size": 524288,
    "compression_ratio": 1.0
  },
  "frame_info": {
    "is_multiframe": false,
    "frame_count": 1,
    "frame_offsets": []
  }
}
```

## Error Handling

The script includes comprehensive error handling:
- Gracefully handles missing DICOM headers
- Reports detailed error messages in the JSON output
- Continues processing even if individual files fail
- Provides traceback information for debugging

## Contributing

Feel free to submit issues and enhancement requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details. 
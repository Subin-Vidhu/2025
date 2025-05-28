import requests
import csv

ORTHANC_URL = "https://fdapacstest.protosonline.in"
AUTH = ('admin', 'password')

def get(endpoint):
    r = requests.get(f"{ORTHANC_URL}/{endpoint}", auth=AUTH)
    r.raise_for_status()
    return r.json()

def extract_dicom_values(tags_dict, prefix=''):
    """Extract only the Value from DICOM tags, using the tag Name and ID as the key"""
    result = {}
    
    for tag_id, tag_info in tags_dict.items():
        if isinstance(tag_info, dict):
            # Get the tag name and value
            tag_name = tag_info.get('Name', tag_id)
            tag_value = tag_info.get('Value', 'NA')
            
            # Clean tag_id by replacing commas with underscores
            clean_tag_id = tag_id.replace(',', '_')
            
            # Create field name with both tag name and DICOM tag ID
            if prefix:
                field_name = f"{prefix}_{tag_name}_{clean_tag_id}"
            else:
                field_name = f"{tag_name}_{clean_tag_id}"
            
            # Handle list values (convert to string)
            if isinstance(tag_value, list):
                tag_value = ', '.join(map(str, tag_value)) if tag_value else 'NA'
            
            result[field_name] = tag_value
            
            # Also create a clean version without tag ID for common fields
            if tag_name in ['PatientName', 'PatientID', 'StudyDescription', 'SeriesDescription', 'Modality']:
                clean_field_name = f"{prefix}_{tag_name}" if prefix else tag_name
                result[clean_field_name] = tag_value
                
        else:
            # Handle non-dict values directly
            clean_tag_id = tag_id.replace(',', '_')
            if prefix:
                field_name = f"{prefix}_{clean_tag_id}"
            else:
                field_name = clean_tag_id
            result[field_name] = tag_info
    
    return result

def collect_study_metadata():
    study_ids = get("studies")
    all_rows = []
    all_keys = set()
    
    for study_id in study_ids:
        print(f"Processing study: {study_id}")
        row_data = {}
        
        # Get study information
        study = get(f"studies/{study_id}")
        study_tags = get(f"studies/{study_id}/shared-tags")
        
        # Extract study-level tags
        study_values = extract_dicom_values(study_tags)
        row_data.update(study_values)
        
        # Add study metadata
        row_data["StudyInstanceUID"] = study_id
        row_data["StudyDescription"] = study_values.get("StudyDescription_0008_1030", study_values.get("StudyDescription", "NA"))
        
        # Get series information
        series_ids = study.get("Series", [])
        row_data["SeriesCount"] = len(series_ids)
        
        # Process each series
        for i, series_id in enumerate(series_ids):
            series = get(f"series/{series_id}")
            series_tags = get(f"series/{series_id}/shared-tags")
            
            # Extract series-level tags with series prefix
            series_prefix = f"Series_{i+1}" if len(series_ids) > 1 else "Series"
            series_values = extract_dicom_values(series_tags, series_prefix)
            row_data.update(series_values)
            
            # Add series metadata
            row_data[f"{series_prefix}_SeriesInstanceUID"] = series_id
            row_data[f"{series_prefix}_InstanceCount"] = len(series.get("Instances", []))
            
            # Get modality from MainDicomTags if available
            main_dicom_tags = series_tags.get("MainDicomTags", {})
            if isinstance(main_dicom_tags, dict):
                for key, value in main_dicom_tags.items():
                    row_data[f"{series_prefix}_{key}"] = value
        
        all_keys.update(row_data.keys())
        all_rows.append(row_data)
    
    return all_keys, all_rows

def write_metadata_to_csv(output_file='orthanc_study_metadata.csv'):
    keys, rows = collect_study_metadata()
    
    # Put PatientName and StudyInstanceUID first, then sort the rest
    priority_cols = ['PatientName', 'StudyInstanceUID']
    remaining_keys = sorted([k for k in keys if k not in priority_cols])
    sorted_keys = priority_cols + remaining_keys
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sorted_keys)
        writer.writeheader()
        
        for row in rows:
            # Fill missing values with 'NA'
            complete_row = {k: row.get(k, 'NA') for k in sorted_keys}
            writer.writerow(complete_row)
    
    print(f"✅ Exported {len(rows)} studies to {output_file}")
    print(f"📊 Total columns: {len(sorted_keys)}")

# Alternative version that creates a more normalized structure
def collect_series_level_metadata():
    """Creates one row per series instead of one row per study"""
    study_ids = get("studies")
    all_rows = []
    all_keys = set()
    
    for study_id in study_ids:
        print(f"Processing study: {study_id}")
        
        # Get study information
        study = get(f"studies/{study_id}")
        study_tags = get(f"studies/{study_id}/shared-tags")
        study_values = extract_dicom_values(study_tags)
        
        # Process each series separately
        series_ids = study.get("Series", [])
        
        for series_id in series_ids:
            row_data = {}
            
            # Add study-level data
            row_data["StudyInstanceUID"] = study_id
            row_data["StudyDescription"] = study_values.get("StudyDescription", "NA")
            
            # Add other important study fields
            for key in ["PatientName", "PatientID", "StudyDate", "StudyTime"]:
                if key in study_values:
                    row_data[key] = study_values[key]
            
            # Get series information
            series = get(f"series/{series_id}")
            series_tags = get(f"series/{series_id}/shared-tags")
            
            # Extract series-level tags
            series_values = extract_dicom_values(series_tags)
            
            # Add series data with cleaner names
            row_data["SeriesInstanceUID"] = series_id
            row_data["SeriesCount"] = len(series_ids)
            
            # Add MainDicomTags directly
            main_dicom_tags = series_tags.get("MainDicomTags", {})
            if isinstance(main_dicom_tags, dict):
                for key, value in main_dicom_tags.items():
                    row_data[f"MainDicomTags_{key}"] = value
            
            # Add other series values
            for key, value in series_values.items():
                if not key.startswith("MainDicomTags"):  # Avoid duplicates
                    row_data[key] = value
            
            all_keys.update(row_data.keys())
            all_rows.append(row_data)
    
    return all_keys, all_rows

def write_series_metadata_to_csv(output_file='orthanc_series_metadata.csv'):
    keys, rows = collect_series_level_metadata()
    
    # Put PatientName and StudyInstanceUID first, then sort the rest
    priority_cols = ['PatientName', 'StudyInstanceUID']
    remaining_keys = sorted([k for k in keys if k not in priority_cols])
    sorted_keys = priority_cols + remaining_keys
    
    with open(output_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=sorted_keys)
        writer.writeheader()
        
        for row in rows:
            complete_row = {k: row.get(k, 'NA') for k in sorted_keys}
            writer.writerow(complete_row)
    
    print(f"✅ Exported {len(rows)} series to {output_file}")
    print(f"📊 Total columns: {len(sorted_keys)}")

# Run both versions
if __name__ == "__main__":
    print("Generating study-level metadata...")
    write_metadata_to_csv()
    
    print("\nGenerating series-level metadata...")
    write_series_metadata_to_csv()

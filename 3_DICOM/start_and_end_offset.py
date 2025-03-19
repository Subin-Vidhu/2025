import pydicom
import os
import numpy as np
import json
from datetime import datetime

def analyze_dicom_offsets(dicom_path, results_dict=None, force=True):
    """
    Analyze DICOM file to extract and verify pixel data and frame offsets
    Works with both single-frame and multi-frame images
    Supports compressed and uncompressed transfer syntaxes
    
    Parameters:
    -----------
    dicom_path : str
        Path to the DICOM file to analyze
    results_dict : dict, optional
        Dictionary to store results if part of a batch process
    force : bool, optional
        Whether to force reading files with missing DICOM headers (default: True)
        
    Returns:
    --------
    dict
        Dictionary containing analysis results
        
    Notes:
    ------
    offset_from_pixel_data: Bytes from start of pixel data element content
    absolute_offset: Actual file position in bytes from start of file
    """
    # Check if file exists
    if not os.path.exists(dicom_path):
        print(f"\nFile not found: {dicom_path}")
        print("Please ensure the file exists.")
        return None
        
    print(f"Analyzing: {os.path.basename(dicom_path)}")
    
    # Initialize results dictionary
    result = {}
    
    try:
        # Basic file information
        result["file_info"] = {
            "filename": os.path.basename(dicom_path),
            "filepath": dicom_path,
            "filesize": os.path.getsize(dicom_path),
            "analysis_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        # Check if file is readable
        if not os.access(dicom_path, os.R_OK):
            print(f"\nFile is not readable: {dicom_path}")
            print("Please check file permissions.")
            result["error"] = {
                "message": "File is not readable",
                "details": "Check file permissions"
            }
            return result
            
        # Load the DICOM file with force=True to handle files missing standard headers
        try:
            ds = pydicom.dcmread(dicom_path, force=force)
        except Exception as e:
            print(f"\nError reading DICOM file: {e}")
            result["error"] = {
                "message": f"Error reading DICOM file: {str(e)}",
                "details": "File may be corrupted or not a valid DICOM file"
            }
            return result
        
        # Extract key DICOM identifiers
        result["dicom_identifiers"] = {}
        
        # Check if file_meta exists, if not create an empty one
        if not hasattr(ds, 'file_meta') or ds.file_meta is None:
            result["dicom_identifiers"]["warning"] = "No File Meta Information found in file"
            ds.file_meta = pydicom.dataset.FileMetaDataset()
            # Try to determine transfer syntax from file content
            # Default to implicit VR little endian if can't determine
            if not hasattr(ds.file_meta, 'TransferSyntaxUID'):
                ds.file_meta.TransferSyntaxUID = pydicom.uid.ImplicitVRLittleEndian
                result["dicom_identifiers"]["assumed_transfer_syntax"] = "ImplicitVRLittleEndian (assumed)"
        
        # Now extract identifiers, using getattr to avoid errors if attributes don't exist
        result["dicom_identifiers"].update({
            "SOPInstanceUID": getattr(ds, "SOPInstanceUID", "Unknown"),
            "SOPClassUID": getattr(ds, "SOPClassUID", "Unknown"),
            "StudyInstanceUID": getattr(ds, "StudyInstanceUID", "Unknown"),
            "SeriesInstanceUID": getattr(ds, "SeriesInstanceUID", "Unknown"),
            "Modality": getattr(ds, "Modality", "Unknown"),
            "TransferSyntaxUID": str(getattr(ds.file_meta, "TransferSyntaxUID", "Unknown")),
            "TransferSyntaxName": getattr(ds.file_meta, "TransferSyntaxUID", "Unknown").name if hasattr(ds.file_meta, "TransferSyntaxUID") else "Unknown",
            "ImplicitVR": getattr(ds.file_meta, "TransferSyntaxUID", "Unknown").is_implicit_VR if hasattr(ds.file_meta, "TransferSyntaxUID") else "Unknown",
            "Compressed": getattr(ds.file_meta, "TransferSyntaxUID", "Unknown").is_compressed if hasattr(ds.file_meta, "TransferSyntaxUID") else "Unknown"
        })
        
        # Add patient and study information if available
        result["patient_info"] = {
            "PatientID": getattr(ds, "PatientID", "Unknown"),
            "PatientName": str(getattr(ds, "PatientName", "Unknown")),
            "PatientBirthDate": getattr(ds, "PatientBirthDate", "Unknown"),
            "PatientSex": getattr(ds, "PatientSex", "Unknown"),
            "StudyDate": getattr(ds, "StudyDate", "Unknown"),
            "StudyTime": getattr(ds, "StudyTime", "Unknown"),
            "StudyDescription": getattr(ds, "StudyDescription", "Unknown"),
            "SeriesDescription": getattr(ds, "SeriesDescription", "Unknown")
        }
        
        # ---- Calculate Pixel Data Offset ----
        # Method 1: Using file positioning
        with open(dicom_path, 'rb') as f:
            try:
                ds_no_pixels = pydicom.dcmread(f, stop_before_pixels=True, force=force)
                pixel_data_offset = f.tell()
                print(f"Pixel Data Offset (header size): {pixel_data_offset} bytes")
            except Exception as e:
                print(f"Warning: Could not determine pixel data offset with stop_before_pixels: {e}")
                # Fall back to manual calculation
                pixel_data_offset = None
        
        # Method 2: Using tag's file_tell attribute if possible
        pixel_data_element = ds.get('PixelData', None)
        pixel_data_tag_offset = None
        
        if pixel_data_element:
            # Get the tag information
            tag_info = ds['PixelData']
            # The offset is available in the tag's file_tell attribute
            if hasattr(tag_info, 'file_tell'):
                pixel_data_tag_offset = tag_info.file_tell
                print(f"Pixel Data Offset from tag: {pixel_data_tag_offset} bytes")
                if pixel_data_offset is not None:
                    print(f"Tag header size: {pixel_data_tag_offset - pixel_data_offset} bytes")
            else:
                print("Warning: No file_tell attribute found in PixelData tag")
        else:
            print("Warning: No PixelData element found in DICOM file")
            result["warnings"] = result.get("warnings", []) + ["No PixelData element found"]
        
        # If both methods failed, we need to add an error
        if pixel_data_offset is None and pixel_data_tag_offset is None:
            result["warnings"] = result.get("warnings", []) + ["Could not determine pixel data offset"]
        
        # Use whichever offset we could determine
        if pixel_data_offset is None and pixel_data_tag_offset is not None:
            pixel_data_offset = pixel_data_tag_offset
        
        # ---- Extract Basic Image Information ----
        pixel_data_info = {
            "pixel_data_offset": pixel_data_offset,
            "pixel_data_tag_offset": pixel_data_tag_offset
        }
        
        # Add pixel data tag info if available
        if pixel_data_element:
            pixel_data_info["pixel_data_tag"] = f"{ds['PixelData'].tag}"
            pixel_data_info["pixel_data_vr"] = ds['PixelData'].VR
        
        # Add image dimension info if available
        if hasattr(ds, 'Rows') and hasattr(ds, 'Columns'):
            pixel_data_info.update({
                "rows": int(ds.Rows),
                "columns": int(ds.Columns),
                "bits_allocated": int(getattr(ds, "BitsAllocated", 0)),
                "bits_stored": int(getattr(ds, "BitsStored", 0)),
                "high_bit": int(getattr(ds, "HighBit", 0)),
                "samples_per_pixel": int(getattr(ds, "SamplesPerPixel", 1)),
                "photometric_interpretation": getattr(ds, "PhotometricInterpretation", "Unknown"),
                "pixel_representation": int(getattr(ds, "PixelRepresentation", 0))  # 0 for unsigned, 1 for signed
            })
            
            # Expected size calculation
            expected_frame_size = ds.Rows * ds.Columns * (getattr(ds, "BitsAllocated", 8) // 8)
            pixel_data_info["expected_frame_size"] = expected_frame_size
        else:
            result["warnings"] = result.get("warnings", []) + ["Missing image dimension information"]
        
        # Add rescale values if available
        if hasattr(ds, 'RescaleIntercept'):
            pixel_data_info["rescale_intercept"] = float(ds.RescaleIntercept)
        
        if hasattr(ds, 'RescaleSlope'):
            pixel_data_info["rescale_slope"] = float(ds.RescaleSlope)
        
        if hasattr(ds, 'PixelSpacing'):
            pixel_data_info["pixel_spacing"] = [float(x) for x in ds.PixelSpacing]
        
        result["pixel_data_info"] = pixel_data_info
        
        # Determine if multi-frame
        is_multiframe = hasattr(ds, 'NumberOfFrames')
        num_frames = 1
        
        if is_multiframe:
            num_frames = int(ds.NumberOfFrames)
            print(f"Multi-frame image with {num_frames} frames")
            if "expected_frame_size" in pixel_data_info:
                expected_total_size = pixel_data_info["expected_frame_size"] * num_frames
                print(f"Expected Total Uncompressed Size: {expected_total_size} bytes")
                pixel_data_info["number_of_frames"] = num_frames
                pixel_data_info["expected_total_size"] = expected_total_size
        else:
            print("Single-frame image")
            pixel_data_info["number_of_frames"] = 1
            if "expected_frame_size" in pixel_data_info:
                pixel_data_info["expected_total_size"] = pixel_data_info["expected_frame_size"]
        
        # Actual size reporting
        if hasattr(ds, 'PixelData'):
            actual_size = len(ds.PixelData)
            pixel_data_info["actual_size"] = actual_size
            print(f"Actual Pixel Data Size: {actual_size} bytes")
            
            # Check for compression
            is_compressed = getattr(ds.file_meta, "TransferSyntaxUID", None).is_compressed if hasattr(ds.file_meta, "TransferSyntaxUID") else False
            if is_compressed and "expected_total_size" in pixel_data_info:
                compression_ratio = pixel_data_info["expected_total_size"] / actual_size
                if compression_ratio < 1:
                    pixel_data_info["expansion_ratio"] = 1/compression_ratio
                    print(f"Expansion Ratio: {1/compression_ratio:.2f}x")
                else:
                    pixel_data_info["compression_ratio"] = compression_ratio
                    print(f"Compression Ratio: {compression_ratio:.2f}x")
            elif "expected_total_size" in pixel_data_info:
                pixel_data_info["compression_ratio"] = 1.0
                print("Uncompressed image (1:1)")
        
        # Verify by reading raw bytes of pixel data start
        if pixel_data_offset is not None:
            try:
                with open(dicom_path, 'rb') as f:
                    f.seek(pixel_data_offset)
                    # Read the first few bytes of pixel data
                    pixel_data_start = f.read(16)
                    pixel_data_info["first_16_bytes_hex"] = pixel_data_start.hex()
                    print(f"First 16 bytes of pixel data: {pixel_data_start.hex()}")
            except Exception as e:
                print(f"Warning: Could not read first 16 bytes of pixel data: {e}")
                result["warnings"] = result.get("warnings", []) + [f"Could not read pixel data bytes: {str(e)}"]
        
        # ---- Frame Offset Analysis ----
        frame_offsets = []
        result["frame_info"] = {
            "is_multiframe": is_multiframe,
            "frame_count": num_frames,
            "frame_offsets": []
        }
        
        # Only continue with frame analysis if we have a valid pixel_data_offset
        if pixel_data_offset is not None:
            # Check if we have the expected_frame_size
            if "expected_frame_size" in pixel_data_info:
                expected_frame_size = pixel_data_info["expected_frame_size"]
                
                # Case 1: Uncompressed data (simple sequential frames)
                is_compressed = getattr(ds.file_meta, "TransferSyntaxUID", None).is_compressed if hasattr(ds.file_meta, "TransferSyntaxUID") else False
                if not is_compressed:
                    print("\nUncompressed image - Frames are stored sequentially")
                    for i in range(num_frames):
                        offset_start = i * expected_frame_size
                        offset_end = (i + 1) * expected_frame_size - 1  # End offset is start of next frame - 1
                        frame_offsets.append((offset_start, offset_end))
                        
                        # Get first 16 bytes of this frame
                        frame_start_bytes = None
                        frame_end_bytes = None
                        try:
                            with open(dicom_path, 'rb') as f:
                                # Read first 16 bytes
                                f.seek(pixel_data_offset + offset_start)
                                frame_start_bytes = f.read(16).hex()
                                
                                # Read last 16 bytes - make sure we don't read past the frame end
                                f.seek(pixel_data_offset + offset_end - 15)  # 15 instead of 16 to include the last byte
                                frame_end_bytes = f.read(16).hex()
                        except Exception as e:
                            frame_start_bytes = f"Error reading frame bytes: {str(e)}"
                            frame_end_bytes = f"Error reading frame bytes: {str(e)}"
                        
                        frame_entry = {
                            "frame_number": i,
                            "offset_from_pixel_data_start": offset_start,  # Relative to start of pixel data content
                            "offset_from_pixel_data_end": offset_end,  # End of this frame relative to pixel data start
                            "absolute_offset_start": pixel_data_offset + offset_start,  # Position in file
                            "absolute_offset_end": pixel_data_offset + offset_end,  # End position in file
                            "frame_size": expected_frame_size,  # Size in bytes
                            "offset_type": "calculated_sequential",
                            "first_16_bytes_hex": frame_start_bytes,
                            "last_16_bytes_hex": frame_end_bytes
                        }
                        result["frame_info"]["frame_offsets"].append(frame_entry)
                        print(f"Frame {i}: Start {offset_start}, End {offset_end} (Size: {expected_frame_size} bytes)")
                
                # Case 2: Compressed data (need to analyze encapsulation)
                else:
                    print("\nCompressed image - Analyzing frame offsets")
                    result["frame_info"]["compression_type"] = getattr(ds.file_meta, "TransferSyntaxUID", "Unknown").name if hasattr(ds.file_meta, "TransferSyntaxUID") else "Unknown"
                    
                    # Check for Basic Offset Table
                    bot_offsets = []
                    basic_offset_table_size = 0
                    has_basic_offset_table = False
                    
                    if hasattr(ds.PixelData, 'is_undefined_length') and ds.PixelData.is_undefined_length:
                        try:
                            # Try to get offsets from the Basic Offset Table
                            from pydicom.encaps import get_frame_offsets
                            offsets = get_frame_offsets(ds.PixelData)
                            has_basic_offset_table = len(offsets) > 0
                            result["frame_info"]["has_basic_offset_table"] = has_basic_offset_table
                            
                            if has_basic_offset_table:
                                bot_offsets = offsets
                                # Estimate BOT size: 8 bytes for Item tag + length, then 4 bytes per offset
                                basic_offset_table_size = 8 + (len(bot_offsets) * 4)
                                result["frame_info"]["basic_offset_table_size"] = basic_offset_table_size
                                
                                print("\nBasic Offset Table entries:")
                                
                                # Calculate frame sizes based on difference between offsets
                                for i, offset in enumerate(bot_offsets):
                                    # Start offset is the current offset
                                    offset_start = offset
                                    
                                    # End offset is either next frame's start - 1, or if it's the last frame
                                    # we estimate based on total data size
                                    if i < len(bot_offsets) - 1:
                                        offset_end = bot_offsets[i+1] - 1
                                        frame_size = bot_offsets[i+1] - offset
                                    else:
                                        # For the last frame, we use the actual data size minus offsets
                                        # This is an estimate and may include sequence delimiters
                                        if hasattr(ds, 'PixelData'):
                                            # Subtract BOT size and current offset
                                            frame_size = len(ds.PixelData) - basic_offset_table_size - offset
                                            offset_end = offset + frame_size - 1
                                        else:
                                            frame_size = None
                                            offset_end = None
                                    
                                    # Calculate the actual file position
                                    absolute_offset_start = pixel_data_offset + basic_offset_table_size + offset_start
                                    absolute_offset_end = None if offset_end is None else pixel_data_offset + basic_offset_table_size + offset_end
                                    
                                    # Get first 16 bytes of this frame
                                    frame_start_bytes = None
                                    frame_end_bytes = None
                                    try:
                                        with open(dicom_path, 'rb') as f:
                                            # Read first 16 bytes
                                            f.seek(absolute_offset_start)
                                            frame_start_bytes = f.read(16).hex()
                                            
                                            # Read last 16 bytes if we know the end position
                                            if absolute_offset_end is not None:
                                                # Make sure we don't read past the frame end
                                                f.seek(absolute_offset_end - 15)  # Position to read last 16 bytes
                                                frame_end_bytes = f.read(16).hex()
                                    except Exception as e:
                                        frame_start_bytes = f"Error reading frame bytes: {str(e)}"
                                        frame_end_bytes = f"Error reading frame bytes: {str(e)}"
                                    
                                    frame_entry = {
                                        "frame_number": i,
                                        "offset_from_pixel_data_start": basic_offset_table_size + offset_start,
                                        "offset_from_pixel_data_end": None if offset_end is None else basic_offset_table_size + offset_end,
                                        "offset_from_first_frame": offset_start,  # This is relative to first frame fragment
                                        "absolute_offset_start": absolute_offset_start,  # Absolute file position
                                        "absolute_offset_end": absolute_offset_end,  # End position in file
                                        "frame_size": frame_size,
                                        "offset_type": "basic_offset_table",
                                        "first_16_bytes_hex": frame_start_bytes,
                                        "last_16_bytes_hex": frame_end_bytes
                                    }
                                    result["frame_info"]["frame_offsets"].append(frame_entry)
                                    print(f"Frame {i}: Start {offset_start}, End {offset_end if offset_end is not None else 'unknown'} (Size: {frame_size if frame_size is not None else 'unknown'} bytes)")
                                
                                frame_offsets = bot_offsets
                                
                        except Exception as e:
                            print(f"Error extracting Basic Offset Table: {e}")
                            result["frame_info"]["bot_error"] = str(e)
                    else:
                        result["frame_info"]["has_basic_offset_table"] = False
                    
                    # If BOT didn't work or doesn't exist, try direct analysis
                    if not frame_offsets and hasattr(ds.file_meta, "TransferSyntaxUID") and ds.file_meta.TransferSyntaxUID == '1.2.840.10008.1.2.4.80':  # JPEG-LS
                        print("\nAnalyzing JPEG-LS markers for frame detection:")
                        result["frame_info"]["marker_analysis"] = "JPEG-LS"
                        
                        # Get pixel data as bytes
                        pixel_data_bytes = ds.PixelData
                        
                        # For JPEG-LS, frames are typically separated by JPEG markers
                        # Common JPEG-LS frame start: FF F7 (Start of Scan)
                        frame_starts = []
                        pos = 0
                        
                        # Handle BOT if present
                        bot_size = 0
                        if has_basic_offset_table:
                            bot_size = basic_offset_table_size
                        else:
                            # Try to detect and skip the Basic Offset Table
                            if hasattr(ds.PixelData, 'is_undefined_length') and ds.PixelData.is_undefined_length:
                                # Find the first item tag which is typically the BOT
                                while pos < len(pixel_data_bytes) - 3:
                                    if (pixel_data_bytes[pos] == 0xFE and pixel_data_bytes[pos+1] == 0xFF and 
                                        pixel_data_bytes[pos+2] == 0x00 and pixel_data_bytes[pos+3] == 0xE0):
                                        # Get the length from the next 4 bytes (little endian)
                                        length_bytes = pixel_data_bytes[pos+4:pos+8]
                                        length = int.from_bytes(length_bytes, byteorder='little')
                                        bot_size = 8 + length  # 8 bytes for tag + length, then the length itself
                                        pos += bot_size
                                        break
                                    pos += 1
                        
                        # Record BOT detection results
                        result["frame_info"]["detected_bot_size"] = bot_size
                        
                        # Search for FF F7 markers (JPEG-LS Start of Scan)
                        start_pos = pos
                        while pos < len(pixel_data_bytes) - 1:
                            if pixel_data_bytes[pos] == 0xFF and pixel_data_bytes[pos+1] == 0xF7:
                                frame_starts.append(pos - start_pos)  # Store offset relative to first frame
                                pos += 2  # Skip past the marker
                            else:
                                pos += 1
                        
                        if frame_starts:
                            for i, offset in enumerate(frame_starts):
                                # Calculate absolute file position: pixel_data_offset + bot_size + relative_offset
                                absolute_offset_start = pixel_data_offset + bot_size + offset
                                
                                # Calculate end offset and frame size
                                if i < len(frame_starts) - 1:
                                    # End is the start of next frame - 1
                                    offset_end = frame_starts[i+1] - 1
                                    frame_size = frame_starts[i+1] - offset
                                else:
                                    # For last frame, end is end of pixel data
                                    if hasattr(ds, 'PixelData'):
                                        frame_size = len(pixel_data_bytes) - bot_size - offset
                                        offset_end = offset + frame_size - 1
                                    else:
                                        frame_size = None
                                        offset_end = None
                                
                                absolute_offset_end = None if offset_end is None else pixel_data_offset + bot_size + offset_end
                                
                                # Get first 16 bytes of this frame
                                frame_start_bytes = None
                                frame_end_bytes = None
                                try:
                                    with open(dicom_path, 'rb') as f:
                                        # Read first 16 bytes
                                        f.seek(absolute_offset_start)
                                        frame_start_bytes = f.read(16).hex()
                                        
                                        # Read last 16 bytes if we know the end position
                                        if absolute_offset_end is not None:
                                            # Make sure we don't read past the frame end
                                            f.seek(absolute_offset_end - 15)  # Position to read last 16 bytes
                                            frame_end_bytes = f.read(16).hex()
                                except Exception as e:
                                    frame_start_bytes = f"Error reading frame bytes: {str(e)}"
                                    frame_end_bytes = f"Error reading frame bytes: {str(e)}"
                                
                                frame_entry = {
                                    "frame_number": i,
                                    "offset_from_pixel_data_start": bot_size + offset,  # From start of pixel data element
                                    "offset_from_pixel_data_end": None if offset_end is None else bot_size + offset_end,
                                    "offset_from_first_frame": offset,  # From start of first frame (after BOT)
                                    "absolute_offset_start": absolute_offset_start,  # Actual file start position
                                    "absolute_offset_end": absolute_offset_end,  # Actual file end position
                                    "frame_size": frame_size,
                                    "offset_type": "jpeg_ls_marker",
                                    "first_16_bytes_hex": frame_start_bytes,
                                    "last_16_bytes_hex": frame_end_bytes
                                }
                                result["frame_info"]["frame_offsets"].append(frame_entry)
                                print(f"Frame {i}: Start {offset}, End {offset_end if offset_end is not None else 'unknown'} (Size: {frame_size if frame_size is not None else 'unknown'} bytes)")
                            
                            frame_offsets = frame_starts
                    # for JPEG 2000
                    elif not frame_offsets and hasattr(ds.file_meta, "TransferSyntaxUID") and ds.file_meta.TransferSyntaxUID in ['1.2.840.10008.1.2.4.90', '1.2.840.10008.1.2.4.91']:  # JPEG 2000
                        print("\nAnalyzing JPEG 2000 markers for frame detection:")
                        result["frame_info"]["marker_analysis"] = "JPEG 2000"
                        
                        # Get pixel data as bytes
                        pixel_data_bytes = ds.PixelData
                        
                        # For JPEG 2000, frames typically start with FF 4F (SOC - Start of Codestream)
                        frame_starts = []
                        pos = 0
                        
                        # Handle BOT if present
                        bot_size = 0
                        if has_basic_offset_table:
                            bot_size = basic_offset_table_size
                        else:
                            # Try to detect and skip the Basic Offset Table
                            if hasattr(ds.PixelData, 'is_undefined_length') and ds.PixelData.is_undefined_length:
                                # Find the first item tag which is typically the BOT
                                while pos < len(pixel_data_bytes) - 3:
                                    if (pixel_data_bytes[pos] == 0xFE and pixel_data_bytes[pos+1] == 0xFF and 
                                        pixel_data_bytes[pos+2] == 0x00 and pixel_data_bytes[pos+3] == 0xE0):
                                        # Get the length from the next 4 bytes (little endian)
                                        length_bytes = pixel_data_bytes[pos+4:pos+8]
                                        length = int.from_bytes(length_bytes, byteorder='little')
                                        bot_size = 8 + length  # 8 bytes for tag + length, then the length itself
                                        pos += bot_size
                                        break
                                    pos += 1
                        
                        # Record BOT detection results
                        result["frame_info"]["detected_bot_size"] = bot_size
                        
                        # Search for FF 4F markers (JPEG 2000 Start of Codestream)
                        start_pos = pos
                        
                        # DICOM encapsulated pixel data format also has item markers
                        # These are FEFF00E0 followed by a 4-byte length, then the JPEG 2000 data
                        item_starts = []
                        pos = 0
                        
                        # First, find all DICOM items
                        while pos < len(pixel_data_bytes) - 3:
                            if (pixel_data_bytes[pos] == 0xFE and pixel_data_bytes[pos+1] == 0xFF and 
                                pixel_data_bytes[pos+2] == 0x00 and pixel_data_bytes[pos+3] == 0xE0):
                                # Found an item tag
                                item_starts.append(pos)
                                # Get the length and skip past this item
                                length_bytes = pixel_data_bytes[pos+4:pos+8]
                                length = int.from_bytes(length_bytes, byteorder='little')
                                pos += 8 + length  # 8 bytes for tag + length, then the length itself
                            else:
                                pos += 1
                        
                        # Remove the first item if it's the Basic Offset Table
                        if item_starts and len(item_starts) > 1:
                            # Skip first item which is likely the BOT
                            item_starts = item_starts[1:]
                        
                        # Now for each item start, check if there's a JPEG 2000 SOC marker
                        frame_starts = []
                        for item_pos in item_starts:
                            # Each item should have a JPEG 2000 SOC marker (FF 4F) after the item header (8 bytes)
                            data_pos = item_pos + 8
                            
                            # Verify it's a JPEG 2000 frame
                            if data_pos + 1 < len(pixel_data_bytes) and pixel_data_bytes[data_pos] == 0xFF and pixel_data_bytes[data_pos+1] == 0x4F:
                                frame_starts.append(item_pos - start_pos)  # Store offset relative to first frame
                        
                        if frame_starts:
                            for i, offset in enumerate(frame_starts):
                                # Calculate absolute file position: pixel_data_offset + bot_size + relative_offset
                                absolute_offset_start = pixel_data_offset + offset
                                
                                # Calculate end offset and frame size
                                if i < len(frame_starts) - 1:
                                    # End is the start of next frame - 1
                                    offset_end = frame_starts[i+1] - 1
                                    frame_size = frame_starts[i+1] - offset
                                else:
                                    # For last frame, end is end of pixel data
                                    if hasattr(ds, 'PixelData'):
                                        frame_size = len(pixel_data_bytes) - offset
                                        offset_end = offset + frame_size - 1
                                    else:
                                        frame_size = None
                                        offset_end = None
                                
                                absolute_offset_end = None if offset_end is None else pixel_data_offset + offset_end
                                
                                # Get first 16 bytes of this frame
                                frame_start_bytes = None
                                frame_end_bytes = None
                                try:
                                    with open(dicom_path, 'rb') as f:
                                        # Read first 16 bytes
                                        f.seek(absolute_offset_start)
                                        frame_start_bytes = f.read(16).hex()
                                        
                                        # Read last 16 bytes if we know the end position
                                        if absolute_offset_end is not None:
                                            # Make sure we don't read past the frame end
                                            f.seek(absolute_offset_end - 15)  # Position to read last 16 bytes
                                            frame_end_bytes = f.read(16).hex()
                                except Exception as e:
                                    frame_start_bytes = f"Error reading frame bytes: {str(e)}"
                                    frame_end_bytes = f"Error reading frame bytes: {str(e)}"
                                
                                frame_entry = {
                                    "frame_number": i,
                                    "offset_from_pixel_data_start": offset,  # From start of pixel data element
                                    "offset_from_pixel_data_end": None if offset_end is None else offset_end,
                                    "offset_from_first_frame": offset,  # From start of first frame (after BOT)
                                    "absolute_offset_start": absolute_offset_start,  # Actual file start position
                                    "absolute_offset_end": absolute_offset_end,  # Actual file end position
                                    "frame_size": frame_size,
                                    "offset_type": "jpeg2000_marker",
                                    "first_16_bytes_hex": frame_start_bytes,
                                    "last_16_bytes_hex": frame_end_bytes
                                }
                                result["frame_info"]["frame_offsets"].append(frame_entry)
                                print(f"Frame {i}: Start {offset}, End {offset_end if offset_end is not None else 'unknown'} (Size: {frame_size if frame_size is not None else 'unknown'} bytes)")
                            
                            frame_offsets = frame_starts
                    # If no frames detected but we know it's multi-frame, add a note
                    if is_multiframe and num_frames > 1 and not result["frame_info"]["frame_offsets"]:
                        result["frame_info"]["frame_detection_note"] = "Could not automatically detect frame boundaries"
            else:
                result["warnings"] = result.get("warnings", []) + ["Could not calculate frame offsets - missing image dimension info"]
        else:
            result["warnings"] = result.get("warnings", []) + ["Could not determine frame offsets - missing pixel data offset"]
        
        # Add hex editor verification guide
        if pixel_data_offset is not None:
            result["hex_editor_guide"] = {
                "pixel_data_start_offset_decimal": pixel_data_offset,
                "pixel_data_start_offset_hex": f"0x{pixel_data_offset:X}",
                "offset_terminology": {
                    "offset_from_pixel_data_start": "Bytes from start of pixel data element content to beginning of frame",
                    "offset_from_pixel_data_end": "Bytes from start of pixel data element content to end of frame",
                    "absolute_offset_start": "Start of frame as actual file position in bytes from start of file",
                    "absolute_offset_end": "End of frame as actual file position in bytes from start of file",
                    "frame_size": "Size of frame in bytes"
                }
            }
            
            is_compressed = getattr(ds.file_meta, "TransferSyntaxUID", None).is_compressed if hasattr(ds.file_meta, "TransferSyntaxUID") else False
            if is_compressed:
                result["hex_editor_guide"]["pattern_description"] = "Look for encapsulated DICOM data pattern: Item tag (FE FF 00 E0), Length field (4 bytes), then Basic Offset Table or first frame"
                if frame_offsets and len(frame_offsets) > 1:
                    next_frame_info = result["frame_info"]["frame_offsets"][1]
                    result["hex_editor_guide"]["second_frame_offset_decimal"] = next_frame_info["absolute_offset_start"]
                    result["hex_editor_guide"]["second_frame_offset_hex"] = f"0x{next_frame_info['absolute_offset_start']:X}"
            else:
                result["hex_editor_guide"]["pattern_description"] = "For uncompressed data, pixel values start immediately"
                if is_multiframe and num_frames > 1 and "expected_frame_size" in pixel_data_info:
                    next_frame = pixel_data_info["expected_frame_size"]
                    next_frame_pos = pixel_data_offset + next_frame
                    result["hex_editor_guide"]["second_frame_offset_decimal"] = next_frame_pos
                    result["hex_editor_guide"]["second_frame_offset_hex"] = f"0x{next_frame_pos:X}"
        
        # Print success
        print("Analysis completed successfully")
        
    except Exception as e:
        print(f"Error analyzing DICOM file: {e}")
        import traceback
        result["error"] = {
            "message": str(e),
            "traceback": traceback.format_exc()
        }
    
    # If we're part of a batch process, add to results dict
    if results_dict is not None:
        results_dict[os.path.basename(dicom_path)] = result
    
    return result


def analyze_dicom_directory(directory_path, output_json_path=None, force=True):
    """
    Analyze all DICOM files in a directory and save results to JSON
    
    Parameters:
    -----------
    directory_path : str
        Path to directory containing DICOM files
    output_json_path : str, optional
        Path to save JSON results, defaults to 'dicom_analysis_results.json'
    force : bool, optional
        Whether to force reading files with missing DICOM headers (default: True)
    """
    # Check if directory exists
    if not os.path.exists(directory_path):
        print(f"\nDirectory not found: {directory_path}")
        print("Please ensure the directory exists.")
        return None

    # Set default output path if none provided
    if output_json_path is None:
        output_json_path = os.path.join(os.path.dirname(directory_path), 'dicom_analysis_results.json')
    
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)
    
    # Find all potential DICOM files (no extension or .dcm extension)
    dicom_files = []
    for root, _, files in os.walk(directory_path):
        for file in files:
            filepath = os.path.join(root, file)
            _, ext = os.path.splitext(file)
            if ext.lower() == '.dcm' or ext == '':
                dicom_files.append(filepath)
    
    if not dicom_files:
        print(f"\nNo DICOM files found in directory: {directory_path}")
        print("Please ensure the directory contains DICOM files (.dcm extension or no extension)")
        return None
    
    print(f"Found {len(dicom_files)} potential DICOM files")
    
    # Analyze each file
    results = {}
    for i, filepath in enumerate(dicom_files):
        try:
            print(f"\nProcessing file {i+1}/{len(dicom_files)}")
            if not os.path.exists(filepath):
                print(f"File not found: {filepath}")
                continue
            analyze_dicom_offsets(filepath, results, force=force)
        except Exception as e:
            print(f"Error processing {filepath}: {e}")
            import traceback
            results[os.path.basename(filepath)] = {
                "error": {
                    "message": str(e),
                    "traceback": traceback.format_exc()
                }
            }
    
    if not results:
        print("\nNo files were successfully analyzed")
        return None
    
    # Save results to JSON
    try:
        with open(output_json_path, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nAnalysis complete. Results saved to {output_json_path}")
        return output_json_path
    except Exception as e:
        print(f"\nError saving results to {output_json_path}: {e}")
        return None

if __name__ == "__main__":
    # Create necessary directories if they don't exist
    os.makedirs("Data", exist_ok=True)
    os.makedirs("JSON", exist_ok=True)
    os.makedirs(os.path.join("Data", "SPIN"), exist_ok=True)

    # Test with multi-frame - from SPIN
    multi_frame_path = os.path.join("Data", "SPIN", "1.2.250.1.90.2.1211619309.20250228095743.9948.90256.dcm")
    if os.path.exists(multi_frame_path):
        print("\n===== ANALYZING MULTI-FRAME IMAGE =====")
        result = analyze_dicom_offsets(multi_frame_path)
        
        # Save single file result to JSON
        output_path = os.path.join("JSON", f"{os.path.basename(multi_frame_path)}_analysis.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to: {output_path}")
    else:
        print(f"\nFile not found: {multi_frame_path}")
        print("Please ensure the DICOM file exists in the specified location.")

    # Test with multi-frame - from DX
    multi_frame_path = os.path.join("Data", "DX000000.dcm")
    if os.path.exists(multi_frame_path):
        print("\n===== ANALYZING MULTI-FRAME IMAGE =====")
        result = analyze_dicom_offsets(multi_frame_path)
        
        # Save single file result to JSON
        output_path = os.path.join("JSON", f"{os.path.basename(multi_frame_path)}_analysis.json")
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        print(f"Results saved to: {output_path}")

    else:
        print(f"\nFile not found: {multi_frame_path}")
        print("Please ensure the DICOM file exists in the specified location.")


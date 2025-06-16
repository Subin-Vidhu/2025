# -*- coding: utf-8 -*-
"""
Created on Wed Jun  4 13:41:05 2025

@author: Subin-PC
"""

import os
import numpy as np
import nibabel as nib
import matplotlib.pyplot as plt
import random
from pathlib import Path

def load_nifti_data(file_path):
    """Load NIfTI file and return data array"""
    try:
        nii = nib.load(file_path)
        data = nii.get_fdata()
        return data
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return None

def find_slices_with_values(mask_data, threshold=0.1):
    """Find slices that contain segmentation values"""
    valid_slices = []
    for i in range(mask_data.shape[2]):  # Assuming axial slices
        slice_data = mask_data[:, :, i]
        if np.sum(slice_data > threshold) > 0:  # Has segmentation
            valid_slices.append(i)
    return valid_slices

def apply_ct_windowing(image, window_min=-135, window_max=215):
    """Apply CT windowing to enhance kidney visibility"""
    windowed_image = np.clip(image, window_min, window_max)
    # Normalize to 0-1 range for better display
    windowed_image = (windowed_image - window_min) / (window_max - window_min)
    return windowed_image

# Removed overlay function as we're now using separate plots

def rotate_image(image, rotation_angle=0):
    """Rotate image by specified angle (0, 90, 180, 270 degrees)"""
    if rotation_angle == 90:
        return np.rot90(image, k=1)
    elif rotation_angle == 180:
        return np.rot90(image, k=2)
    elif rotation_angle == 270:
        return np.rot90(image, k=3)
    else:
        return image

def visualize_case(case_folder, case_name, num_slices=5, rotation_angle=270, save_path=None):
    """Visualize random slices from a single case with separate image and mask plots"""
    img_path = os.path.join(case_folder, 'img.nii')
    mask_path = os.path.join(case_folder, 'mask.nii')
    
    # Check if files exist
    if not (os.path.exists(img_path) and os.path.exists(mask_path)):
        print(f"Missing files in {case_name}")
        return
    
    # Load data
    img_data = load_nifti_data(img_path)
    mask_data = load_nifti_data(mask_path)
    
    if img_data is None or mask_data is None:
        print(f"Failed to load data for {case_name}")
        return
    
    print(f"Processing {case_name} - Image shape: {img_data.shape}, Mask shape: {mask_data.shape}")
    
    # Find slices with segmentation
    valid_slices = find_slices_with_values(mask_data)
    
    if len(valid_slices) == 0:
        print(f"No valid slices found for {case_name}")
        return
    
    # Select random slices
    selected_slices = random.sample(valid_slices, min(num_slices, len(valid_slices)))
    selected_slices.sort()
    
    # Create subplot with 2 rows: top for images, bottom for masks
    fig, axes = plt.subplots(2, len(selected_slices), figsize=(3*len(selected_slices), 6))
    if len(selected_slices) == 1:
        axes = axes.reshape(2, 1)
    
    fig.suptitle(f'{case_name}', fontsize=16, fontweight='bold')
    
    for idx, slice_num in enumerate(selected_slices):
        img_slice = img_data[:, :, slice_num]
        mask_slice = mask_data[:, :, slice_num]
        
        # Apply rotation if specified
        if rotation_angle != 0:
            img_slice = rotate_image(img_slice, rotation_angle)
            mask_slice = rotate_image(mask_slice, rotation_angle)
        
        # Apply CT windowing for better kidney visualization
        img_slice_windowed = apply_ct_windowing(img_slice)
        
        # Original image with CT windowing (top row)
        axes[0, idx].imshow(img_slice_windowed, cmap='gray', origin='lower')
        axes[0, idx].set_title(f'Slice {slice_num}')
        axes[0, idx].axis('off')
        
        # Mask (bottom row)
        axes[1, idx].imshow(mask_slice, cmap='jet', origin='lower')
        axes[1, idx].set_title(f'Mask Slice {slice_num}')
        axes[1, idx].axis('off')
    
    # Add rotation info to title if applied
    title = f'{case_name}'
    if rotation_angle != 0:
        title += f' (Rotated {rotation_angle}°)'
    fig.suptitle(title, fontsize=16, fontweight='bold')
    
    plt.tight_layout()
    
    # Save plot if save_path is provided
    if save_path:
        os.makedirs(save_path, exist_ok=True)
        filename = f"{case_name}_rotation_{rotation_angle}.png"
        filepath = os.path.join(save_path, filename)
        plt.savefig(filepath, dpi=300, bbox_inches='tight')
        print(f"Saved plot: {filepath}")
    
    plt.show()

def main(dataset_path, max_cases=None, rotation_angle=270, save_path=None):
    """Main function to process all cases"""
    dataset_path = Path(dataset_path)
    
    if not dataset_path.exists():
        print(f"Dataset path {dataset_path} does not exist!")
        return
    
    # Get all case folders
    case_folders = [f for f in dataset_path.iterdir() if f.is_dir()]
    case_folders.sort()
    
    if max_cases and max_cases != -1:
        case_folders = case_folders[:max_cases]
    
    print(f"Found {len(case_folders)} cases")
    if max_cases == -1 or max_cases is None:
        print("Processing ALL cases in the dataset")
    else:
        print(f"Processing first {max_cases} cases")
    if rotation_angle != 0:
        print(f"Applying {rotation_angle}° rotation to all images")
    if save_path:
        print(f"Plots will be saved to: {save_path}")
    
    # Set random seed for reproducibility
    random.seed(42)
    
    # Process each case
    for case_folder in case_folders:
        case_name = case_folder.name
        try:
            visualize_case(str(case_folder), case_name, rotation_angle=rotation_angle, save_path=save_path)
        except Exception as e:
            print(f"Error processing {case_name}: {e}")
            continue

# Usage example:
if __name__ == "__main__":
    # Update this path to your dataset location
    dataset_path = "E:/AIRA/ARAMIS_RENAL_FULL_DATASET"
    
    # Set save path for plots
    save_folder = "E:/AIRA/kidney_visualization_plots"
    
    # Process ALL cases with default settings (270° rotation, CT windowing, save plots)
    main(dataset_path, max_cases=-1, rotation_angle=270, save_path=save_folder)
    
    # Alternative usage options:
    # Process first 10 cases only
    # main(dataset_path, max_cases=10, rotation_angle=270, save_path=save_folder)
    
    # Process all cases without saving (just display)
    # main(dataset_path, max_cases=-1, rotation_angle=270)
    
    # Test different rotations on a few cases first:
    # main(dataset_path, max_cases=3, rotation_angle=0, save_path=save_folder)    # Original
    # main(dataset_path, max_cases=3, rotation_angle=90, save_path=save_folder)   # Rotate left
    # main(dataset_path, max_cases=3, rotation_angle=180, save_path=save_folder)  # Rotate 180°
    
    # Or visualize a single case
    # single_case_path = "path/to/your/ARAMIS_RENAL_FULL_DATASET/N001"
    # visualize_case(single_case_path, "N001", rotation_angle=270, save_path=save_folder)
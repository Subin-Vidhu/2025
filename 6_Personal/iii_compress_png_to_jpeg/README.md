# PNG to JPEG Compression Tool

A Python script that efficiently converts PNG images to JPEG format while maintaining quality and reducing file size. The script automatically adjusts compression quality to keep files under a specified size limit (default: 2MB).

## Features

- **Batch Processing**: Converts multiple PNG files in a folder simultaneously
- **Smart Compression**: Automatically adjusts JPEG quality to meet target file size
- **Alpha Channel Handling**: Properly handles PNG transparency by converting to white background
- **Size Optimization**: Ensures output files stay under 2MB (configurable)
- **Progress Feedback**: Shows compression results for each file

## Requirements

- Python 3.6+
- Pillow (PIL) library

## Installation

1. Install the required dependency:
```bash
pip install Pillow
```

## Usage

### Basic Usage

1. Update the folder paths in `main.py`:
   ```python
   input_folder = "path/to/your/png/files"
   output_folder = "path/to/output/jpeg/files"
   ```

2. Run the script:
   ```bash
   python main.py
   ```

### Configuration Options

You can modify these parameters in the script:

- **Target Size**: Change `target_size` parameter (default: 2MB)
  ```python
  compress_to_jpeg(input_path, output_path, target_size=1 * 1024 * 1024)  # 1MB
  ```

- **Starting Quality**: Modify the initial `quality` value (default: 95)
  ```python
  quality = 85  # Start with lower quality for smaller files
  ```

- **Quality Step**: Adjust how much quality is reduced each iteration (default: 5)
  ```python
  quality -= 10  # Larger steps for faster compression
  ```

## How It Works

1. **Image Loading**: Opens each PNG file using PIL
2. **Alpha Channel Removal**: Converts RGBA/LA images to RGB with white background
3. **Iterative Compression**: 
   - Starts with high quality (95%)
   - Reduces quality by 5% increments
   - Stops when file size is under target or quality reaches 10%
4. **Progress Reporting**: Shows final file size and quality used

## Output Format

The script provides feedback for each processed file:

- ✅ **Success**: `filename.png compressed to 1.23 MB (quality=85)`
- ⚠️ **Warning**: `filename.png still above 2MB even at quality=10`

## File Structure

```
input_folder/
├── image1.png
├── image2.png
└── image3.png

output_folder/
├── image1.jpg
├── image2.jpg
└── image3.jpg
```

## Technical Details

### Image Processing Pipeline

1. **Color Mode Conversion**:
   - RGBA → RGB (with white background)
   - LA → RGB (with white background)
   - Other modes → RGB

2. **Compression Algorithm**:
   - Uses JPEG format with variable quality
   - Quality range: 95% down to 10%
   - 5% quality reduction per iteration

3. **Size Validation**:
   - Checks file size after each compression attempt
   - Stops when target size is achieved

### Supported Formats

- **Input**: PNG files (any color mode)
- **Output**: JPEG files (RGB only)

## Error Handling

The script includes basic error handling for:
- Missing input directories
- Unsupported file formats
- File access permissions

## Performance Considerations

- **Memory Usage**: Images are processed one at a time to minimize memory usage
- **Speed**: Quality reduction in 5% steps balances speed vs. precision
- **File Size**: 2MB target size works well for most web and document uses

## Customization Examples

### For Web Optimization (smaller files)
```python
target_size = 500 * 1024  # 500KB
quality = 80  # Start lower
```

### For Print Quality (larger files)
```python
target_size = 5 * 1024 * 1024  # 5MB
quality = 98  # Start higher
```

### For Faster Processing
```python
quality -= 10  # Bigger quality steps
```

## Troubleshooting

### Common Issues

1. **"File not found" error**: Check that input folder path is correct
2. **Permission denied**: Ensure write access to output folder
3. **Large files still over limit**: Some images may need manual quality adjustment

### Tips

- Use absolute paths to avoid directory issues
- Test with a few files first before batch processing
- Check available disk space in output directory

## License

This script is provided as-is for educational and personal use.

## Author

Created for efficient PNG to JPEG batch conversion with size optimization.
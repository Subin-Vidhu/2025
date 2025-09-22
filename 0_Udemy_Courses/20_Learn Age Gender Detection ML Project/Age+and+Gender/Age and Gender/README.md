# Age and Gender Detection using Deep Neural Networks and OpenCV

This project implements real-time age and gender detection using pre-trained deep neural network models with OpenCV's DNN module. The system can detect faces in images or video streams and predict the age group and gender of detected persons.

## 📋 Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Model Architecture](#model-architecture)
- [Technical Details](#technical-details)
- [Sample Results](#sample-results)
- [Troubleshooting](#troubleshooting)
- [Course Information](#course-information)

## 🎯 Overview

This project demonstrates computer vision techniques for demographic analysis using deep learning. It combines three pre-trained models:
1. **Face Detection**: Uses OpenCV's DNN face detector
2. **Age Classification**: Predicts age groups using a Caffe model
3. **Gender Classification**: Determines gender using a separate Caffe model

## ✨ Features

- **Real-time Processing**: Works with webcam feed or static images
- **Multi-face Detection**: Can detect and analyze multiple faces simultaneously
- **Age Group Classification**: Classifies age into 8 different groups
- **Gender Detection**: Binary classification (Male/Female)
- **Visual Feedback**: Draws bounding boxes and displays predictions on faces
- **Flexible Input**: Supports both image files and live video stream

## 📁 Project Structure

```
Age and Gender/
├── Age.py                          # Main application script
├── opencv_face_detector.pbtxt      # Face detection model configuration
├── opencv_face_detector_uint8.pb   # Pre-trained face detection model (2.7MB)
├── age_deploy.prototxt            # Age classification model architecture
├── age_net.caffemodel             # Pre-trained age classification model (45.7MB)
├── gender_deploy.prototxt         # Gender classification model architecture
├── gender_net.caffemodel          # Pre-trained gender classification model (45.6MB)
├── d.jpg                          # Sample test image
├── e.jpg                          # Sample test image
└── README.md                      # This documentation
```

## 🛠 Prerequisites

- Python 3.6 or higher
- OpenCV with DNN module support
- NumPy
- A webcam (for live detection) or sample images

## 💻 Installation

1. **Clone or download this project**
   ```bash
   # Navigate to the project directory
   cd "Age and Gender"
   ```

2. **Install required dependencies**
   ```bash
   pip install opencv-python
   pip install numpy
   ```

   Alternative installation:
   ```bash
   pip install opencv-contrib-python
   ```

3. **Verify OpenCV installation**
   ```python
   import cv2
   print(cv2.__version__)
   print(cv2.dnn.getAvailableBackends())
   ```

## 🚀 Usage

### For Live Webcam Detection
```bash
python Age.py
```

### For Image File Detection
```bash
python Age.py --image path/to/your/image.jpg
```

### Example Commands
```bash
# Using sample images provided
python Age.py --image d.jpg
python Age.py --image e.jpg

# Using your own image
python Age.py --image "C:\path\to\your\photo.jpg"
```

### Controls
- **ESC key**: Exit the application
- **Any other key**: Continue to next frame (in image mode)

## 🏗 Model Architecture

### Face Detection Model
- **Type**: TensorFlow frozen graph
- **Input Size**: 300x300x3
- **Architecture**: SSD MobileNet-based detector
- **Confidence Threshold**: 0.7 (adjustable)

### Age Classification Model
- **Type**: Caffe CNN model
- **Input Size**: 227x227x3
- **Architecture**: CaffeNet-style CNN
- **Output Classes**: 8 age groups
  - (0-2), (4-6), (8-12), (15-20), (25-32), (38-43), (48-53), (60-100)

### Gender Classification Model
- **Type**: Caffe CNN model  
- **Input Size**: 227x227x3
- **Architecture**: CaffeNet-style CNN
- **Output Classes**: 2 genders (Male, Female)

## 🔧 Technical Details

### Key Parameters
```python
MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
conf_threshold = 0.7  # Face detection confidence
padding = 20          # Face crop padding
```

### Processing Pipeline
1. **Frame Capture**: Read frame from video source
2. **Face Detection**: Use DNN face detector to locate faces
3. **Face Extraction**: Crop face regions with padding
4. **Preprocessing**: Resize and normalize face crops
5. **Age Prediction**: Feed to age classification model
6. **Gender Prediction**: Feed to gender classification model  
7. **Visualization**: Draw results on original frame

### Color Coding
- **Face Boxes**: Green rectangles around detected faces
- **Text Labels**: Yellow text showing "Gender, Age" predictions
- **Font**: FONT_HERSHEY_SIMPLEX with thickness 2

## 📸 Sample Results

The system provides predictions in the format:
```
Gender: Male
Age: 25-32 years
Display: "Male, (25)"
```

Expected accuracy ranges:
- **Face Detection**: ~95% for well-lit frontal faces
- **Gender Classification**: ~85-90% accuracy
- **Age Classification**: ~70-80% accuracy (challenging task)

## 🔍 Troubleshooting

### Common Issues and Solutions

1. **"No face detected" message**
   - Ensure good lighting conditions
   - Face should be clearly visible and frontal
   - Adjust `conf_threshold` parameter (lower value = more sensitive)

2. **OpenCV DNN module not found**
   ```bash
   pip uninstall opencv-python
   pip install opencv-contrib-python
   ```

3. **Model files not loading**
   - Verify all model files are in the same directory as Age.py
   - Check file permissions and paths
   - Ensure model files are not corrupted

4. **Poor accuracy results**
   - Ensure faces are well-lit and clearly visible
   - Age detection is inherently challenging, especially for certain age ranges
   - Results improve with higher quality input images

5. **Webcam not accessible**
   - Check if webcam is being used by another application
   - Try changing camera index: `cv2.VideoCapture(1)` instead of `cv2.VideoCapture(0)`

### Performance Optimization
- **GPU Acceleration**: Use `net.setPreferableBackend(cv2.dnn.DNN_BACKEND_CUDA)` if CUDA is available
- **Input Resolution**: Lower resolution images process faster but may reduce accuracy
- **Batch Processing**: Process multiple faces in batches for better efficiency

## 📚 Course Information

This project is part of the Udemy course: **"Learn Age Gender Detection ML Project"**
- **Course Link**: [Complete Age Gender Detection Using DNN & OpenCV Project](https://www.udemy.com/course/complete-age-gender-detection-using-dnn-opencv-project/)
- **Instructor**: Course instructor information available in course materials
- **Project Complexity**: Beginner to Intermediate level

## 🤝 Contributing

Feel free to contribute to this project by:
- Adding support for more age ranges
- Implementing emotion detection
- Adding batch processing capabilities
- Improving accuracy through ensemble methods
- Adding GUI interface

## 📄 License

This project is for educational purposes. Model files are used under their respective licenses.

## 🙏 Acknowledgments

- OpenCV team for the DNN module
- Caffe framework developers
- Original model creators and researchers
- Course instructors and educational content creators

---

**Note**: This is an educational project. For production use, consider more robust error handling, model validation, and performance optimization techniques.

# Complete Face Recognition, Age, Gender, and Emotion System

This Python application implements a comprehensive facial analysis system using the DeepFace library and OpenCV. The system can detect faces, recognize individuals, and analyze age, gender, and emotions in real-time.

## Course Information
- **Course Link**: [Complete Facial Recognition System Using Deep Face Model](https://www.udemy.com/course/complete-facial-recognition-system-using-deep-face-model/)
- **Reference**: [Face Detection Using Cascade Classifier - GeeksforGeeks](https://www.geeksforgeeks.org/python/face-detection-using-cascade-classifier-using-opencv-python/)

## Features

- **Face Dataset Creation**: Capture and store face images for training
- **Face Recognition**: Identify known individuals using facial embeddings
- **Age Estimation**: Predict the approximate age of detected faces
- **Gender Detection**: Classify gender (male/female) of detected faces
- **Emotion Recognition**: Detect emotions (happy, sad, angry, surprise, fear, disgust, neutral)
- **Real-time Processing**: Live camera feed with instant analysis

## Requirements

### Dependencies
```bash
pip install opencv-python
pip install deepface
pip install numpy
```

### System Requirements
- Python 3.6 or higher
- Webcam/Camera for face capture and recognition
- Sufficient disk space for storing face datasets

## Installation

1. Clone or download the project files
2. Install the required dependencies:
   ```bash
   pip install opencv-python deepface numpy
   ```
3. Ensure your camera is properly connected and accessible

## Usage

Run the application using:
```bash
python recog.py
```

The system will present a menu with three options:

### 1. Create Face Dataset
- **Purpose**: Capture face images for training the recognition system
- **Process**: 
  - Enter the name of the person
  - Position your face in front of the camera
  - The system will automatically detect and capture 100 face images
  - Images are stored in `Dataset/{person_name}/` directory
  - Press 'q' to quit early if needed

### 2. Train Face Dataset
- **Purpose**: Process captured images to create facial embeddings
- **Process**:
  - Scans all person folders in the Dataset directory
  - Generates facial embeddings using FaceNet model
  - Saves embeddings to `file_embedding.npy` for later use
  - Handles errors gracefully for corrupted or unclear images

### 3. Recognize Faces
- **Purpose**: Real-time face recognition with analysis
- **Features**:
  - Detects faces in live camera feed
  - Identifies known persons with similarity scores
  - Displays age estimation
  - Shows gender classification
  - Indicates dominant emotion
  - Unknown faces are labeled as "Unknown"
- **Controls**: Press 'q' to quit

## Technical Details

### Face Detection
- Uses OpenCV's Haar Cascade classifier for face detection
- Configuration: `scaleFactor=1.3, minNeighbors=5`

### Face Recognition
- Utilizes DeepFace library with FaceNet model
- Calculates cosine similarity between face embeddings
- Similarity threshold: 0.7 (adjustable)
- Higher similarity scores indicate better matches

### Analysis Models
- **Age**: Deep learning regression model
- **Gender**: Binary classification (male/female)
- **Emotion**: Multi-class classification (7 emotions)

## File Structure
```
├── recog.py                 # Main application file
├── README.md               # This documentation
├── Dataset/                # Auto-created directory for face images
│   ├── person1/           # Individual person folders
│   │   ├── person1_1.jpg  # Captured face images
│   │   ├── person1_2.jpg
│   │   └── ...
│   └── person2/
│       └── ...
└── file_embedding.npy     # Trained embeddings (created after training)
```

## Configuration Options

### Adjustable Parameters

1. **Number of training images**: Modify `count >= 100` in `create_dataset()`
2. **Similarity threshold**: Change `max_similarity > 0.7` in `recognize_faces()`
3. **Face detection sensitivity**: Adjust `scaleFactor` and `minNeighbors` parameters

### Model Options
The system uses these DeepFace models:
- **Face Recognition**: FaceNet
- **Age**: Built-in age estimation model
- **Gender**: Built-in gender classification model
- **Emotion**: Built-in emotion recognition model

## Troubleshooting

### Common Issues

1. **Camera not accessible**
   - Ensure camera permissions are granted
   - Check if other applications are using the camera
   - Try changing `cv2.VideoCapture(0)` to `cv2.VideoCapture(1)` for external cameras

2. **Face detection not working**
   - Ensure proper lighting conditions
   - Position face clearly in frame
   - Check camera focus and quality

3. **Recognition accuracy issues**
   - Capture more training images per person
   - Ensure diverse lighting and angles during dataset creation
   - Adjust similarity threshold if needed

4. **Performance issues**
   - DeepFace models are downloaded on first use
   - Ensure stable internet connection for initial setup
   - Processing may be slower on older hardware

### Error Handling
- Failed image training is logged with specific error messages
- Face recognition gracefully handles detection failures
- System continues operation even if individual frames fail

## Performance Notes

- **Initial Setup**: First run may take longer due to model downloads
- **Training Time**: Depends on number of people and images in dataset
- **Recognition Speed**: Real-time on modern hardware, may vary with older systems
- **Memory Usage**: Increases with larger datasets

## How It Works

### Dataset Creation Flow
1. User enters person's name
2. Camera captures live video feed
3. Haar Cascade detects faces in each frame
4. Detected faces are cropped and saved as individual images
5. Process continues until 100 images are captured or user exits

### Training Process
1. System scans all person directories in Dataset folder
2. For each person, loads all their face images
3. DeepFace generates 128-dimensional embeddings using FaceNet
4. Embeddings are stored in a dictionary structure
5. Dictionary is saved as `file_embedding.npy` for later use

### Recognition Process
1. Live camera feed captures frames
2. Faces are detected using Haar Cascade
3. For each detected face:
   - DeepFace analyzes age, gender, and emotion
   - Face embedding is generated
   - Cosine similarity is calculated against all stored embeddings
   - Best match above threshold (0.7) is identified
   - Results are displayed on the frame

## Future Enhancements

Potential improvements for the system:
- Add face verification mode
- Implement database storage for embeddings
- Add confidence scores for age/emotion predictions
- Include face mask detection
- Support for multiple face tracking
- Export recognition results to files
- Add batch processing for images
- Implement face clustering for unknown faces

## License

This project is for educational purposes. Please respect privacy and obtain consent before using facial recognition on others.

## Acknowledgments

- [DeepFace](https://github.com/serengil/deepface) - Lightweight face recognition library
- [OpenCV](https://opencv.org/) - Computer vision library
- Face recognition models and techniques from various research papers
- Udemy course instructor for the comprehensive tutorial

---

**Note**: Always ensure you have proper permissions and comply with privacy laws when using facial recognition systems.

- Certificate of Completion: [Complete Face Recognition System Using Deep Face Model](Face,%20Age,%20Gender,%20Emotion%20Recognition%20Using%20Facenet%20Model.pdf)
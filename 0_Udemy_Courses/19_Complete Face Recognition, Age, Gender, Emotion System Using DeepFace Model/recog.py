import os
import cv2
import numpy as np
from deepface import DeepFace

# CREATE DATASET

dir="Dataset"
os.makedirs(dir,exist_ok=True)


def create_dataset(name):
    # Create folder for person if it doesn't exist
    person = os.path.join(dir, name)
    os.makedirs(person, exist_ok=True)

    # Open camera
    cap = cv2.VideoCapture(0)
    count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Cannot Capture Image")
            break

        # Convert to grayscale
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Load face detector
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml") \
                    .detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            count += 1
            # Crop face
            face_img = frame[y:y+h, x:x+w]
            face_path = os.path.join(person, f"{name}_{count}.jpg")

            # Save face image
            cv2.imwrite(face_path, face_img)

            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        # Show the frame
        cv2.imshow("Capture Face In Camera", frame)

        # Exit if 'q' is pressed or after collecting 100 samples
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        elif count >= 100:  # Capture 100 images
            break

    cap.release()
    cv2.destroyAllWindows()

def train_dataset():
    embedding = {}  

    for i in os.listdir(dir):
        person = os.path.join(dir, i)

        if os.path.isdir(person):
            embedding[i] = []

            for img_name in os.listdir(person):
                img_path = os.path.join(person, img_name)

                try:
                    # Get face embedding using FaceNet
                    emb = DeepFace.represent(
                        img_path,
                        model_name="Facenet",
                        enforce_detection=False
                    )[0]["embedding"]

                    embedding[i].append(emb)

                except Exception as e:
                    print(f"Failed To Train Image {img_name} of {i}: {e}")

    return embedding


def recognize_faces(embeddings):
    cap = cv2.VideoCapture(0)
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml").detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
        
        for (x, y, w, h) in faces:
            face_img = frame[y:y + h, x:x + w]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            
            try:
                analysis = DeepFace.analyze(face_img, actions=["age", "gender", "emotion"], enforce_detection=False)
                
                if isinstance(analysis, list):
                    analysis = analysis[0]
                
                age = analysis["age"]
                gender = analysis["gender"]
                gender = gender if isinstance(gender, str) else max(gender, key=gender.get)
                emotion = max(analysis["emotion"], key=analysis["emotion"].get)
                
                face_embedding = DeepFace.represent(face_img, model_name="Facenet", enforce_detection=False)[0]["embedding"]
                
                match = None
                max_similarity = -1
                
                for person, person_embeddings in embeddings.items():
                    for embed in person_embeddings:
                        similarity = np.dot(face_embedding, embed) / (np.linalg.norm(face_embedding) * np.linalg.norm(embed))
                        if similarity > max_similarity:
                            max_similarity = similarity
                            match = person
                
                if max_similarity > 0.7:
                    label = f"{match} ({max_similarity:.2f})"
                else:
                    label = "Unknown"
                
                display_text = f"{label}, Age: {int(age)}, Gender: {gender}, Emotion: {emotion}"
                cv2.putText(frame, display_text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
                
            except Exception as e:
                print("Face cannot be recognized")
        
        cv2.imshow("Recognize Faces", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()



if __name__ == "__main__":
    print("1.Create Face Dataset\n 2.Train Face Dataset\n 3.Recognize Faces")
    choice = input("Enter Your Choice: ")
    
    if choice == "1":
        name = input("Enter Name Of the person: ")
        create_dataset(name)
    elif choice == "2":
        embedding = train_dataset()
        np.save("file_embedding.npy", embedding)
    elif choice == "3":
        if os.path.exists("file_embedding.npy"):
            embedding = np.load(file="file_embedding.npy", allow_pickle=True).item()
            recognize_faces(embedding)
        else:
            print("No File is found")
    else:
        print("invalid choice")
import cv2
import time
from transformers import pipeline
import numpy as np

class EmotionDetector:
    def __init__(self):
        print("Initializing EmotionDetector...")
        
        # Initialize face detection
        print("Loading face detection model...")
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        
        # Initialize emotion detection
        print("Loading emotion detection model...")
        self.classifier = pipeline(
            "image-classification",
            model="j-hartmann/emotion-english-distilroberta-base",
            top_k=1
        )
    
    def detect_and_predict(self, frame):
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = self.face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Process each face
        for (x, y, w, h) in faces:
            # Extract face ROI
            face_roi = frame[y:y+h, x:x+w]
            
            try:
                # Convert BGR to RGB
                rgb_roi = cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB)
                
                # Get emotion prediction
                prediction = self.classifier(rgb_roi)[0]
                emotion = prediction['label']
                score = prediction['score']
                
                # Draw rectangle around face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                
                # Add text with emotion and confidence
                text = f"{emotion}: {score*100:.1f}%"
                cv2.putText(frame, text, (x, y-10),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                           (0, 255, 0), 2)
                
            except Exception as e:
                print(f"Error processing face: {e}")
                continue
        
        return frame

def main():
    print("Starting emotion detection system...")
    
    # Initialize camera
    print("Initializing camera...")
    cap = cv2.VideoCapture(0)
    
    # Set lower resolution for better performance
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    
    # Initialize detector
    detector = EmotionDetector()
    
    # FPS calculation variables
    fps_start_time = time.time()
    fps_counter = 0
    fps = 0
    frame_skip = 2  # Process every 2nd frame
    
    print("Ready! Press 'q' to quit.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        # Skip frames for better performance
        fps_counter += 1
        if fps_counter % frame_skip != 0:
            cv2.imshow('Emotion Detection', frame)
            continue
        
        # Process frame
        try:
            processed_frame = detector.detect_and_predict(frame)
            
            # Calculate FPS
            if time.time() - fps_start_time > 1:
                fps = fps_counter
                fps_counter = 0
                fps_start_time = time.time()
            
            # Display FPS
            cv2.putText(processed_frame, f"FPS: {fps}", (10, 30),
                       cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # Show frame
            cv2.imshow('Emotion Detection', processed_frame)
            
        except Exception as e:
            print(f"Error processing frame: {e}")
            continue
        
        # Check for quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
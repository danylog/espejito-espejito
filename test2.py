from transformers import AutoImageProcessor, AutoModelForImageClassification
import torch
from PIL import Image
import cv2
import numpy as np
from typing import Union, Dict, List

class FacialEmotionDetector:
    def __init__(self):
        # Load the processor and model
        self.processor = AutoImageProcessor.from_pretrained("prithivMLmods/Facial-Emotion-Detection-SigLIP2")
        self.model = AutoModelForImageClassification.from_pretrained("prithivMLmods/Facial-Emotion-Detection-SigLIP2")
        
        # Define emotion mapping for the model
        self.emotion_mapping = {
            0: 'Ahegao',
            1: 'Angry',
            2: 'Happy',
            3: 'Neutral',
            4: 'Sad',
            5: 'Surprise'
        }
        
        # Load the Haar cascade for face detection
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect_faces(self, image: np.ndarray) -> List[Dict[str, int]]:
        """
        Detect faces in an image using Haar cascades.
        Args:
            image (numpy.ndarray): Input image
        
        Returns:
            List[Dict[str, int]]: List of bounding boxes for detected faces
        """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(48, 48))
        return [{'x': x, 'y': y, 'w': w, 'h': h} for (x, y, w, h) in faces]

    def process_face(self, face_roi: np.ndarray) -> Dict:
        """
        Predict emotions for a cropped face.
        Args:
            face_roi (numpy.ndarray): Cropped image of a face
        
        Returns:
            Dict: Predicted top emotion and scores for all emotions
        """
        # Convert face ROI to PIL Image
        face_pil = Image.fromarray(cv2.cvtColor(face_roi, cv2.COLOR_BGR2RGB))
        
        # Process the image
        inputs = self.processor(images=face_pil, return_tensors="pt")
        
        # Get predictions
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=-1)
        
        # Get the top prediction
        predicted_class = outputs.logits.argmax(-1).item()
        confidence = probs[0][predicted_class].item()
        
        # Map predictions to emotions
        predictions = [
            {'emotion': self.emotion_mapping[i], 'confidence': prob.item()}
            for i, prob in enumerate(probs[0])
        ]
        predictions.sort(key=lambda x: x['confidence'], reverse=True)
        
        return {
            'top_emotion': self.emotion_mapping[predicted_class],
            'confidence': confidence,
            'all_emotions': predictions
        }

    def analyze_image(self, image_path: str) -> List[Dict]:
        """
        Analyze an image for emotions in detected faces.
        Args:
            image_path (str): Path to the input image
        
        Returns:
            List[Dict]: List of emotions detected for each face
        """
        # Load the image
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Could not load image at path: {image_path}")
        
        # Detect faces
        faces = self.detect_faces(image)
        
        # Analyze emotions for each detected face
        results = []
        for face in faces:
            x, y, w, h = face['x'], face['y'], face['w'], face['h']
            face_roi = image[y:y+h, x:x+w]
            emotions = self.process_face(face_roi)
            results.append({
                'face': face,
                'emotions': emotions
            })
        
        return results

# Example usage
if __name__ == "__main__":
    detector = FacialEmotionDetector()
    image_path = "path/to/your/image.jpg"  # Replace with the path to your image
    
    try:
        results = detector.analyze_image(image_path)
        for i, result in enumerate(results):
            print(f"Face {i + 1}:")
            print(f"  Top Emotion: {result['emotions']['top_emotion']} ({result['emotions']['confidence']:.2f})")
            print("  All Emotions:")
            for emotion in result['emotions']['all_emotions']:
                print(f"    - {emotion['emotion']}: {emotion['confidence']:.2f}")
    except Exception as e:
        print(f"Error: {e}")
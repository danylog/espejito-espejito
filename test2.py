import cv2
import numpy as np
from keras.models import load_model

# Load pre-trained face detection model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Load pre-trained emotion detection model
emotion_model = load_model('fer.hdf5')  # Make sure you have a trained model
emotions = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Initialize the webcam
cap = cv2.VideoCapture(0)

def preprocess_face(face):
    face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    face = cv2.resize(face, (48, 48))             # Resize to the input size of the model
    face = face / 255.0                           # Normalize pixel values
    face = np.expand_dims(face, axis=0)           # Add batch dimension
    face = np.expand_dims(face, axis=-1)          # Add channel dimension
    return face

while True:
    ret, frame = cap.read()  # Capture frame-by-frame
    if not ret:
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        face = frame[y:y+h, x:x+w]
        preprocessed_face = preprocess_face(face)
        prediction = emotion_model.predict(preprocessed_face)
        emotion_label = emotions[np.argmax(prediction)]

        # Draw a rectangle around the face and put emotion label
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.putText(frame, emotion_label, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.imshow('Emotion Detection', frame)  # Display the resulting frame

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np
import time
from keras.models import load_model

# Load face detector and emotion model
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
emotion_model = load_model("fer.h5")  # replace with your model path

emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot access webcam")
    exit()

print("Starting emotion recognition...")

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            roi_gray = gray[y:y+h, x:x+w]
            roi_gray = cv2.resize(roi_gray, (48, 48))
            roi = roi_gray.astype('float') / 255.0
            roi = np.expand_dims(roi, axis=0)
            roi = np.expand_dims(roi, axis=-1)

            prediction = emotion_model.predict(roi, verbose=0)
            maxindex = int(np.argmax(prediction))
            emotion = emotion_labels[maxindex]

            print("Detected emotion:", emotion)
            break  # Only detect one face/emotion per frame

        time.sleep(1)  # Wait 1 second before next check

except KeyboardInterrupt:
    print("Stopping...")

cap.release()

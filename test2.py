import cv2
import numpy as np

# Load OpenCV's pre-trained Haar Cascade for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()  # Capture a frame
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract the face region from the frame
        face = gray[y:y + h, x:x + w]

        # Preprocess the face image (resize and normalize)
        face = cv2.resize(face, (48, 48))  # Assuming the model was trained on 48x48 images
        face = face.astype('float32') / 255.0  # Normalize the image
        face = np.expand_dims(face, axis=-1)  # Add channel dimension (grayscale)
        face = np.expand_dims(face, axis=0)  # Add batch dimension

        # Predict emotion
        emotion_probabilities = model.predict(face)
        max_index = np.argmax(emotion_probabilities)
        dominant_emotion = emotion_labels[max_index]

        # Draw a rectangle around the face and display the predicted emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, dominant_emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Show the frame with emotion label
    cv2.imshow('Emotion Recognition', frame)

    # Break the loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
# asda
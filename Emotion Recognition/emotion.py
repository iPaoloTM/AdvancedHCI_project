import cv2
from deepface import DeepFace
import matplotlib.pyplot as plt
from collections import Counter
import time

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start capturing video
cap = cv2.VideoCapture(0)

emotion_history = []

# Record the start time
start_time = time.time()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Convert grayscale frame to RGB format
    rgb_frame = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2RGB)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray_frame, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # Extract the face ROI (Region of Interest)
        face_roi = rgb_frame[y:y + h, x:x + w]

        # Perform emotion analysis on the face ROI
        result = DeepFace.analyze(face_roi, actions=['emotion'], enforce_detection=False)

        # Determine the dominant emotion
        emotion = result[0]['dominant_emotion']

        # Draw rectangle around face and label with predicted emotion
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

        # Calculate the elapsed time
        elapsed_time = time.time() - start_time

        print(emotion, elapsed_time)

        # Append the emotion and elapsed time to the history
        emotion_history.append((elapsed_time, emotion))

    # Display the resulting frame
    cv2.imshow('Real-time Emotion Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()

# Extract times and emotions for plotting
times = [entry[0] for entry in emotion_history]
emotions = [entry[1] for entry in emotion_history]

# Plot time series of emotions
plt.figure(figsize=(12, 6))
for emotion in set(emotions):
    emotion_times = [times[i] for i in range(len(emotions)) if emotions[i] == emotion]
    plt.scatter(emotion_times, [emotion] * len(emotion_times), label=emotion)

plt.xlabel('Time (seconds)')
plt.ylabel('Emotions')
plt.title('Time Series of Emotions')
plt.legend()
plt.show()

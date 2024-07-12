import cv2
from deepface import DeepFace
import matplotlib.pyplot as plt
from collections import Counter
import time

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Open the video file
video_path = 'video.mp4'  # Replace with the path to your video file
cap = cv2.VideoCapture(video_path)

# Track emotions and engagement
emotion_history = []
dominant_emotions = []
engagement_scores = []
engagement_threshold = 0.5  # Define a threshold for engagement

# Record the start time
start_time = time.time()

# Emotion weights
positive_emotions = {'happy': 1, 'angry': 1, 'surprise': 1}
negative_emotions = {'neutral': -1, 'sad': -1, 'disgust': -1, 'fear': -1}

while cap.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        break

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

        try:
            print(result[0]['emotion'][emotion])
        except:
            print("An exception occurred")

        color = (0, 0, 0)
        if emotion == 'happy':
            color = (0, 255, 255)  # Yellow
        elif emotion == 'sad':
            color = (255, 0, 0)   # Blue
        elif emotion == 'fear':
            color = (128, 0, 128)  # Purple
        elif emotion == 'angry':
            color = (0, 0, 255)   # Red
        elif emotion == 'neutral':
            color = (0, 0, 0)  # Black
        elif emotion == 'surprise':
            color = (0, 165, 255)  # Orange
        elif emotion == 'disgust':
            color = (0, 255, 0)  # Green

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.9, color, 2)

        # Append the emotion to the history
        emotion_history.append(result[0]['emotion'])
        dominant_emotions.append(emotion)

        # Calculate engagement score based on weighted emotions
        engagement_score = 0
        for emo, confidence in result[0]['emotion'].items():
            if emo in positive_emotions:
                engagement_score += confidence * positive_emotions[emo]
            elif emo in negative_emotions:
                engagement_score += confidence * negative_emotions[emo]

        engagement_scores.append(engagement_score)

    # Display the engagement score on the frame
    if len(engagement_scores) > 0:
        avg_engagement_score = sum(engagement_scores[-30:]) / min(len(engagement_scores), 30)  # Rolling average over the last 30 frames
        cv2.putText(frame, f'Engagement Score: {avg_engagement_score:.2f}', (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)

    # Display the resulting frame
    cv2.imshow('Emotion Detection from Video', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture and close all windows
cap.release()
cv2.destroyAllWindows()

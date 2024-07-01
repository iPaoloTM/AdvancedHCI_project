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
dominant_emotions = []

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

        try:
            print(result[0]['emotion'][emotion])
        except:
            print("An exception occurred")

        color=(0,0,0)

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
            color = (0, 255, 0)  # Orange

        cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
        cv2.putText(frame, emotion, (x, y - 10), cv2.FONT_HERSHEY_DUPLEX, 0.9, color, 2)

        # Calculate the elapsed time
        elapsed_time = time.time() - start_time

        #print(emotion, elapsed_time)

        # Append the emotion and elapsed time to the history
        emotion_history.append(result[0]['emotion'])
        dominant_emotions.append(emotion)

    # Display the resulting frame
    cv2.imshow('Real-time Emotion Detection', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close all windows
cap.release()
cv2.destroyAllWindows()

emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
time_series_data = {emotion: [] for emotion in emotions}

for sample in emotion_history:
    for emotion in emotions:
        time_series_data[emotion].append(sample[emotion])

# Color coding for each emotion
color_dict = {
    'angry': 'red',
    'disgust': 'green',
    'fear': 'purple',
    'happy': 'yellow',
    'sad': 'blue',
    'surprise': 'orange',
    'neutral': 'black'
}

# Plotting the time series for each emotion with specified colors
plt.figure(figsize=(12, 6))

for emotion in emotions:
    plt.plot(range(len(emotion_history)), time_series_data[emotion], label=emotion, color=color_dict[emotion])

plt.xlabel('Sample')
plt.ylabel('Confidence')
plt.title('Emotion Confidence Over Samples')
plt.legend(loc='upper right')
plt.grid(True)

plt.tight_layout()
plt.show()

emotion_counts = Counter(dominant_emotions)

# Extract emotions and their counts from Counter object
emotions = list(emotion_counts.keys())
counts = list(emotion_counts.values())

# Plotting the bar chart
plt.figure(figsize=(10, 6))
bars = plt.bar(emotions, counts, color=[color_dict[emotion] for emotion in emotions])

# Adding labels and title
plt.xlabel('Emotion')
plt.ylabel('Count')
plt.title('Dominant Emotions Over Time')

# Adding text labels on top of each bar
for bar, count in zip(bars, counts):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f'{count}', ha='center', va='bottom')

plt.tight_layout()
plt.show()

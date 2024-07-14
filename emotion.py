import cv2
from deepface import DeepFace
import matplotlib.pyplot as plt
from collections import Counter
import time
import threading
import text2speech

# Function for voice feedback
def give_feedback():
    text2speech.read("Keep going, you are doing great!")

# Load face cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Start capturing video
cap = cv2.VideoCapture(0)

# Track emotions and engagement
emotion_history = []
dominant_emotions = []
engagement_scores = []
engagement_threshold = 0.5  # Define a threshold for engagement

# Record the start time
start_time = time.time()

# Emotion weights
positive_emotions = {'happy': 1, 'surprise': 1}
negative_emotions = {'sad': -1, 'disgust': -1, 'fear': -1}

# Counters for positive and negative emotions
positive_count = 0
negative_count = 0
engagement_score = 0

# Initialize last check time
last_check_time = time.time()

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
        cv2.putText(frame, "+"+str(positive_count), (x, y - 50), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 255, 0), 2)
        cv2.putText(frame, "-"+str(negative_count), (x, y - 100), cv2.FONT_HERSHEY_DUPLEX, 0.9, (0, 0, 255), 2)

        # Append the emotion to the history
        emotion_history.append(result[0]['emotion'])
        dominant_emotions.append(emotion)

        # Calculate engagement score based on weighted emotions


        if (emotion == 'happy') or (emotion == 'surprise'):
            engagement_score=engagement_score+5
            positive_count=positive_count+1
        elif (emotion == 'sad') or (emotion == 'fear') or (emotion == 'angry') or (emotion == 'disgust'):
            engagement_score=engagement_score-5
            negative_count=negative_count+1

        engagement_scores.append(engagement_score)

    # Check if 5 seconds have passed
    current_time = time.time()
    if current_time - last_check_time >= 5:
        last_check_time = current_time

        if negative_count > positive_count:
            feedback_thread = threading.Thread(target=give_feedback)
            feedback_thread.start()

        positive_count=0
        negative_count=0



    # if len(engagement_scores) > 0:
    #     avg_engagement_score = sum(engagement_scores[-30:]) / min(len(engagement_scores), 30)  # Rolling average over the last 30 frames
    cv2.putText(frame, f'Engagement Score: {engagement_score}', (10, 30), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)


    cv2.imshow('Real-time Emotion Detection', frame)





    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


cap.release()
cv2.destroyAllWindows()

plt.figure(figsize=(12, 6))
plt.plot(range(len(engagement_scores)), engagement_scores, label='Engagement Score', color='blue')
plt.axhline(y=engagement_threshold, color='red', linestyle='--', label='Engagement Threshold')
plt.xlabel('Frame')
plt.ylabel('Engagement Score')
plt.title('Engagement Score Over Time')
plt.legend(loc='upper right')
plt.grid(True)
plt.tight_layout()
plt.show()


emotion_counts = Counter(dominant_emotions)
emotions = list(emotion_counts.keys())
counts = list(emotion_counts.values())

plt.figure(figsize=(10, 6))
color_dict = {
    'angry': 'red',
    'disgust': 'green',
    'fear': 'purple',
    'happy': 'yellow',
    'sad': 'blue',
    'surprise': 'orange',
    'neutral': 'black'
}
bars = plt.bar(emotions, counts, color=[color_dict[emotion] for emotion in emotions])
plt.xlabel('Emotion')
plt.ylabel('Count')
plt.title('Dominant Emotions Over Time')


for bar, count in zip(bars, counts):
    plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.5, f'{count}', ha='center', va='bottom')

plt.tight_layout()
plt.show()

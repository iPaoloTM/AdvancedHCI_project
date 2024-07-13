import cv2
import numpy as np

# Load pre-trained Haar cascade classifiers for face and facial feature detection
face_cascade = cv2.CascadeClassifier( 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier( 'haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier( 'haarcascade_mcs_mouth.xml')



def detect_landmarks(gray, face):
    (x, y, w, h) = face
    roi_gray = gray[y:y+h, x:x+w]

    # Detect eyes (used as a proxy for eyebrows)
    eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))

    # Detect mouth
    mouth = mouth_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))

    return eyes, mouth

def recognize_emotion(face, eyes, mouth, mouth_centroid_avg, frames):
    (x, y, w, h) = face
    if len(eyes) >= 2 and len(mouth) >= 1:
        (mx, my, mw, mh) = mouth[0]
        mouth_centroid = (x + mx + mw // 2, y + my + mh // 2)
        mouth_centroid_avg=(mouth_centroid_avg+mouth_centroid[1])/frames
        frames=frames+1
        mouth_corners = [(x + mx, y + my + mh), (x + mx + mw, y + my + mh)]

        # Check if the centroid of both corners of the mouth is below the centroid of the mouth
        print("LX CORNER")
        print(mouth_corners[0][1])
        print("RX CORNER")
        print(mouth_corners[1][1])
        print("CENTER")
        print(mouth_centroid[1])
        print("------------------")


        # Check for happy and surprise
        mouth_open = mh > 20  # Assuming the height of the mouth is > 20 pixels indicates open mouth
        if (mouth_corners[0][1]>mouth_centroid[1]) and (mouth_corners[1][1]>mouth_centroid[1]):

            return "Happy"
        else:
            return "Sad"
    else:
        return "Neutral"

# Initialize video capture
cap = cv2.VideoCapture(0)
mouth_centroid_avg=0
frames=1

while True:

    ret, frame = cap.read()
    if not ret:
        break
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for face in faces:
        (x, y, w, h) = face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        eyes, mouth = detect_landmarks(gray, face)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)

        for (mx, my, mw, mh) in mouth:
            cv2.rectangle(frame, (x+mx, y+my), (x+mx+mw, y+my+mh), (0, 0, 255), 2)

        emotion = recognize_emotion(face, eyes, mouth,  mouth_centroid_avg, frames)
        cv2.putText(frame, emotion, (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)

    cv2.imshow('Emotion Recognition', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

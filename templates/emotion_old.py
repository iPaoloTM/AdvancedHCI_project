import cv2
import matplotlib.pyplot as plt
from feat import Detector

# Initialize the detector
detector = Detector()

# Initialize video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to RGB (pyfeat expects RGB images)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Detect facial landmarks
    results = detector.detect_landmarks(rgb_frame)

    # Draw landmarks on the frame
    for face in results.iterrows():
        landmarks = face[1]["landmarks"]
        for (x, y) in landmarks:
            cv2.circle(frame, (int(x), int(y)), 2, (0, 255, 0), -1)

    # Display the frame with landmarks
    cv2.imshow('Facial Landmark Recognition', frame)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the capture and close windows
cap.release()
cv2.destroyAllWindows()

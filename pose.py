import cv2
import mediapipe as mp
import numpy as np

# Initialize MediaPipe Pose.
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
mp_drawing = mp.solutions.drawing_utils

# Define the landmarks for the arms.
RIGHT_ARM_CONNECTIONS = [
    (mp_pose.PoseLandmark.RIGHT_SHOULDER, mp_pose.PoseLandmark.RIGHT_ELBOW),
    (mp_pose.PoseLandmark.RIGHT_ELBOW, mp_pose.PoseLandmark.RIGHT_WRIST)
]
LEFT_ARM_CONNECTIONS = [
    (mp_pose.PoseLandmark.LEFT_SHOULDER, mp_pose.PoseLandmark.LEFT_ELBOW),
    (mp_pose.PoseLandmark.LEFT_ELBOW, mp_pose.PoseLandmark.LEFT_WRIST)
]

# Open a connection to the webcam.
cap = cv2.VideoCapture(0)

def get_angle(a, b, c):
    # Calculate the angle between points a, b, and c
    a = np.array(a)  # First point
    b = np.array(b)  # Middle point
    c = np.array(c)  # End point

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convert the BGR image to RGB.
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Process the image and detect the pose.
    results = pose.process(image_rgb)

    # Draw the pose annotation on the image.
    if results.pose_landmarks:
        # Draw the full body landmarks.
        mp_drawing.draw_landmarks(
            image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
            mp_drawing.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=2),
            mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2))

        right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
        right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
        right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
        left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
        left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
        left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]

        # Get arm positions
        right_angle = get_angle(
            (right_shoulder.x, right_shoulder.y),
            (right_elbow.x, right_elbow.y),
            (right_wrist.x, right_wrist.y)
        )

        left_angle = get_angle(
            (left_shoulder.x, left_shoulder.y),
            (left_elbow.x, left_elbow.y),
            (left_wrist.x, left_wrist.y)
        )

        # Determine arm position
        tolerance_angle = 30  # Adjust tolerance as needed
        right_position = "straight" if right_angle > (180 - tolerance_angle) else "bent"
        left_position = "straight" if left_angle > (180 - tolerance_angle) else "bent"

        if right_elbow.y < right_shoulder.y and right_wrist.y < right_elbow.y:
            right_position = "up"
        elif right_elbow.y > right_shoulder.y and right_wrist.y > right_elbow.y:
            right_position = "down"

        if left_elbow.y < left_shoulder.y and left_wrist.y < left_elbow.y:
            left_position = "up"
        elif left_elbow.y > left_shoulder.y and left_wrist.y > left_elbow.y:
            left_position = "down"

        # Determine overall arm positions
        if right_position == "up" and left_position == "up":
            arm_status = "both up"
        elif right_position == "down" and left_position == "down":
            arm_status = "both down"
        elif right_position == "up" and left_position == "down":
            arm_status = "right up, left down"
        elif right_position == "down" and left_position == "up":
            arm_status = "right down, left up"
        else:
            arm_status = f"right {right_position}, left {left_position}"

        # Draw the arms with a different color.
        for connection in RIGHT_ARM_CONNECTIONS:
            start_idx = connection[0].value
            end_idx = connection[1].value
            if results.pose_landmarks.landmark[start_idx].visibility > 0.5 and results.pose_landmarks.landmark[end_idx].visibility > 0.5:
                start_point = (int(results.pose_landmarks.landmark[start_idx].x * image.shape[1]),
                               int(results.pose_landmarks.landmark[start_idx].y * image.shape[0]))
                end_point = (int(results.pose_landmarks.landmark[end_idx].x * image.shape[1]),
                             int(results.pose_landmarks.landmark[end_idx].y * image.shape[0]))
                cv2.line(image, start_point, end_point, (255, 0, 0), 3)

        for connection in LEFT_ARM_CONNECTIONS:
            start_idx = connection[0].value
            end_idx = connection[1].value
            if results.pose_landmarks.landmark[start_idx].visibility > 0.5 and results.pose_landmarks.landmark[end_idx].visibility > 0.5:
                start_point = (int(results.pose_landmarks.landmark[start_idx].x * image.shape[1]),
                               int(results.pose_landmarks.landmark[start_idx].y * image.shape[0]))
                end_point = (int(results.pose_landmarks.landmark[end_idx].x * image.shape[1]),
                             int(results.pose_landmarks.landmark[end_idx].y * image.shape[0]))
                cv2.line(image, start_point, end_point, (255, 0, 0), 3)

        # Display the arm status on the image.
        cv2.putText(image, arm_status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    # Display the resulting image.
    cv2.imshow('MediaPipe Pose', image)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()



import cv2
import dlib
import numpy as np

# Load Dlib's face detector and shape predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Function to calculate midpoint
def midpoint(p1, p2):
    return int((p1.x + p2.x) / 2), int((p1.y + p2.y) / 2)

# Function to get the pupil location and gaze ratio
def get_gaze_ratio(eye_points, facial_landmarks, gray):
    left_eye_region = np.array([(facial_landmarks.part(point).x, facial_landmarks.part(point).y) for point in eye_points], np.int32)
    min_x = np.min(left_eye_region[:, 0])
    max_x = np.max(left_eye_region[:, 0])
    min_y = np.min(left_eye_region[:, 1])
    max_y = np.max(left_eye_region[:, 1])
    eye = gray[min_y: max_y, min_x: max_x]
    _, threshold_eye = cv2.threshold(eye, 70, 255, cv2.THRESH_BINARY)
    height, width = threshold_eye.shape
    left_side_threshold = threshold_eye[0: height, 0: int(width / 2)]
    left_side_white = cv2.countNonZero(left_side_threshold)
    right_side_threshold = threshold_eye[0: height, int(width / 2): width]
    right_side_white = cv2.countNonZero(right_side_threshold)
    if left_side_white == 0:
        gaze_ratio = 1
    elif right_side_white == 0:
        gaze_ratio = 5
    else:
        gaze_ratio = left_side_white / right_side_white

    # Find the center of the eye
    eye_center = midpoint(facial_landmarks.part(eye_points[0]), facial_landmarks.part(eye_points[3]))

    return gaze_ratio, eye_center

# Load two images
image_left = cv2.imread('IMG_0826.jpeg')
image_right = cv2.imread('IMG_0825.jpeg')

# Initialize video capture
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # Get gaze ratio and pupil position for left eye
        left_eye_ratio, left_pupil = get_gaze_ratio([36, 37, 38, 39, 40, 41], landmarks, gray)

        # Determine where the user is looking
        if left_eye_ratio < 1:
            gaze_direction = "Looking right"
            cursor_pos = (3 * frame.shape[1] // 4, frame.shape[0] // 2)
        elif left_eye_ratio > 1.7:
            gaze_direction = "Looking left"
            cursor_pos = (frame.shape[1] // 4, frame.shape[0] // 2)
        else:
            gaze_direction = "Looking center"
            cursor_pos = (frame.shape[1] // 2, frame.shape[0] // 2)

        # Draw the gaze pointer
        cv2.circle(frame, left_pupil, 5, (0, 0, 255), -1)
        cv2.circle(frame, cursor_pos, 10, (255, 0, 0), 2)
        cv2.putText(frame, gaze_direction, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Resize the images to match the frame size
    frame_height, frame_width = frame.shape[:2]
    image_left_resized = cv2.resize(image_left, (frame_width // 2, frame_height))
    image_right_resized = cv2.resize(image_right, (frame_width // 2, frame_height))

    # Concatenate images side by side
    combined_images = np.concatenate((image_left_resized, image_right_resized), axis=1)

    # Combine the frame and the images vertically
    combined_height, combined_width = combined_images.shape[:2]
    frame_resized = cv2.resize(frame, (combined_width, combined_height // 2))
    display_image = np.vstack((frame_resized, combined_images))

    cv2.imshow('Gaze Detection', display_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

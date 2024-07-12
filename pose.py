import cv2
import mediapipe as mp
import numpy as np
import math
import time

def get_angle(a, b, c):
    # Calculate the angle between points a, b, and c
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle

# Function to calculate angle between two vectors
def get_angle_between_vectors(v1, v2):
    dot_product = sum(x*y for x, y in zip(v1, v2))
    magnitude_v1 = math.sqrt(sum(x**2 for x in v1))
    magnitude_v2 = math.sqrt(sum(x**2 for x in v2))
    cosine_angle = dot_product / (magnitude_v1 * magnitude_v2)
    angle = math.acos(cosine_angle)
    return math.degrees(angle)

# Function to calculate vector from two points
def get_vector(p1, p2):
    return [p2[0] - p1[0], p2[1] - p1[1]]



# Function to calculate the Euclidean distance between two points
def compute_distance(point1, point2):
    return math.sqrt((point2.x - point1.x) ** 2 + (point2.y - point1.y) ** 2)

# Function to detect if the legs are open or closed
def detect_leg_position(left_knee, right_knee, left_ankle, right_ankle, threshold=0.1):
    knee_distance = compute_distance(left_knee, right_knee)
    #print("knee_distance ",knee_distance)

    # Use either knee_distance to determine leg position
    if knee_distance < threshold:
        return 'closed'
    else:
        return 'open'

def findLetter(timer):

    letters={
            "I":0,
            "V":0,
            "X":0,
            "L":0,
            "C":0,
            "D":0,
            "M":0}

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

    start_time = time.time()

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            continue

        # Convert the BGR image to RGB.
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = pose.process(image_rgb)     # Process the image and detect the pose.

        cv2.putText(image, str(int(timer-(time.time()-start_time))), (1100, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 2, cv2.LINE_AA)

        # Draw the pose annotation on the image.
        if results.pose_landmarks:
            right_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_SHOULDER]
            right_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ELBOW]
            right_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_WRIST]
            left_shoulder = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_SHOULDER]
            left_elbow = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ELBOW]
            left_wrist = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_WRIST]

            right_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP]
            left_hip = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP]
            right_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE]
            left_knee = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE]
            right_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE]
            left_ankle = results.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE]


            # Draw right arm
            cv2.line(image, (int(right_shoulder.x * image.shape[1]), int(right_shoulder.y * image.shape[0])),(int(right_elbow.x * image.shape[1]), int(right_elbow.y * image.shape[0])), (0, 255, 0), 2)
            cv2.line(image, (int(right_elbow.x * image.shape[1]), int(right_elbow.y * image.shape[0])),(int(right_wrist.x * image.shape[1]), int(right_wrist.y * image.shape[0])), (0, 255, 0), 2)

            # Draw left arm
            cv2.line(image, (int(left_shoulder.x * image.shape[1]), int(left_shoulder.y * image.shape[0])), (int(left_elbow.x * image.shape[1]), int(left_elbow.y * image.shape[0])), (0, 255, 0), 2)
            cv2.line(image, (int(left_elbow.x * image.shape[1]), int(left_elbow.y * image.shape[0])), (int(left_wrist.x * image.shape[1]), int(left_wrist.y * image.shape[0])), (0, 255, 0), 2)

            # Draw torso
            cv2.line(image, (int(right_shoulder.x * image.shape[1]), int(right_shoulder.y * image.shape[0])),(int(left_shoulder.x * image.shape[1]), int(left_shoulder.y * image.shape[0])), (0, 255, 0), 2)
            cv2.line(image, (int(right_hip.x * image.shape[1]), int(right_hip.y * image.shape[0])),(int(left_hip.x * image.shape[1]), int(left_hip.y * image.shape[0])), (0, 255, 0), 2)
            cv2.line(image, (int(right_shoulder.x * image.shape[1]), int(right_shoulder.y * image.shape[0])),(int(right_hip.x * image.shape[1]), int(right_hip.y * image.shape[0])), (0, 255, 0), 2)
            cv2.line(image, (int(left_shoulder.x * image.shape[1]), int(left_shoulder.y * image.shape[0])),(int(left_hip.x * image.shape[1]), int(left_hip.y * image.shape[0])), (0, 255, 0), 2)

            # Draw right leg
            cv2.line(image, (int(right_hip.x * image.shape[1]), int(right_hip.y * image.shape[0])), (int(right_knee.x * image.shape[1]), int(right_knee.y * image.shape[0])), (0, 255, 0), 2)
            cv2.line(image, (int(right_knee.x * image.shape[1]), int(right_knee.y * image.shape[0])), (int(right_ankle.x * image.shape[1]), int(right_ankle.y * image.shape[0])), (0, 255, 0), 2)

            # Draw left leg
            cv2.line(image, (int(left_hip.x * image.shape[1]), int(left_hip.y * image.shape[0])), (int(left_knee.x * image.shape[1]), int(left_knee.y * image.shape[0])), (0, 255, 0), 2)
            cv2.line(image, (int(left_knee.x * image.shape[1]), int(left_knee.y * image.shape[0])), (int(left_ankle.x * image.shape[1]), int(left_ankle.y * image.shape[0])), (0, 255, 0), 2)


            # Get arm positions
            right_arm_angle = get_angle((right_shoulder.x, right_shoulder.y),(right_elbow.x, right_elbow.y),(right_wrist.x, right_wrist.y)) # angle shoulder - elbow - wrist
            left_arm_angle = get_angle((left_shoulder.x, left_shoulder.y),(left_elbow.x, left_elbow.y),(left_wrist.x, left_wrist.y))

            right_elbow_angle = get_angle((right_hip.x, right_hip.y),(right_shoulder.x, right_shoulder.y),(right_elbow.x, right_elbow.y)) # angle hip - shoulder - elbows
            left_elbow_angle = get_angle((left_hip.x, left_hip.y),(left_shoulder.x, left_shoulder.y),(left_elbow.x, left_elbow.y),)

            right_leg_angle = get_angle((right_hip.x, right_hip.y),(right_shoulder.x, right_shoulder.y),(right_knee.x, right_knee.y)) # angle hip - knee - ankle
            left_leg_angle = get_angle((left_hip.x, left_hip.y),(left_shoulder.x, left_shoulder.y),(left_knee.x, left_knee.y))

            left_knee_angle = get_angle((left_hip.x, left_hip.y),(right_shoulder.x, right_shoulder.y),(left_knee.x, left_knee.y)) # angle shoulder - hip . knee
            right_knee_angle = get_angle((right_hip.x, right_hip.y),(right_shoulder.x, right_shoulder.y),(right_knee.x, right_knee.y))


            tolerance_angle = 20

            right_arm_position = "straight" if right_arm_angle > (180 - tolerance_angle) else "bent"
            left_arm_position = "straight" if left_arm_angle > (180 - tolerance_angle) else "bent"
            right_leg_position = "straight" if right_leg_angle > (180 - tolerance_angle) else "bent"
            left_leg_position = "straight" if left_leg_angle > (180 - tolerance_angle) else "bent"

            right_arm_dir = "up" if right_elbow.y < right_shoulder.y and right_wrist.y < right_elbow.y else "down"
            left_arm_dir = "up" if left_elbow.y < left_shoulder.y and left_wrist.y < left_elbow.y else "down"


            # Determine legs position
            letter = None
            legs_open = detect_leg_position(left_knee, right_knee, left_ankle, right_ankle)
            #print("right_elbow_angle ", right_elbow_angle, "left_elbow_angle ", left_elbow_angle)

            if legs_open == 'open': # X
                #print("checking for X-pose")
                if right_arm_position == "straight" and left_arm_position == "straight":
                    if 160 - tolerance_angle < right_elbow_angle < 160 + tolerance_angle and 160 - tolerance_angle < left_elbow_angle < 160 + tolerance_angle:
                        letter = 'X'
            else:
                # I, V, L, C, D, M
                #print("checking for I, V, L, C, D, M poses")
                if right_arm_position == "straight" and left_arm_position == "straight":
                    if right_arm_dir == "down" and left_arm_dir == "down":
                        if -tolerance_angle < right_elbow_angle <  tolerance_angle and  -tolerance_angle < left_elbow_angle <  tolerance_angle:
                            letter = 'I'
                    elif right_arm_dir == "down" and left_arm_dir == "up":
                        if 90 - tolerance_angle < right_elbow_angle < 90 + tolerance_angle and 170 - tolerance_angle < left_elbow_angle < 170 + tolerance_angle:
                            letter = 'L'
                    elif right_arm_dir == "up" and left_arm_dir == "up":
                        if 170 - tolerance_angle < right_elbow_angle < 170 + tolerance_angle and 170 - tolerance_angle < left_elbow_angle < 170 + tolerance_angle:
                            letter = 'V'
                elif right_arm_position == "bent" and left_arm_position == "bent":
                    if right_arm_dir == "down" and left_arm_dir == "up":
                        if 45 - tolerance_angle < right_elbow_angle < 45 + tolerance_angle and 160 - tolerance_angle < left_elbow_angle < 160 + tolerance_angle:
                            letter = 'C'
                    elif right_arm_dir == "down" and left_arm_dir == "down":
                        if 90 - tolerance_angle < right_arm_angle < 90 + tolerance_angle and 90 - tolerance_angle < left_arm_angle < 90 + tolerance_angle:
                            letter = 'M'
                elif right_arm_position == "bent" and left_arm_position == "straight":
                    if right_arm_dir == "down" and left_arm_dir == "down":
                        if 120 - tolerance_angle < right_arm_angle < 120 + tolerance_angle and  -tolerance_angle < left_elbow_angle <  tolerance_angle:
                            letter = 'D'


            if letter:
                cv2.putText(image, f'Detected letter: {letter}', (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                letters[letter]=letters[letter]+1
            else:
                cv2.putText(image, f'NO LETTER RECOGNISED', (50, 50), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

        # Display the resulting image.
        cv2.imshow('Roman Letter Pose', image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        elapsed_time = time.time() - start_time

        if elapsed_time >= timer:
            break

    cap.release()
    cv2.destroyAllWindows()

    max_key = max(letters, key=letters.get)

    print(f"The letter with the maximum score is: {max_key}")
    return max_key

if __name__ == '__main__':
    findLetter(1000)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # Suppress TensorFlow logs
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'  # Disable oneDNN custom operations

import cv2
import mediapipe as mp
import pyautogui
import time

# Initialize video capture and mediapipe face mesh
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

# Parameters for relative movement
prev_eye_x, prev_eye_y = None, None
sensitivity = 20         # Adjust this to control how much movement is applied
smoothing_factor = 0.2   # Smoothing factor for delta movement
smoothed_dx, smoothed_dy = 0, 0

# Click detection thresholds (tweak these if needed)
left_click_threshold = 0.01   # For left eye blink detection (landmarks 145 & 159)
right_click_threshold = 0.01  # For right eye blink detection (landmarks 374 & 386)

# Initialize click cooldowns
last_left_click = 0
last_right_click = 0
click_cooldown = 1.0  # seconds

while True:
    ret, frame = cam.read()
    if not ret:
        break

    # Flip frame for natural movement and convert color
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, _ = frame.shape

    if landmark_points:
        landmarks = landmark_points[0].landmark

        # --- Relative Mouse Movement using Eye Landmark (e.g., landmark 475) ---
        eye_landmark = landmarks[475]
        current_eye_x = int(eye_landmark.x * frame_w)
        current_eye_y = int(eye_landmark.y * frame_h)
        cv2.circle(frame, (current_eye_x, current_eye_y), 3, (0, 255, 0), -1)

        # Initialize previous position if needed
        if prev_eye_x is None or prev_eye_y is None:
            prev_eye_x, prev_eye_y = current_eye_x, current_eye_y

        # Calculate delta movement from previous frame
        dx = current_eye_x - prev_eye_x
        dy = current_eye_y - prev_eye_y

        # Apply smoothing to reduce jitter
        smoothed_dx = smoothed_dx + smoothing_factor * (dx - smoothed_dx)
        smoothed_dy = smoothed_dy + smoothing_factor * (dy - smoothed_dy)

        # Scale the movement with sensitivity
        move_x = smoothed_dx * sensitivity
        move_y = smoothed_dy * sensitivity

        # Move the mouse pointer relative to its current position
        pyautogui.moveRel(move_x, move_y)

        # Update previous eye position for the next frame
        prev_eye_x, prev_eye_y = current_eye_x, current_eye_y

        # --- Blink Detection for Clicking using Timestamps Instead of Blocking Sleep ---

        current_time = time.time()

        # Left click detection using left eye landmarks [145, 159]
        left_eye = [landmarks[145], landmarks[159]]
        for landmark in left_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255), -1)
        if (left_eye[0].y - left_eye[1].y) < left_click_threshold:
            if current_time - last_left_click > click_cooldown:
                print('Left Click')
                pyautogui.click(button='left')
                last_left_click = current_time

        # Right click detection using right eye landmarks [374, 386]
        right_eye = [landmarks[374], landmarks[386]]
        for landmark in right_eye:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (255, 0, 255), -1)
        if (right_eye[0].y - right_eye[1].y) < right_click_threshold:
            if current_time - last_right_click > click_cooldown:
                print('Right Click')
                pyautogui.click(button='right')
                last_right_click = current_time

    cv2.imshow('Eye Controlled Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
cv2.destroyAllWindows()

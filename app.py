import cv2
import mediapipe as mp

# Initialize mediapipe pose module
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize OpenCV's VideoCapture
cap = cv2.VideoCapture(1)

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture a frame.")
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame using mediapipe pose
    results = pose.process(rgb_frame)

    # Draw body landmarks and lines on the frame
    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        for landmark in landmarks:
            x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        # Draw lines connecting landmarks
        connections = mp_pose.POSE_CONNECTIONS
        for connection in connections:
            start_idx = connection[0]
            end_idx = connection[1]
            start_point = (int(landmarks[start_idx].x * frame.shape[1]), int(landmarks[start_idx].y * frame.shape[0]))
            end_point = (int(landmarks[end_idx].x * frame.shape[1]), int(landmarks[end_idx].y * frame.shape[0]))
            cv2.line(frame, start_point, end_point, (0, 255, 0), 2)

    # Display the processed frame
    cv2.imshow('Body Landmarks', frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the VideoCapture and close the display window
cap.release()
cv2.destroyAllWindows()

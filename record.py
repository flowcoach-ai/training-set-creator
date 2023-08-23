import cv2
import mediapipe as mp
import csv

# Initialize mediapipe pose module
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

# Initialize OpenCV's VideoCapture
cap = cv2.VideoCapture(1)

# Initialize CSV file for saving poses
csv_filename = 'raw_data/pose.csv'
csv_file = open(csv_filename, mode='w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Nose_X', 'Nose_Y', 'Left_Shoulder_X', 'Left_Shoulder_Y', 'Right_Shoulder_X', 'Right_Shoulder_Y', 'Left_Hip_X', 'Left_Hip_Y', 'Right_Hip_X', 'Right_Hip_Y'])

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture a frame.")
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame using mediapipe pose
    results = pose.process(rgb_frame)
    # print(results.pose_landmarks)
    # Draw landmarks and connections on the frame
    if results.pose_landmarks:
        landmark_list = []
        for landmark in results.pose_landmarks.landmark:
            x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
            landmark_list.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)
            print(frame.shape[0], frame.shape[1])

        # Draw lines to connect landmarks
        connections = mp_pose.POSE_CONNECTIONS
        for connection in connections:
            x1, y1 = landmark_list[connection[0]]
            x2, y2 = landmark_list[connection[1]]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Save landmarks to CSV file
        csv_writer.writerow([landmark[0] for landmark in landmark_list])

    # Display the processed frame
    cv2.imshow('Whole Body Pose', frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
csv_file.close()
cv2.destroyAllWindows()

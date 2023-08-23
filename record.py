import cv2
import mediapipe as mp
import csv
from itertools import chain
import datetime
import os

utc_datetime = datetime.datetime.utcnow()
formatted_datetime = utc_datetime.strftime("%Y-%m-%d-%H-%M-%S")

SAMPLE_RATE = 6


# Initialize mediapipe pose module
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

cap = cv2.VideoCapture(1)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))
clip_folder_name = f'clip_{formatted_datetime}'
clip_folder_path = f'clips/{clip_folder_name}'
if not os.path.exists(clip_folder_path):
    os.makedirs(clip_folder_path)
    print(f"Folder '{clip_folder_path}' created successfully.")
else:
    print(f"Folder '{clip_folder_path}' already exists.")

out = cv2.VideoWriter(f"{clip_folder_path}/output.mp4", cv2.VideoWriter_fourcc(*'avc1'), 30, (frame_width, frame_height))

# Initialize CSV file for saving poses
csv_filename = 'raw_data/pose.csv'
csv_file = open(csv_filename, mode='w')
csv_writer = csv.writer(csv_file)


def coords(i):
    return [f"{mp_pose.PoseLandmark(i).name}_X", f"{mp_pose.PoseLandmark(i).name}_Y",
            f"{mp_pose.PoseLandmark(i).name}_Z"]


def xyz(pose_landmark):
    return [pose_landmark.x, pose_landmark.y, pose_landmark.z]


heading = list(chain.from_iterable([coords(i) for i in range(33)]))
csv_writer.writerow(heading)

frame_counter = 0

while cap.isOpened():
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture a frame.")
        break

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process the frame using mediapipe pose
    results = pose.process(rgb_frame)

    # Draw landmarks and connections on the frame
    if results.pose_landmarks:
        frame_counter += 1
        landmark_list = []
        for i, landmark in enumerate(results.pose_landmarks.landmark):
            x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
            landmark_list.append((x, y))
            cv2.circle(frame, (x, y), 5, (0, 255, 0), -1)

        # Draw lines to connect landmarks
        connections = mp_pose.POSE_CONNECTIONS
        for connection in connections:
            x1, y1 = landmark_list[connection[0]]
            x2, y2 = landmark_list[connection[1]]
            cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Save landmarks to CSV file

        if frame_counter % SAMPLE_RATE == 0:
            row = list(chain.from_iterable([xyz(landmark) for landmark in results.pose_landmarks.landmark]))
            csv_writer.writerow(row)

            cv2.imwrite(f"{clip_folder_path}/frame_{frame_counter}.jpg", frame)

            csv_filename = f"{clip_folder_path}/frame_{frame_counter}.csv"
            csv_frame_file = open(csv_filename, mode='w')
            csv_frame_writer = csv.writer(csv_frame_file)
            csv_frame_writer.writerow(row)
            csv_frame_file.close()

            with open(f"{clip_folder_path}/frame_{frame_counter}.txt", 'w') as file:
                pass



    # Display the processed frame
    cv2.imshow('Whole Body Pose', frame)

    out.write(frame)

    # Exit the loop if 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
csv_file.close()
cv2.destroyAllWindows()

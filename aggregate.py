import csv
import os
import mediapipe as mp
from itertools import chain


def coords(i):
    return [f"{mp_pose.PoseLandmark(i).name}_X",
            f"{mp_pose.PoseLandmark(i).name}_Y",
            f"{mp_pose.PoseLandmark(i).name}_Z"]


def titleize_checkpoint(cp):
    return 'IS_' + cp.replace(" ", "_").upper()


absolute_path = os.path.dirname(__file__)
mp_pose = mp.solutions.pose
csv_filename = 'raw_data/training_set.csv'
csv_file = open(csv_filename, mode='w')
csv_writer = csv.writer(csv_file)

checkpoints = ['Downward Dog',
               '3 Legged Dog',
               'Forward Lunge',
               'Crescent Pose',
               'Raise Hands',
               'Arch Your Back']

checkpoint_titles = [titleize_checkpoint(cp) for cp in checkpoints]
heading = list(chain.from_iterable([coords(i) for i in range(33)]))
heading.append(checkpoint_titles)
heading.append('INSTRUCTION')
csv_writer.writerow(heading)

root_path = os.path.join(absolute_path, 'clips')

for folder in os.listdir(os.fsencode(root_path)):
    folder_name = os.fsdecode(folder)
    folder_path = os.path.join(absolute_path, 'clips', folder_name)
    for file in os.listdir(os.fsencode(folder_path)):
        file_name = os.fsdecode(file)
        file_path = os.path.join(folder_path, file_name)
        if file_name.endswith('.csv'):
            print(file_path)
            print("hi")
            with open(file_path, 'r') as textfile:
                line = textfile.readline().strip()
                row = line.split(',')

            # print(os.path.join(directory, filename))
            continue
        elif file_name.endswith('.txt'):
            print(file_path)
            print("bye txt")
            with open(file_path, 'r') as textfile:
                lines = textfile.readlines()
                if len(lines) == 0:
                    raise Exception(f'{file_path} is empty!')
                checkpoint = lines[0].strip()
                instruction = lines[1].strip()
                row.append(annotate_checkpoint)
                row.append(instruction)
                csv_writer.writerow(row)
            continue
        else:
            continue

csv_file.close()

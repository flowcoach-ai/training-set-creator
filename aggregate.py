import csv
import os
import re
import mediapipe as mp
from itertools import chain

instructions = {
    "Low Lunge": [
        "come into a low lunge",
        "bring one leg back one leg forward with your fingertips underneath your shoulders on the mat",
        "make sure that your feet are hips-width in distance and that your front leg shin is in a nice straight line over the top of the front foot",
        "with the ball of the back foot stacked underneath the heel put a little bend in your back leg knee"
    ],
    "Crescent Pose": [
        "place your hands on your front leg knee",
        "press your torso up over your pelvis",
        "lift your lower belly and draw your ribs in",
        "begin to straighten your back leg by pressing the heel back and lifting the inner thigh",
        "squeeze your inner thighs together",
        "raise your arms up towards the sky",
        "as you inhale lengthen through the sides of your waist",
        "lift your back ribs as you exhale",
        "bring palms to touch and gaze up towards your hands",
        "perfect"
    ],
    "Correction": [
        "turn to your side",
        "lower back down into a lunge",
    ]
}


def translate_pose_number_into_text(pose_number):
    return checkpoints[int(pose_number)]


def translate_instruction_number_into_text(pose_name, instruction_number):
    return instructions[pose_name][int(instruction_number)]


def titleize_checkpoint(cp):
    return 'IS_' + cp.replace(" ", "_").upper()


checkpoints = ['Low Lunge',
               'Crescent Pose',
               'Correction']

checkpoint_titles = [titleize_checkpoint(cp) for cp in checkpoints]

mp_pose = mp.solutions.pose


def coords(i):
    return [f"{mp_pose.PoseLandmark(i).name}_X",
            f"{mp_pose.PoseLandmark(i).name}_Y",
            f"{mp_pose.PoseLandmark(i).name}_Z"]


def annotate_checkpoint(cp):
    titled_cp = titleize_checkpoint(cp)
    if titled_cp not in checkpoint_titles:
        raise Exception(f'Checkpoint is not defined: {cp}')

    return [str(int(titled_cp == title)) for title in checkpoint_titles]


def run():
    absolute_path = os.path.dirname(__file__)
    csv_filename = 'raw_data/training_set.csv'
    csv_file = open(csv_filename, mode='w')
    csv_writer = csv.writer(csv_file)

    heading = list(chain.from_iterable([coords(i) for i in range(33)]))
    heading.extend(checkpoint_titles)
    heading.append('INSTRUCTION')
    csv_writer.writerow(heading)

    root_path = os.path.join(absolute_path, 'clips')

    for folder in os.listdir(os.fsencode(root_path)):
        rows = {}
        folder_name = os.fsdecode(folder)
        folder_path = os.path.join(absolute_path, 'clips', folder_name)

        for file in sorted(os.listdir(os.fsencode(folder_path))):
            file_name = os.fsdecode(file)
            if not file_name.startswith('frame'):
                continue
            file_number = re.search(r'\d+', file_name).group()

            if rows.get(file_number) is None:
                rows[file_number] = []

            file_path = os.path.join(folder_path, file_name)
            if file_name.endswith('.csv'):
                with open(file_path, 'r') as textfile:
                    line = textfile.readline().strip()
                    values = line.split(',')
                    rows[file_number].extend(values)
                continue
            elif file_name.endswith('.txt'):
                with open(file_path, 'r') as textfile:
                    lines = textfile.readlines()
                    if len(lines) == 0:
                        print(f'{file_path} is empty!')
                        continue

                    instruction = lines[1].strip()

                    if instruction == "None":
                        print(f'skipping {file_path}: no instruction specified')
                        continue

                    checkpoint = translate_pose_number_into_text(lines[0].strip())
                    # instruction = translate_instruction_number_into_text(checkpoint, lines[1].strip())

                    try:
                        rows[file_number].extend(annotate_checkpoint(checkpoint))
                        rows[file_number].append(instruction)
                        csv_writer.writerow(rows[file_number])
                    except Exception as e:
                        print(e)
                continue
            else:
                continue

    csv_file.close()


run()

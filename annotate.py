import streamlit as st
import os
import time

instructions = {
    'Downward Dog': [
        'Focus on pressing your heels toward the ground.',
        'Engage your core muscles for better stability.',
        'Relax your neck and let your head hang naturally.'
    ],
    '3 Legged Dog': [
        'Extend your raised leg higher for a deeper stretch.',
        'Keep your hips squared and facing downward.',
        'Maintain an even distribution of weight between your hands.'
    ],
    'Low Lunge': [
        'Ensure your front knee is directly above your ankle.',
        'Activate your back leg to feel a stretch in your hip flexor.',
        'Consider using props for better balance and alignment.'
    ],
    'Crescent Pose': [
        'Sink deeper into your front knee while keeping your back leg straight.',
        'Engage your core muscles to stabilize your torso.',
        'Extend your arms upward and feel the stretch in your back.'
    ],
    'Look Up': [
        'Gently lift your chin while maintaining a neutral spine.',
        'Engage your upper back muscles to avoid straining your neck.',
        'Breathe deeply and create space in your chest and throat.'
    ],
    'Back Bend': [
        'Start with a gentle backbend and gradually increase the arch.',
        'Press your hips forward to protect your lower back.',
        'Engage your glutes and quads for added stability.'
    ]
}


class FileManager:
    def __init__(self):
        self.clips_directory = os.listdir('clips')
        self.frame_filenames = []
        self.current_clip_directory = ""

    def clips_directories(self):
        unique_names = set()

        for filename in self.clips_directory:
            if filename.startswith('clip'):
                unique_names.add(f"clips/{filename}")

        return list(unique_names)

    def frames(self, in_clip_directory):
        self.current_clip_directory = in_clip_directory
        ls_clip_directory = os.listdir(in_clip_directory)
        unique_frames = set()

        for filename in ls_clip_directory:
            if filename.startswith('frame'):
                name_without_extension = filename.split('.')[0]  # Remove anything after the "."
                unique_frames.add(name_without_extension)

            self.frame_filenames = list(unique_frames)

        return self.unsaved_frames()

    def unsaved_frames(self):
        def is_unsaved(y_input):
            with open(f"{self.current_clip_directory}/{y_input}.txt", 'r') as y_txt:
                return y_txt.read() == ""

        return list(filter(is_unsaved, self.frame_filenames))


st.title("Aggregating & Annotating Platform")
st.write("select the y")

if 'current_index' not in st.session_state:
    st.session_state['current_index'] = 0

progress_text = "Operation in progress. Please wait."
my_bar = st.progress(0, text=progress_text)

FM = FileManager()


def onchange():
    st.session_state.current_index = 0


selected_directory = st.selectbox('Directory:', FM.clips_directories(), on_change=onchange)

if selected_directory:
    frame = FM.frames(selected_directory)

    for index in range(len(frame)):
        checkpoints = list(instructions.keys())
        checkpoints.insert(0, 'None')
        selected_instructions_values = []
        if f'save{index}' not in st.session_state:
            if index == 0:
                st.session_state[f'save{index}'] = True
            else:
                st.session_state[f'save{index}'] = False

        if index == st.session_state.current_index:
            st.image(f"{selected_directory}/{frame[index]}.jpg",
                     caption=f"{st.session_state.current_index} {frame[index]}",
                     use_column_width=True)

            selected_checkpoint = st.selectbox('Checkpoints:', checkpoints, key=f"checkpoint-{index}")
            if selected_checkpoint != 'None':
                selected_instructions_values = instructions[selected_checkpoint]
                selected_instructions_values.insert(0, 'None')

            selected_instructions = st.selectbox('Instructions:', selected_instructions_values,
                                                 key=f"instructions-{index}")

            if selected_instructions != 'None' and selected_checkpoint != 'None':
                with open(f"{selected_directory}/{frame[st.session_state.current_index]}.txt", 'w') as file:
                    file.write(f'{selected_checkpoint}:{selected_instructions}')
                st.write(f"{frame[st.session_state.current_index]} has been updated.")
                my_bar.progress(index + 1, text=progress_text)
                st.session_state.current_index = index

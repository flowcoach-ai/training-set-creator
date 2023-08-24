import streamlit as st
import time
from utils.filemanager import FileManager

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

st.title("Aggregating & Annotating Platform")

if 'current_index' not in st.session_state:
    st.session_state['current_index'] = 0

FM = FileManager()


def onchange():
    st.session_state.current_index = 0


selected_directory = st.selectbox('Directory:', FM.clips_directories(), on_change=onchange)


def current_progress():
    current = FM.frames(selected_directory)
    completed = FM.get_total_frames() - len(current)
    if completed == 0 or FM.get_total_frames() == 0:
        return 0
    total_frames = FM.get_total_frames()
    return round((completed / total_frames) * 100)


progress_text = ""
bar = st.progress(current_progress(), text=progress_text)
frame = FM.frames(selected_directory)

if selected_directory and len(frame) > 0:
    index = st.session_state.current_index
    checkpoints = list(instructions.keys())
    checkpoints.insert(0, 'None')
    selected_instructions_values = []
    if f'save{index}' not in st.session_state:
        st.session_state[f'save{index}'] = False

    if index == st.session_state.current_index:
        st.image(f"{selected_directory}/{frame[index]}.jpg",
                 caption=f"{frame[index]}",
                 use_column_width=True)

        selected_checkpoint = st.selectbox('Checkpoints:', checkpoints, key=f"checkpoint-{index}")
        if selected_checkpoint != 'None':
            selected_instructions_values = instructions[selected_checkpoint]
            selected_instructions_values.insert(0, 'None')

        selected_instructions = st.selectbox('Instructions:', selected_instructions_values,
                                             key=f"instructions-{index}")

        if selected_instructions != 'None' and selected_checkpoint != 'None':
            if st.button('Save', key=f"save-{index}"):
                with open(f"{selected_directory}/{frame[index]}.txt", 'w') as y_txt:
                    y_txt.write(f"{selected_checkpoint}\n{selected_instructions}")
                st.session_state[f'save{index}'] = True
                st.session_state.current_index += 1
                bar.progress(current_progress())
                time.sleep(3)
                st.experimental_rerun()
else:
    st.success(f"Annotation complete for {selected_directory}")
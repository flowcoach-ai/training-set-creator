import streamlit as st
import time
from utils.filemanager import FileManager

instructions = {
    'Low Lunge': [
        'Come into a runners lunge one',
        'leg back one leg forward with your',
        'fingertips underneath your shoulders on',
        'the mat make sure that your feet are hips-width in distance and that your front leg Shin is in a nice straight line over the top of the foot the back, leg knee is lifted up off the ground',
        'with the ball of the foot stacked underneath the heel put a little bend in',
        'your back leg knee place your hands on your front leg knee and press your torso',
    ],
    'Crescent Pose': [
        'up over your pelvis from here lift your',
        'lower belly and draw your ribs in begin',
        'to straighten your back leg by pressing the heel back and lifting the inner',
        'thigh squeeze your inner thighs together',
        'your arms up towards the sky as you',
        'inhale lengthen through the sides of your waist and lift your back ribs as you exhale draw your front ribs down and',
        'palms to touch and gaze up towards your hands'
    ],
}

def translate_pose(pose_name):
    return(index(instructions.keys(), pose_name))

def translate_instruction(pose_name, instruction):
    return (index(translate_pose(pose_name)), index(instruction))

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
    # checkpoints.insert(0, 'None')
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
                    y_txt.write(f"{translate_pose(selected_checkpoint)}\n{translate_instruction(selected_checkpoint, selected_instructions)}")
                st.session_state[f'save{index}'] = True
                st.session_state.current_index += 1
                bar.progress(current_progress())
                time.sleep(3)
                st.experimental_rerun()
else:
    if selected_directory is None:
        st.error("There are no clips to run in the /clips folder.")
        st.warning("Make sure to add the clip_* folders to the /clips folder.")
        st.markdown(":violet[Record data to annotate: ] **:blue[python record.py]** ")

    else:
        st.success(f"Annotation complete for {selected_directory}")

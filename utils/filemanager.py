import os


class FileManager:
    def __init__(self):
        self.clips_directory = os.listdir('clips')
        self.frame_filenames = []
        self.total_frames = 0
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
            self.total_frames = len(self.frame_filenames)

        return self.unsaved_frames()

    def get_total_frames(self):
        return self.total_frames

    def unsaved_frames(self):
        def is_unsaved(y_input):
            with open(f"{self.current_clip_directory}/{y_input}.txt", 'r') as y_txt:
                return y_txt.read() == ""

        return list(filter(is_unsaved, self.frame_filenames))

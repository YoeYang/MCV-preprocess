import os
import subprocess

class AudioExtractor:
    def __init__(self, video_input_path, audio_output_base, data_length):
        """
        :param video_input_path: root dir of input videos. Sub-directory name format: f"{i:04d} (eg. 0001, 0232)
        :param audio_output_base: root dir of output audio. Default: data-audio in current dir. 
        """
        self.video_input_path = video_input_path
        self.audio_output_base = audio_output_base
        self.data_length = data_length

    def extract_audio(self, input_file, output_file):
        ffmpeg_command = [
            'ffmpeg', '-i', input_file,
            '-vn',  # delete video
            '-acodec', 'pcm_s16le',
            '-ar', '44100',
            '-y',   # cover original video
            output_file
        ]
        try:
            subprocess.run(ffmpeg_command, check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error processing file {input_file}: {e}")

    def process_folders(self):
        for i in range(1, self.data_length): 
            folder_name = f"{i:04d}"
            input_folder = os.path.join(self.video_input_path, folder_name)
            input_file = os.path.join(input_folder, f"{folder_name}.mp4")
            output_folder = os.path.join(self.audio_output_base, folder_name)

            if os.path.exists(input_file):
                os.makedirs(output_folder, exist_ok=True)
                output_file = os.path.join(output_folder, f"{folder_name}.wav")
                self.extract_audio(input_file, output_file)
                print(f"{input_file} processed!")
            else:
                print(f"{input_file} doesn't exit!")

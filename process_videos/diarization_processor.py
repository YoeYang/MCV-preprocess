import os
import torch
from pyannote.audio import Pipeline

class DiarizationProcessor:
    def __init__(self, audio_input_base, time_output_base,
                 auth_token=" ", data_length=455):      
        """
        ATTENTION: You should edit your file number, and get the access of pyannote on Huggingface. Then add your auth_token.
        Pyannote HF: https://huggingface.co/pyannote/speaker-diarization-3.1
        :param audio_input_base: root dir of input audio
        :param time_output_base: root dir of output timestamp
        :param start_num: Your video start ID number (default 0001)
        :param end_num: Your video start ID number (default 0455)
        :param auth_token: pyannote model access token
        """
        self.audio_input_base = audio_input_base
        self.time_output_base = time_output_base
        self.auth_token = auth_token
        self.data_length = data_length

        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            print(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            self.device = torch.device("cpu")
            print("No GPU found, using CPU instead.")
        self.pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1",
                                                 use_auth_token=self.auth_token)

    def process(self):
        for number in range(1, self.data_length):
            folder_name = f"{number:04d}"
            wav_file_path = os.path.join(self.audio_input_base, folder_name, f"{folder_name}.wav")
            if os.path.exists(wav_file_path):
                diarization = self.pipeline(wav_file_path)
                txt_output_folder = os.path.join(self.time_output_base, folder_name)
                os.makedirs(txt_output_folder, exist_ok=True)
                txt_file_path = os.path.join(txt_output_folder, f"{folder_name}.txt")
                with open(txt_file_path, 'w') as txt_file:
                    for turn, _, speaker in diarization.itertracks(yield_label=True):
                        txt_file.write(f"Speaker {speaker} from {turn.start:.1f}s to {turn.end:.1f}s\n")
                print(f"{wav_file_path} Processed. Result saved in {txt_file_path}")
            else:
                print(f"{wav_file_path} doesn't exit!")

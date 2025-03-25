import os
import whisper
import torch

class VideoTranscriber:
    def __init__(self, model_path, clips_input, transcript_output):
        """
        :param model_path: Path of whisper model
        :param clips_input: Root dir of input video clips
        :param transcript_output: Dir of output transcription text
        """
        self.clips_input = clips_input
        self.transcript_output = transcript_output
        os.makedirs(self.transcript_output, exist_ok=True)
        if torch.cuda.is_available():
            self.device = torch.device("cuda")
            print(f"Using GPU: {torch.cuda.get_device_name(0)}")
        else:
            self.device = torch.device("cpu")
            print("No GPU found, using CPU instead.")
        self.model = whisper.load_model(model_path)

    def process_videos(self):
        for folder_name in os.listdir(self.clips_input):
            folder_path = os.path.join(self.clips_input, folder_name)
            if not os.path.isdir(folder_path):
                continue
            output_folder = os.path.join(self.transcript_output, folder_name)
            os.makedirs(output_folder, exist_ok=True)
            for filename in os.listdir(folder_path):
                if filename.endswith(".mp4"):
                    input_file_path = os.path.join(folder_path, filename)
                    if os.path.exists(input_file_path):
                        result = self.model.transcribe(input_file_path, language='en')
                        output_file_name = filename.replace(".mp4", ".txt")
                        output_file_path = os.path.join(output_folder, output_file_name)
                        with open(output_file_path, "w", encoding="utf-8") as f:
                            f.write(result['text'])
                        print(f"Transcription for {filename} has been saved to {output_file_path}.")
                    else:
                        print(f"File {input_file_path} does not exist.")

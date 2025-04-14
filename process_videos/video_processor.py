import os
from .audio_extractor import AudioExtractor
from .diarization_processor import DiarizationProcessor
from .timestamp_processor import TimestampProcessor

class VideoProcessor:
    def __init__(self, video_input_path, current_dir):
        """
        Edit data length with your total video number.
        """
        self.video_input_path = video_input_path
        self.current_dir = current_dir
        self.audio_output_base = os.path.join(current_dir, "data-audio")
        self.time_output_base = os.path.join(current_dir, "data-time")
        self.data_length = 455   # Edit here

        os.makedirs(self.audio_output_base, exist_ok=True)
        os.makedirs(self.time_output_base, exist_ok=True)

        self.audio_extractor = AudioExtractor(self.video_input_path, self.audio_output_base, self.data_length)
        self.diarization_processor = DiarizationProcessor(self.audio_output_base, self.time_output_base, self.data_length)
        self.timestamp_processor = TimestampProcessor(self.time_output_base, self.data_length)

    def process(self):
        print("Start extract audio...")
        self.audio_extractor.process_folders()
        print("Audio extraction finished!\n")

        print("Start speaker diarization...")
        self.diarization_processor.process()
        print("Diarization finished!\n")

        print("Start auto denoise and merge timestamps...")
        self.timestamp_processor.process_time_files()
        print("Timestamp clean finished!")

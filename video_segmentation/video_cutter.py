import os
import subprocess

class VideoCutter:
    def __init__(self, video_base, timestamps_dir, clips_output):
        """
        :param video_base: Root path of input video, video path format: {video_base}/{number:04d}/{number:04d}.mp4
        :param timestamps_dir: path of timestamps
        :param clips_output: Dir of output video clips
        """
        self.video_base = video_base
        self.timestamps_dir = timestamps_dir
        self.clips_output = clips_output
        os.makedirs(self.clips_output, exist_ok=True)

    def get_video_info(self, input_video):
        probe_cmd = f'ffprobe -v error -select_streams v:0 -show_entries stream=codec_name,pix_fmt -of default=noprint_wrappers=1:nokey=1 "{input_video}"'
        result = subprocess.run(probe_cmd, shell=True, capture_output=True, text=True)
        lines = result.stdout.splitlines()
        if len(lines) >= 2:
            codec_name = lines[0].strip()
            pix_fmt = lines[1].strip()
            return codec_name, pix_fmt
        return None, None

    def extract_video_segments(self, input_video, timestamps_file, output_folder):
        os.makedirs(output_folder, exist_ok=True)
        with open(timestamps_file, 'r') as f:
            lines = f.readlines()
        timestamps = [float(line.strip()) for line in lines]
        if len(timestamps) < 2:
            print(f"ERROR: {timestamps_file} doesn't have enough timestamps")
            return
        codec_name, pix_fmt = self.get_video_info(input_video)
        base_name = os.path.splitext(os.path.basename(input_video))[0]
        for i in range(len(timestamps) - 1):
            start_time = timestamps[i]
            end_time = timestamps[i + 1]
            segment_number = i // 2 + 1 
            suffix = 'A' if i % 2 == 0 else 'B'
            output_file = os.path.join(output_folder, f"{base_name}-{segment_number}-{suffix}.mp4")
            ffmpeg_command = [
                'ffmpeg',
                '-i', input_video,
                '-ss', str(start_time),
                '-to', str(end_time),
                '-c:v', codec_name,
                '-pix_fmt', pix_fmt,
                '-c:a', 'copy',
                '-y',
                output_file
            ]
            try:
                subprocess.run(ffmpeg_command, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"Successful extacted: {output_file}")
            except subprocess.CalledProcessError as e:
                print(f"Fail to extract: {e}")

    def batch_process_videos(self, number_list):
        for number in number_list:
            number_str = f"{number:04d}"
            input_video_path = os.path.join(self.video_base, number_str, f"{number_str}.mp4")
            timestamps_file_path = os.path.join(self.timestamps_dir, f"{number_str}.txt")
            output_folder_path = os.path.join(self.clips_output, number_str)
            if not os.path.exists(timestamps_file_path):
                print(f"File doesn't exist: {timestamps_file_path}")
                continue
            if not os.path.exists(input_video_path):
                print(f"File doesn't exist:{input_video_path}")
                continue
            self.extract_video_segments(input_video_path, timestamps_file_path, output_folder_path)
            print(f"Finished: {number_str}")
        print("All video clips are exracted!")

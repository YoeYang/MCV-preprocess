import os

class TimestampGenerator:
    def __init__(self, merged_dir, timestamps_dir):
        """
        :param merged_dir: Dir of input merged timestamps
        :param timestamps_dir: Dir of output new timestamps for cutting video
        """
        self.merged_dir = merged_dir
        self.timestamps_dir = timestamps_dir
        os.makedirs(self.timestamps_dir, exist_ok=True)

    @staticmethod
    def generate_timestamp(merged_segments):
        timestamps = []
        if not merged_segments:
            return timestamps
        # The first line: first frame of video
        first_start_time = merged_segments[0][1]
        timestamps.append(first_start_time)
        for i in range(len(merged_segments)):
            start_time = merged_segments[i][1]
            if i > 0:
                previous_end_time = merged_segments[i-1][2]
                timestamps.append(max(previous_end_time, start_time))
        # The last line: last frame of video
        last_end_time = merged_segments[-1][2]
        timestamps.append(last_end_time)
        return timestamps

    def process_file(self, number):
        file_name = f"{number:04d}.txt"
        input_file = os.path.join(self.merged_dir, file_name)
        if not os.path.exists(input_file):
            print(f"File doesn't exist: {input_file}")
            return
        merged_segments = []
        with open(input_file, 'r') as f:
            for line in f:
                parts = line.strip().split(' ')
                if len(parts) == 6:
                    try:
                        speaker = parts[1]
                        start_time = float(parts[3][:-1])
                        end_time = float(parts[5][:-1])
                        merged_segments.append([speaker, start_time, end_time])
                    except ValueError:
                        continue
        timestamps = self.generate_timestamp(merged_segments)
        output_file = os.path.join(self.timestamps_dir, file_name)
        with open(output_file, 'w') as f:
            for t in timestamps:
                f.write(f"{t:.1f}\n")
        print(f"{input_file} processed, generated timestamps have saved in {output_file}")

    def process_files(self, number_list):
        for number in number_list:
            self.process_file(number)

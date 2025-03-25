import os

class TimestampProcessor:
    def __init__(self, time_base_path, data_length):
        self.time_base_path = time_base_path
        self.data_length = data_length

    # def generate_timestamp(self, merged_segments):
    #     """
    #     根据合并后的时间段生成时间戳列表：
    #      - 第一行为起始时间，
    #      - 中间行为每段的起始时间（取上一段结束与当前开始的较大值），
    #      - 最后一行为结束时间。
    #     """
    #     timestamps = []
    #     if not merged_segments:
    #         return timestamps

    #     first_start_time = merged_segments[0][1]
    #     timestamps.append(first_start_time)
    #     for i in range(len(merged_segments)):
    #         start_time = merged_segments[i][1]
    #         if i > 0:
    #             previous_end_time = merged_segments[i-1][2]
    #             timestamps.append(max(previous_end_time, start_time))
    #     last_end_time = merged_segments[-1][2]
    #     timestamps.append(last_end_time)
    #     return timestamps

    def denoise_n_merge(self, input_file, output_file):
        """
        denoise and merge on the original timestamps.
        The new result will cover old one.
        """
        with open(input_file, 'r') as f:
            lines = f.readlines()

        merged_segments = []
        current_speaker = None
        current_start = None
        current_end = None

        for line in lines:
            parts = line.strip().split(' ')
            if len(parts) != 6:
                continue
            speaker = parts[1]
            try:
                start_time = float(parts[3][:-1])
                end_time = float(parts[5][:-1])
            except ValueError:
                continue

            if (end_time - start_time) <= 2.0:
                continue

            if current_speaker == speaker and current_end is not None:
                current_end = max(current_end, end_time)
            else:
                if current_speaker is not None:
                    merged_segments.append([current_speaker, current_start, current_end])
                current_speaker = speaker
                current_start = start_time
                current_end = end_time

        if current_speaker is not None:
            merged_segments.append([current_speaker, current_start, current_end])

        with open(output_file, 'w') as f:
            for segment in merged_segments:
                f.write(f"Speaker {segment[0]} from {segment[1]:.1f}s to {segment[2]:.1f}s\n")
        return merged_segments

    def process_time_files(self):
        for i in range(1, self.data_length):
            folder_name = f"{i:04d}"
            folder_path = os.path.join(self.time_base_path, folder_name)
            txt_file_path = os.path.join(folder_path, f"{folder_name}.txt")
            if os.path.exists(txt_file_path):
                merged_segments = self.denoise_n_merge(txt_file_path, txt_file_path)
            #     timestamps = self.generate_timestamp(merged_segments)
            #     timestamps_file_path = os.path.join(folder_path, "timestamps.txt")
            #     with open(timestamps_file_path, 'w') as ts_file:
            #         for ts in timestamps:
            #             ts_file.write(f"{ts:.1f}\n")
            #     print(f"已处理 {txt_file_path}，生成的时间戳保存在 {timestamps_file_path}")
            # else:
            #     print(f"文件不存在: {txt_file_path}")

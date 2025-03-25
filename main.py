import os
import argparse
from process_videos.video_processor import VideoProcessor
from video_segmentation.timestamp_generator import TimestampGenerator
from video_segmentation.video_cutter import VideoCutter
from video_segmentation.video_transcriber import VideoTranscriber

def main():
    parser = argparse.ArgumentParser(description="Main project: Process videos and Video segmentation")
    subparsers = parser.add_subparsers(dest="command", required=True, help="command: process_videos or segment")
    
    # Step 1：process_videos
    parser_videos = subparsers.add_parser("process_videos", help="process video: audio extraction, diarization, timestamps denoise/merge")
    parser_videos.add_argument("video_input_path", help="root path of input videos")
    
    # Step 2：segment
    parser_segment = subparsers.add_parser("segment", help="video segmentation: timestamp generation, video clips extraction, transcription generation")
    # timestamp generation (used to cut video)
    parser_segment.add_argument("--merged_dir", type=str, default='./data-merge', help="path of merged timestamps")
    parser_segment.add_argument("--timestamps_dir", type=str, default='./data-timestamps', help="output dir of timestamps")
    parser_segment.add_argument("--numbers", nargs="+", type=int, default=list(range(1, 455)),
                                help="file number list needed to process")
    # video clips extraction
    parser_segment.add_argument("--video_base", required=True, help="root path of input videos")
    parser_segment.add_argument("--clips_output", type=str, default='./data-clips', help="path of output video clips")

    # transcription generation
    parser_segment.add_argument("--clips_input", type=str, default='./data-clips', help="root path of input videos")
    parser_segment.add_argument("--transcript_output", type=str, default='./data-text', help="path of output transcription texts")
    parser_segment.add_argument("--whisper_model", required=True, help="path of whisper model")
    
    args = parser.parse_args()
    current_dir = os.getcwd()
    if args.command == "process_videos":
        processor = VideoProcessor(args.video_input_path, current_dir)
        processor.process()
    elif args.command == "segment":
        # timestamp generation
        ts_generator = TimestampGenerator(args.merged_dir, args.timestamps_dir)
        ts_generator.process_files(args.numbers)
        # video clips extraction
        cutter = VideoCutter(args.video_base, args.timestamps_dir, args.clips_output)
        cutter.batch_process_videos(args.numbers)
        # transcription generation
        transcriber = VideoTranscriber(args.whisper_model, args.clips_input, args.transcript_output)
        transcriber.process_videos()

if __name__ == "__main__":
    main()

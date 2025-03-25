# Video Preprocess Code for Multimodal Conversational Research: Diarization, Segmentation and Transcription

This project is designed to process videos through a series of automated tasks including:

- **Audio Extraction & Speaker Diarization**: Extract audio from videos, perform speaker diarization, and generate clean timestamp files.
- **Video Segmentation**: Generate segmentation timestamps, cut the videos into clips based on these timestamps, and transcribe the clips using the Whisper model.

The project is organized into two main modules:
- **process_videos**: Handles audio extraction, diarization, and timestamp denoise/merge.
- **video_segmentation**: Handles generating segmentation timestamps, video cutting, and transcription of video clips.

## 🦄 Project Structure
project/
├── main.py
├── check_speaker.py
├── process_videos/
│   ├── __init__.py
│   ├── audio_extractor.py
│   ├── diarization_processor.py
│   ├── timestamp_processor.py
│   └── video_processor.py
├── video_segmentation/
│   ├── __init__.py
│   ├── timestamp_generator.py
│   ├── video_cutter.py
│   └── video_transcriber.py
└── setup.py


## 🔨 Installation

### Prerequisites

- Python 3.8 or later
- [PyTorch](https://pytorch.org/)  
- [pyannote.audio](https://github.com/pyannote/pyannote-audio)  
- [whisper](https://github.com/openai/whisper)  
- Other dependencies as listed in `setup.py`

### Steps

1. **Clone the Repository**

   ```bash
   git clone 
   cd project
   ```

2. **Install the Package**

From the project root, run:

   ```bash
   pip install -e .
   ```

## 🪄 Usage
The project provides a unified command-line interface through main.py with two subcommands.

### Step 1. Process Videos

This command will:

1. Extract audio from input videos (expecting subfolders named 0001 to 0454 with corresponding .mp4 files).

2. Perform speaker diarization on selected audio files.

3. Process and clean the generated timestamp files (denoise/merge).

   ```bash
   python main.py process_videos /path/to/your/video_folder
   ```

Replace /path/to/your/video_folder with the directory containing your video subfolders.

### ⚠️ Step 1.5. Mannual Check
We strongly recommand you have a mannual check in your merged timestamps, and edit unqualified .txt file by yourself.
Before that, you can use check_speaker.py to automatically output unqualified file names.

That will be very helpful to have right video clips!

### Step 2. Video Segmentation
This command will:

1. Generate segmentation timestamps from merged timestamp files.

2. Extract video clips based on the generated timestamps.

3. Transcribe the video clips using the Whisper model.

   ```bash
   python main.py segment --video_base /path/to/your/video_folder --whisper_model /path/to/whisper-model/small.pt

   ```
Replace with the directory containing your video subfolders and whisper models.

## ✏️ Citation
If you find this work useful for your research, please feel free to leave a star⭐️ and cite our paper:

```bibtex
@misc{yang2025saynext,
      title={SayNext: A Novel Benchmark for Multimodal Emotion Understanding via Next-Utterance Prediction}, 
      author={Yueyi Yang and Haotian Liu and Haoyu Chen},
      year={2025},
      eprint={arXiv:2403.xxxxx}, 
      archivePrefix={arXiv},
      primaryClass={cs.CL}
}
```

## 🤝 Acknowledgement
This work is supported by **The University of Oulu & The Research Council of Finland, PROFI7 352788**. Thanks to [Pyannote](https://github.com/pyannote/pyannote-audio), [Whisper ](https://github.com/openai/whisper). 
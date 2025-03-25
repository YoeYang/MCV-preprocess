from setuptools import setup, find_packages

setup(
    name="video_processing_project",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "torch",
        "pyannote.audio",
        "whisper",
    ],
    entry_points={
        "console_scripts": [
            "video_processing=main:main",
        ],
    },
)

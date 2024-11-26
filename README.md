# Ingescape Karaoke App

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Version](https://img.shields.io/badge/version-1.0.0-green.svg)

This is a Karaoke App developed in Python with the objective of having fun while leveraging Ingescape Circle to enable a Distributed Interactive System.

---

## Table of Contents
- [Dependencies](#dependencies)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)

---

## Dependencies

This project was built using:
- [Python 3.10](https://www.python.org/downloads/release/python-3100/)
- [Ingescape Circle](https://ingescape.com/fr/circle/)
- [The WhiteBoard](https://ingescape.com/)

If you don't have [Ingescape Circle](https://ingescape.com/fr/circle/), a full version of the app running exclusively with Python is available [here](#) soon.

To run the code, you need to install the following:

- [librosa](https://pypi.org/project/librosa/0.4.1/)
- [spleeter](https://pypi.org/project/spleeter/)
- [openai-whisper](https://github.com/openai/whisper)
- [pyaudio](https://pypi.org/project/PyAudio/)
- [pydub](https://pypi.org/project/pydub/)
- [pygame](https://pypi.org/project/pygame/)
- [simpleaudio](https://pypi.org/project/simpleaudio/)
- [sounddevice](https://pypi.org/project/sounddevice/)
- [Tkinter](https://docs.python.org/3/library/tkinter.html)
- [ingescape](https://pypi.org/project/ingescape/)

You might also need [ffmpeg](https://www.ffmpeg.org/download.html) if it's not installed.

---

## Installation and Setup

Provide step-by-step instructions for installing and setting up the project on Linux. These steps are practically the same for other OS distributions.

### Installing the Dependencies

Open a terminal and type the following commands:

```bash
# Clone the repository
git clone https://github.com/Andy-Mod/ingescape-karaoke-v1.0.git

# Navigate to the project directory
cd ingescape-karaoke-v1.0

# Install dependencies
pip install -r requirements.txt

# Install openai-whisper
pip install -U openai-whisper
```

### Downloading Data Files
Follow this [link](https://drive.google.com/file/d/1hvTD_66ktQRncpripQCPw5p4is-r3tAe/view?usp=sharing) to download the data files for the Karaoke App.
Once downloaded, move the files to the project's directory (ingescape-karaoke-v1.0).

### Setting Up the App
Open a new terminal and type the following commands:
```bash
# Navigate to the project directory
cd ingescape-karaoke-v1.0

# Launch the initial pre-treatment
python others/pretreatment.py
```
This process may take a little time, so feel free to grab a coffee while it runs.

### Instructions for File Cleanup

After the process is complete, please follow these steps:

1. Open the file located at `data/others/save_score.csv`.
2. Delete its contents, leaving only the first line in the file.
3. Ensure there are no new line characters after the first line.


## Usage

At this stage, everything should be ready. Ensure that Circle and the WhiteBoard are running and connected properly.
Choose the device and port on which you would like to run the application.

Open a new terminal and type the following commands:
```bash
# Navigate to the project directory
cd ingescape-karaoke-v1.0 

# Launch the Karaoke application
python src/KaraokeIngescape/src/main.py KaraokeIngescape --verbose --port chosen_port --device chosen_device
```
Open another terminal and type these commands:
```bash
# Navigate to the project directory
cd ingescape-karaoke-v1.0 

# Launch the Tretor application
python src/Tretor/src/main.py Tretor --verbose --port chosen_port --device chosen_device
```

You did it! The agents will soon be running in Circle. Once again, this might take a little time.


## Bugs and known problems 

While the lyrics display correctly on the Python interface, the whiteboard tends to crash due to the publishing rate. To prevent this issue, we decided to reduce the text publishing rate on the whiteboard. We are currently exploring better solutions to improve this further.


## Demonstration vides
Bellow are two links showing a demonstration usage of our project. 

-[Demonstration for the mode "Play"](https://drive.google.com/file/d/1Ib76d8nKLMKiJqejuFwXSiHBG6GfZW-Y/view?usp=drive_link)
-[Demonstration for the mode "Learn"](https://drive.google.com/file/d/17-2gZv649CS39icmuQXg55EkyAeONNXx/view?usp=sharing)
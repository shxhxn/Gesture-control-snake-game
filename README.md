# Gesture-Controlled Snake Game

A Python Snake game with three input modes: keyboard, webcam hand gestures, and voice commands. A CustomTkinter launcher brings the modes, settings, and score display into one desktop interface.

## Features

- Classic Snake gameplay built with Pygame
- Keyboard controls
- Real-time hand tracking with MediaPipe and OpenCV
- Voice direction commands through SpeechRecognition
- Desktop launcher with appearance, difficulty, speed, and score settings
- Direction validation that prevents instant 180° turns
- Wrap-around game board and self-collision detection

## Requirements

- Python 3.10+
- A webcam for gesture mode
- A working microphone and internet connection for voice recognition

## Setup

```bash
python -m venv .venv
```

Activate the environment, then install dependencies:

```bash
python -m pip install -r requirements.txt
```

> PyAudio installation can require platform-specific audio packages. If the normal install fails, follow the PyAudio instructions for your operating system.

## Run

Start the launcher:

```bash
python launcher.py
```

Or run a mode directly:

```bash
python snake_game.py
python gesture_control.py
python voice_control.py
```

Press `Esc` to close the webcam window in gesture mode.

## Project structure

| File | Purpose |
|---|---|
| `launcher.py` | Desktop launcher and settings UI |
| `snake_game.py` | Game state, rendering, and keyboard controls |
| `gesture_control.py` | Webcam hand tracking and gesture-to-direction mapping |
| `voice_control.py` | Spoken command recognition |
| `settings.json` | Local launcher preferences |

## Tech stack

Python · Pygame · MediaPipe · OpenCV · CustomTkinter · SpeechRecognition

## Privacy

Gesture processing runs locally from the webcam feed. Voice mode uses the speech-recognition service configured by the SpeechRecognition library and may send recorded audio to that service.

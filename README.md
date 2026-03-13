AIRCOMMAND

AirCommand is a computer vision–based system that enables touchless interaction with a computer using hand gestures. The system tracks hand movements through a webcam and translates them into desktop control actions such as cursor movement, clicking, scrolling, drawing, and typing through an on-screen keyboard.

The goal of the project is to explore human–computer interaction using vision-based input, allowing users to interact with a system without traditional peripherals like a mouse or keyboard.

Key Features

Gesture-Based Cursor Control
Real-time cursor movement using hand tracking
Smooth cursor control with movement smoothing and acceleration
Gesture-based click detection
Drag and drop support
Scroll Interaction
Three-finger gesture for vertical scrolling
Enables natural navigation through documents or web pages
Air Drawing Interface
Draw on screen using finger gestures
Canvas overlay for visual feedback
Color palette for selecting drawing colors
Gesture to clear the drawing canvas
Virtual Keyboard
On-screen keyboard interface
Characters can be typed using gesture-based pointer selection
Enables basic text input without physical keyboard usage
Calibration System
Records user hand movement boundaries
Maps hand movement range to full screen resolution
Improves cursor precision and control
Profile Persistence
Calibration data is saved locally
Automatically loaded during future sessions
Basic Voice Commands
Voice input is optionally supported for triggering certain actions such as opening common applications or switching modes.

System Overview

AirCommand processes webcam input in real time and converts detected hand landmarks into interaction commands.
The system workflow follows these stages:
Webcam captures live video frames.
MediaPipe detects hand landmarks.
Gesture interpretation determines the intended action.
Cursor control and system commands are executed through PyAutoGUI.
UI overlays provide drawing canvas and keyboard interaction.

Technologies Used

Python
OpenCV – real-time video processing
MediaPipe – hand landmark detection
PyAutoGUI – desktop control automation
NumPy – numerical operations
SpeechRecognition – optional voice input

Project Structure
AirCommand
│
├── core
│   ├── hand_tracker.py
│   ├── cursor_controller.py
│   ├── gesture_engine.py
│   ├── drawing_engine.py
│   ├── virtual_keyboard.py
│   ├── voice_engine.py
│   └── profile_manager.py
│
├── config.py
├── main.py
└── README.md
Installation

Clone the repository

git clone https://github.com/Harshitha0624/AirCommand.git
Navigate to the project directory
cd AirCommand
Create a virtual environment
python -m venv venv
Activate the environment

Windows:

venv\Scripts\activate
Install dependencies
pip install opencv-python mediapipe pyautogui numpy SpeechRecognition
Run the application
python main.py
Usage

After launching the application:

Move your index finger to control the cursor.
Use thumb gestures for clicking and dragging.
Raise three fingers to enable scrolling.
Use two-finger gestures to activate drawing mode.
Use the palette to change drawing colors.
Activate the virtual keyboard for text input.
Use calibration to improve cursor accuracy.
Potential Applications
Gesture-based computer interaction
Accessibility systems for hands-free control
Human–computer interaction research
Experimental touchless interfaces

Author
Harshitha Vasanth
Computer Science Engineering

License
This project is intended for educational and research purposes.

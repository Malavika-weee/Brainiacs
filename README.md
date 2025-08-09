<img width="3188" height="1202" alt="frame (3)" src="https://github.com/user-attachments/assets/517ad8e9-ad22-457d-9538-a9e62d137cd7" />


# [Project Name] 🎯


## Basic Details
### Team Name: [Name]


### Team Members
- Team Lead: Malavika V - MITS
- Member 1: Malavika V - MITS
- Member 2: Julie Johnson - MITS

### Project Description
This project is a real-time computer vision application that detects eye blinks using MediaPipe FaceMesh and delivers sarcastic, humorous feedback through both visual and audio responses. By analyzing the Eye Aspect Ratio (EAR) from detected facial landmarks, the system identifies intentional blinks and responds instantly with a randomly chosen sarcastic phrase, spoken aloud via a text-to-speech engine. A transparent sprite image or an emoji graphic is overlaid on the live webcam feed for added comedic effect.


### The Problem (that doesn't exist)
  Blinking is the most overlooked talent in human history. Nobody’s applauding you for those rapid eyelid gymnastics—and frankly, that’s a tragedy.




### The Solution (that nobody asked for)
We solve this by using cutting-edge blink detection to trigger sarcastic sprites and cheeky animations every time you blink. Blink once, get a wink back. Blink twice, enjoy the show!



## Technical Details
### Technologies/Components Used
For Software:
- Python – Primary programming language for the entire script.
- (None) – You are not using a large-scale application framework like Django, Flask, etc. Here, you are using libraries and APIs instead.
- [Libraries used]
- OpenCV (cv2) – Capturing video from webcam, image processing, rendering overlays, and displaying windows.

MediaPipe (mediapipe as mp) – FaceMesh solution for facial landmark detection (to get eye coordinates).

NumPy (numpy as np) – Array manipulation and image blending operations.

PIL (Pillow) – Opening and displaying images.

pyttsx3 – Text-to-speech engine for sarcastic phrase playback.

time – Measuring time intervals, cooldowns, and delays.

math – Calculating Euclidean distances for Eye Aspect Ratio (EAR).

threading – Running TTS in a separate background thread.

random – Randomly selecting sarcastic phrases.

os – Checking file existence for the sprite image.
- [Tools used]
- Webcam – Input device for capturing real-time video feed.

Python interpreter – Running the script.

System File Explorer – Storing and loading the PNG sprite image from disk.

Command-line/Terminal – Running and testing the program.

For Hardware:
-Main Components
Webcam Capture

Captures real-time video frames for processing.

Face Landmark Detection (MediaPipe FaceMesh)

Detects and tracks facial landmarks, focusing on eye regions.

Eye Aspect Ratio (EAR) Calculation

Computes EAR from eye landmarks to detect blinks.

Blink Detection Logic

Counts consecutive frames with eyes closed.

Implements cooldown to avoid multiple blink detections in quick succession.

Sarcastic Response Trigger

On blink detection, selects a random sarcastic phrase.

Uses text-to-speech (TTS) to speak the phrase asynchronously.

Sprite Image Overlay

Displays a sarcastic sprite image on the video frame when a blink is detected.

Falls back to drawing a simple emoji circle if sprite image is unavailable.

User Interface (OpenCV Window)

Shows video with overlayed blink count, EAR, sprite image, and controls exit on 'q' key press.

Specifications
Feature	Details
Blink Detection Threshold (EAR)	0.23 (can be tuned based on camera/face)
Consecutive Closed Frames for Blink	2 frames to confirm blink
Blink Cooldown	1.2 seconds between accepted blinks to avoid repeated detection
Sprite Scale	23% of video frame width for main sprite display
Sprite Show Time	1.6 seconds duration to show sprite after blink
FaceMesh Max Faces	1 (single face detection)
Text-to-Speech	pyttsx3 with rate 160 words/min
Fallback Graphics	Simple circle with sarcastic emoji if sprite not found
Overlay Position	Sprite shown top-right with margin; thumbnail bottom-right when idle

Tools Required
Tool/Resource	Purpose	Notes
Python 3.x Interpreter	Run the script	Python 3.6+ recommended
OpenCV (cv2)	Video capture, image processing	pip install opencv-python
MediaPipe	Face landmark detection	pip install mediapipe
NumPy	Array and image manipulation	pip install numpy
Pillow (PIL)	Image loading/display	pip install pillow
pyttsx3	Text-to-speech engine	pip install pyttsx3
Webcam	Video input	Ensure proper driver installed
Sprite Image File	Transparent PNG for overlay	Place file at specified path
IDE/Code Editor development and debugging  vs code pycharm etc

### Implementation
For Software:
# Installation
1. Setup Python Environment
Install Python 3.6 or higher.

Create a virtual environment (optional but recommended):

bash
CopyEdit
python -m venv blink_env
source blink_env/bin/activate  # Linux/Mac
blink_env\Scripts\activate     # Windows
2. Install Required Python Libraries
Run the following commands in your terminal or command prompt:

bash
CopyEdit
pip install opencv-python mediapipe numpy pillow pyttsx3
opencv-python: webcam capture & image processing

mediapipe: face landmark detection

numpy: numerical array processing

pillow: image display

pyttsx3: offline text-to-speech engine

3. Prepare Assets
Place your sarcastic sprite PNG image at the desired location (e.g., C:\Users\Julie Johnson\sarcastic_sprite.png).

Make sure the path in your script matches the sprite location exactly.

4. Implement the Python Script
Use your provided script (with necessary adjustments if needed).

Make sure the sprite image path (SPRITE_FILE) is correct.

The script will capture webcam video, detect eye blinks using MediaPipe FaceMesh, and display sarcastic phrases with TTS and sprite overlay.

5. Run the Script
Run the script from the terminal or your IDE:

A window titled "Sarcastic Blink Detector (press 'q' to quit)" will open showing the webcam feed.

Blink your eyes; sarcastic phrases will be spoken and a sprite will appear on blink detection.

6. Exiting the Program
Press 'q' in the window to quit cleanly.

Webcam and resources will release gracefully.

# Run

### Project Documentation
For Software:Sarcastic Blink Detector 😏👀
A fun computer vision project that detects your blinks using a webcam and responds with sarcastic comments, speech synthesis, and a cartoon sprite pop-up.

📌 Features
Real-time blink detection using MediaPipe Face Mesh.

Sarcastic commentary picked randomly from a phrase list.

Text-to-Speech (TTS) via pyttsx3 so your computer can roast you out loud.

Speech bubbles drawn directly on the webcam feed.

Sprite overlay (PNG with transparency) for extra sass.

Blink counter and Eye Aspect Ratio (EAR) display.

🛠️ Requirements
Python 3.8+

A working webcam

Recommended: virtual environment for dependencies

# Screenshots (Add at least 3)
![Screenshot1]<img width="879" height="600" alt="use" src="https://github.com/user-attachments/assets/0a66e51a-71de-4482-a1d1-5ec30096a20c" />
(intial setting of webcam)


![Screenshot2](<img width="1200" height="728" alt="use2" src="https://github.com/user-attachments/assets/06b93b45-0cc9-4165-b9cf-74ecdd3bf9ad" />
(catch record of movement of left and right eye)

![Screenshot3](<img width="1366" height="768" alt="Screenshot (1)" src="https://github.com/user-attachments/assets/95760562-4fe5-4f8b-b796-a8839a13d785" />
)
(throw sarcasmic comment when it detect blinks)

# Diagrams

For Hardware:<img width="1024" height="1536" alt="ChatGPT Image Aug 9, 2025, 06_46_35 AM" src="https://github.com/user-attachments/assets/dfce6f4f-8ae2-4fa8-a190-74eec8561ec5" />



### Project Demo
# Video
https://drive.google.com/file/d/1dbXEnfV25tfPCpuP94zL0nzKU5nzi7nJ/view?usp=drivesdk
*Explain what the video demonstrates*

# Additional Demos
[Add any extra demo materials/links]

## Team Contributions
- malavika: coding
- julie: coding
- 

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--25-25?link=https%3A%2F%2Fwww.tinkerhub.org%2Fevents%2FQ2Q1TQKX6Q%2FUseless%2520Projects)




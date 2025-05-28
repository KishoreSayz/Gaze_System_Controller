Eye-Controlled Mouse System
A hands-free mouse control solution enabling users to move the cursor and perform clicks through eye movements and blinks—ideal for accessibility applications and innovative HCI experiments.

Description
This project captures webcam video, detects facial and eye landmarks using MediaPipe, and translates eye motion into relative cursor movement via PyAutoGUI. Users can blink their left or right eye to simulate left- and right-clicks, respectively. Adjustable sensitivity, smoothing, and click thresholds ensure smooth, reliable control for individuals with motor impairments or for hands-free interaction scenarios.

🚀 Features
Eye-Based Cursor Control: Direct the mouse pointer by moving your eye.

Blink Clicks: Left-eye blink for left click; right-eye blink for right click.

Real-Time Processing: Webcam input with MediaPipe Face Mesh for instantaneous response.

Configurable Behavior: Tweak sensitivity, smoothing, blink thresholds, and cooldown.

🛠️ Built With
Python 3.7+

OpenCV – real-time computer vision.

MediaPipe – high-fidelity facial landmark detection.

PyAutoGUI – cross-platform GUI automation.

📦 Installation
Clone or download this repository.

Install dependencies:

bash
Copy
Edit
pip install opencv-python mediapipe pyautogui
Run the application:

bash
Copy
Edit
python systemcontrol.py
🎮 Controls
Move Cursor: Move your eye to direct the pointer.

Left Click: Blink left eye (landmarks 145 & 159).

Right Click: Blink right eye (landmarks 374 & 386).

Exit: Press Q.

🧪 How It Works
Video Capture: Grabs frames from the webcam.

Landmark Detection: MediaPipe Face Mesh locates facial landmarks.

Eye Tracking: A chosen eye landmark calculates movement delta.

Cursor Movement: PyAutoGUI moves the mouse relative to delta, with smoothing.

Blink Detection: Vertical distance between eyelid landmarks triggers clicks, with a cooldown timer.

⚙️ Customization
sensitivity: Scale factor for cursor speed.

smoothing_factor: Factor to reduce jitter.

left_click_threshold, right_click_threshold: Blink detection sensitivity.

click_cooldown: Minimum time between clicks.

🧩 Use Cases
Assistive technology for motor-impaired users.

Hands-free interfaces in sterile or VR/AR settings.

Research and prototyping in human-computer interaction.

📜 License
This project is released under the MIT License. See the LICENSE file for details.

🙌 Acknowledgments
MediaPipe Face Mesh for landmark detection.

OpenCV and PyAutoGUI for vision and control.

Inspiration from accessibility research and innovative UI design.








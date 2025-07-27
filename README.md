# AirClicker
# 🖐️ Hand Gesture Controlled Mouse using MediaPipe & PyAutoGUI

Control your computer's mouse using just your hand gestures and a webcam! This Python project uses **MediaPipe** to detect hand landmarks and **PyAutoGUI** to simulate mouse movement and clicks.

---

## 📸 Demo

> 📹 Add a GIF or video here showing your project in action.

---

## 🚀 Features

- Move mouse cursor using your **thumb position**
- Left-click when **thumb and index finger tips** come close
- Real-time hand tracking with webcam
- Beginner-friendly and lightweight

---

## 🧠 How It Works

- Uses **MediaPipe Hands** to detect 21 hand landmarks.
- Tracks:
  - **Thumb tip (ID 4)** → Controls cursor position
  - **Index tip (ID 8)** → Used to calculate distance from thumb for clicking
- If the distance between thumb and index is small → triggers a **mouse click** using `pyautogui`

---

## 🛠️ Requirements

Install the required Python libraries:

```bash
pip install opencv-python mediapipe pyautogui

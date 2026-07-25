# Gesture_Pilot  (REAL-TIME HAND FINGURE TRACKING MOUSE CURSOR)

Gesture_Pilot is a real-time hand gesture–controlled virtual mouse system developed using Python, OpenCV, MediaPipe, NumPy, and PyAutoGUI. The project is designed to enable touch-free human-computer interaction by allowing users to control cursor movement, perform mouse clicks, and scroll vertically using intuitive hand gestures detected through a webcam.

This project demonstrates how computer vision and hand tracking technologies can be applied to create practical, interactive systems that replace traditional input devices with natural body movements. Gesture_Pilot is intended for learning, experimentation, portfolio presentation, and further development in the fields of computer vision, gesture recognition, and human-computer interaction.

---

## Overview

Traditional mouse-based interaction depends on physical hardware input. Gesture_Pilot explores an alternative interaction model in which the user's hand becomes the primary control mechanism. By capturing live video from a webcam and processing it with MediaPipe hand landmark detection, the system tracks fingertip positions in real time and translates specific gesture patterns into mouse events.

The project focuses on three main goals:

1. delivering smooth and responsive cursor movement
2. improving gesture-based click recognition
3. creating a simple but effective touchless control experience

Gesture_Pilot is especially useful as a computer vision project for academic work, GitHub portfolios, project exhibitions, and practical demonstrations of real-time gesture tracking.

---

## Key Features

Gesture_Pilot includes the following capabilities:

- real-time hand tracking using webcam input
- smooth cursor movement based on index finger motion
- left click using thumb and index finger tap
- right click using thumb and middle finger tap
- vertical scrolling using index and middle finger touch gesture
- visual click animation and on-screen feedback
- gesture stability tuning to reduce accidental input
- low-latency interaction with dynamic movement smoothing

---

## Gesture Controls

| Gesture | Action |
|--------|--------|
| Move index finger | Move mouse cursor |
| Tap thumb + index finger | Left click |
| Tap thumb + middle finger | Right click |
| Touch index + middle finger and move vertically | Scroll up/down |

---

## Technology Stack

Gesture_Pilot is built with the following technologies:

- **Python** for application logic
- **OpenCV** for webcam capture and frame processing
- **MediaPipe** for hand landmark detection
- **NumPy** for mathematical operations
- **PyAutoGUI** for controlling system mouse actions

# System Requirements & Prerequisites

To ensure smooth execution of the **Gesture_Pilot** application, the system should meet the following hardware and software requirements.

---

## Minimum Hardware Requirements

| Component | Minimum Requirement | Recommended Specification |
|-----------|---------------------|---------------------------|
| **Processor (CPU)** | Dual-Core 2.0 GHz (Intel Core i3 / AMD Ryzen 3 or equivalent) | Intel Core i5 / AMD Ryzen 5 or higher |
| **Memory (RAM)** | 4 GB | 8 GB or more |
| **Storage** | 200 MB free disk space | SSD with 500 MB+ free space |
| **Graphics (GPU)** | Integrated Graphics | Dedicated NVIDIA/AMD GPU (Optional) |
| **Camera** | 720p USB or Built-in Webcam | 1080p Webcam at 30 FPS or above |
| **Display Resolution** | 1366 × 768 | 1920 × 1080 (Full HD) |

---

## Software Requirements

| Software | Version |
|----------|---------|
| **Operating System** | Windows 10/11, Ubuntu 20.04+, macOS 10.15 or later |
| **Python** | Python 3.9 – 3.11 (Recommended: Python 3.10) |
| **IDE / Code Editor** | Visual Studio Code, PyCharm, Spyder, or Jupyter Notebook |
| **Package Manager** | pip (Latest Version Recommended) |

---

## Python Dependencies

The project requires the following Python libraries.

| Library | Purpose |
|---------|---------|
| **opencv-python** | Captures webcam video and performs image processing. |
| **mediapipe** | Detects and tracks 21 hand landmarks in real time. |
| **numpy** | Performs numerical computations, coordinate calculations, and distance measurements. |
| **pyautogui** | Controls the system mouse for cursor movement, clicking, and scrolling. |
| **math** | Calculates Euclidean distances and geometric measurements. *(Built-in)* |
| **time** | Measures frame processing time and FPS calculations. *(Built-in)* |
| **platform** | Detects the operating system for platform-specific configurations. *(Built-in)* |

---

## Camera Requirements

For accurate hand detection and smooth cursor control, the webcam should satisfy the following conditions:

- Resolution of **720p (1280×720)** or higher.
- Minimum **30 Frames Per Second (FPS)**.
- Autofocus support is recommended.
- Stable mounting position.
- Entire hand should remain visible within the camera frame.
- Maintain a distance of **0.5 to 1.5 meters** from the webcam.

---

## Recommended Operating Environment

The performance of Gesture_Pilot depends significantly on the surrounding environment.

### Lighting Conditions
- Bright and uniform indoor lighting.
- Avoid dim environments.
- Minimize shadows on the hand.
- Avoid direct sunlight into the camera.

### Background
- Plain or uncluttered background.
- Avoid backgrounds containing hand-like objects or excessive movement.
- Ensure sufficient contrast between the hand and background.

### User Position
- Face the camera directly.
- Keep the hand comfortably within the camera's field of view.
- Avoid rapid hand movements during gesture execution.
- Maintain a natural distance for stable landmark tracking.

---

## Supported Features

Gesture_Pilot currently supports the following mouse operations:

- Real-time mouse cursor movement
- Left mouse click
- Right mouse click
- Double click
- Vertical scrolling
- Smooth cursor movement using interpolation
- Gesture recognition using 21 MediaPipe hand landmarks
- Live webcam visualization
- FPS (Frames Per Second) monitoring

---

## Installation Requirements

Before running the project, ensure that Python and all required libraries are installed.

Install the dependencies using:

```bash
pip install -r requirements.txt
```

or install them individually:

```bash
pip install opencv-python
pip install mediapipe
pip install numpy
pip install pyautogui
```

---

## Performance Recommendations

For the best user experience:

- Close unnecessary background applications.
- Use a webcam capable of at least **30 FPS**.
- Prefer a Full HD (1080p) display.
- Ensure adequate ambient lighting.
- Keep the webcam lens clean.
- Use Python 3.10 for optimal MediaPipe compatibility.
- Run the application on a modern multi-core processor for higher frame rates.

---

## Compatibility

Gesture_Pilot has been designed to be cross-platform and supports:

- Windows 10
- Windows 11
- Ubuntu Linux (20.04 or later)
- macOS Catalina (10.15) or later

---

## Notes

- Administrator privileges are generally **not required**.
- An active webcam connection is mandatory.
- Mouse control permissions may need to be granted on macOS.
- Ensure no other application is exclusively using the webcam.
- The application performs entirely on the local system and does not require an internet connection after installation.

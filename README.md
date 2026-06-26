<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FFD1DC,100:FF9EBB&height=200&section=header&text=Lane%20Line%20Detection&fontSize=42&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Real-time%20Road%20Lane%20Detection%20for%20Autonomous%20Navigation&descAlignY=55&descSize=18" width="100%"/>

<a href="https://github.com/your-username/lane-detection">
  <img src="https://readme-typing-svg.demolab.com?font=Fira+Code&size=22&duration=3000&pause=800&color=FF69B4&center=true&vCenter=true&width=600&lines=Detecting+lanes+in+real+time...;Canny+Edges+%E2%9E%9C+Hough+Transform+%E2%9E%9C+Lane+Fit;Built+for+Autonomous+Vehicle+Navigation+%F0%9F%9A%97" alt="Typing SVG" />
</a>

<br/>

![Python](https://img.shields.io/badge/Python-3.8+-FFB6C1?style=for-the-badge&logo=python&logoColor=801336)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-FFC0CB?style=for-the-badge&logo=opencv&logoColor=801336)
![NumPy](https://img.shields.io/badge/NumPy-1.24+-FFD1DC?style=for-the-badge&logo=numpy&logoColor=801336)
![License](https://img.shields.io/badge/License-MIT-FF9EBB?style=for-the-badge&logoColor=801336)
![Status](https://img.shields.io/badge/Status-Active-FF69B4?style=for-the-badge&logoColor=ffffff)

</div>

---
<img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNG8zaGl3eHd2MTl5anZpcDV4dHhtZ2J3ZTI1MmdmdTN1ZmgzZnByMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/3o7TKsQ8UQ0bMQGgwk/giphy.gif" width="70%" alt="lane detection demo placeholder"/>


</div>

---

## 🚦 Overview

This project implements a **computer-vision pipeline** that detects and highlights
road lane lines in both **images and video streams** — a foundational perception
module used in **Advanced Driver Assistance Systems (ADAS)** and autonomous
vehicle navigation stacks.

```mermaid
flowchart LR
    A[📷 Frame] --> B[⬛ Grayscale]
    B --> C[🌫️ Gaussian Blur]
    C --> D[✨ Canny Edge Detection]
    D --> E[📐 ROI Masking]
    E --> F[📏 Hough Transform]
    F --> G[➗ Slope/Intercept Averaging]
    G --> H[🎯 Temporal Smoothing]
    H --> I[🟩 Lane Overlay Output]
```

---

## ✨ Features

| | Feature |
|---|---|
| 🖼️ | Detects lanes in **static images** |
| 🎬 | Processes **video files frame-by-frame** |
| 📊 | Generates a **pipeline-stages figure** for reports/presentations |
| 🌊 | **Temporal smoothing** for jitter-free video output |
| 🟢 | Shaded **drivable-corridor** overlay between lanes |
| ⚡ | Lightweight — only `OpenCV` + `NumPy`, real-time capable |

---

## 📂 Project Structure

```
lane_detection/
├── lane_detection.py     # Core CV pipeline (importable module)
├── main.py                # CLI — image / video / debug modes
├── generate_test_data.py  # Synthetic road image + video generator
├── requirements.txt
├── images/                # Input images
├── videos/                # Input videos
└── output/                # Annotated results
```

---

## 🛠️ Installation

```bash
git clone https://github.com/your-username/lane-detection.git
cd lane-detection

python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

pip install -r requirements.txt
```

---

## ▶️ Usage

### Generate sample test data
```bash
python3 generate_test_data.py
```

### Detect lanes in an image
```bash
python3 main.py --mode image --input images/sample_road.jpg --output output/result.jpg
```

### Detect lanes in a video
```bash
python3 main.py --mode video --input videos/sample_road.mp4 --output output/result.mp4
```

### Generate a pipeline-stages figure
```bash
python3 main.py --mode debug --input images/sample_road.jpg --output output/pipeline_stages.jpg
```

---

## 🧩 Use as a Library

```python
import cv2
from lane_detection import process_frame, LaneSmoother

frame = cv2.imread("images/sample_road.jpg")
annotated = process_frame(frame)
cv2.imwrite("output/result.jpg", annotated)

# For video — reuse a smoother across frames for stability
smoother = LaneSmoother(buffer_size=8)
for frame in video_frames:
    annotated = process_frame(frame, smoother=smoother)
```

---

## 🎛️ Tuning Guide

| Parameter | Location | Effect |
|---|---|---|
| `low_threshold` / `high_threshold` | `detect_edges()` | Canny sensitivity |
| ROI `vertices` | `region_of_interest()` | Search trapezoid shape — match your camera FOV |
| `threshold`, `minLineLength`, `maxLineGap` | `hough_transform()` | Line segment detection strictness |
| `abs(slope) < 0.3` | `average_slope_intercept()` | Filters near-horizontal false positives |
| `buffer_size` | `LaneSmoother` | Smoothness vs. responsiveness on curves |

---

## 🗺️ Roadmap

- [ ] Perspective (bird's-eye) transform + polynomial curve fitting
- [ ] HSV/HLS color thresholding for yellow lane markings
- [ ] Deep-learning segmentation (LaneNet / SCNN)
- [ ] Kalman-filter based lane tracking
- [ ] Sensor fusion with LiDAR/radar


## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF9EBB,100:FFD1DC&height=120&section=footer" width="100%"/>

## 👨‍💻 Developer

<div align="center">

<img src="https://github.com/Akash22-11.png" width="100" style="border-radius:50%;"/>

### Akash

**Engineering Student • Data Science Enthusiast • Builder**

<img src="https://img.shields.io/badge/GitHub-Akash22--11-7C3AED?style=for-the-badge&logo=github&logoColor=white&labelColor=0D0B1F"/>

</div>

<br/>

<img src="https://raw.githubusercontent.com/andreasbm/readme/master/assets/lines/rainbow.gif" width="100%">

<div align="center">
⭐ **If this project helped you, consider giving it a star!** ⭐

</div>

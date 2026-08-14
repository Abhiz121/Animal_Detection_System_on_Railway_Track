# 🚆 Animal Detection on Railway Track

A real-time computer vision system that detects animals on railway tracks using **YOLOv8** and triggers **instant alerts** (audio + Slack notification) to help prevent train-animal collisions.

📄 **Published research paper:** [Animal Detection on Railway Track — IRJMETS, May 2025](https://www.irjmets.com/paperdetail.php?paperId=087c57891780fa99df274722cd705075)

---

## 🎯 Overview

Animal intrusions on railway tracks are a major safety hazard, causing accidents, train delays, and animal fatalities. This project uses a custom-trained YOLOv8 object detection model to monitor a live video feed, detect animals in real time, and immediately alert operators through sound and Slack notifications — enabling faster response and safer railway operations.

## ✨ Features

- **Real-time detection** from a live camera feed using a custom-trained YOLOv8 model
- **Confidence-based filtering** to reduce false positives
- **Audio alerts** on detection (local beep alarm)
- **Slack integration** for instant remote notifications, with a cooldown timer to prevent alert spam
- **Web dashboard** (Flask) to view the live annotated video feed in a browser
- **Bounding box visualisation** for detected animals on-screen

## 🏗️ How It Works

1. **Training** (`Animal detection.py`) — Fine-tunes a YOLOv8n model on a custom-labelled animal-detection dataset (50 epochs, 640px image size).
2. **Inference** — The trained weights (`best.pt`) are loaded to run detection on a live video stream frame-by-frame.
3. **Alerting** — When detection confidence crosses a set threshold, the system plays a local audio beep and sends a Slack alert (rate-limited via a cooldown window).
4. **Web Dashboard** (`app.py`) — Serves the annotated live feed over Flask so it can be monitored from a browser instead of a local OpenCV window.

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Object Detection | YOLOv8 (Ultralytics) |
| Computer Vision | OpenCV |
| Web Framework | Flask |
| Alerting | Slack Webhooks, winsound |
| Language | Python |

## 📁 Project Structure

animal-detection-railway-track/
├── Animal detection.py    (Standalone real-time detection - OpenCV window)
├── alerts.py               (Slack alert helper function)
├── app.py                  (Flask web app for browser-based live detection dashboard)
├── templates/
│   └── index.html          (Web dashboard page - renders the video feed)
├── requirements.txt
└── README.md

## ⚙️ Setup & Installation

### 1. Clone the repository
git clone https://github.com/<your-username>/animal-detection-railway-track.git
cd animal-detection-railway-track

### 2. Install dependencies
pip install -r requirements.txt

### 3. Configure the Slack webhook
Set your Slack webhook URL as an environment variable, never hardcode it.

Windows (PowerShell):
setx SLACK_WEBHOOK_URL "your-webhook-url-here"

macOS/Linux:
export SLACK_WEBHOOK_URL="your-webhook-url-here"

### 4. Add your trained model
Place your trained best.pt weights inside runs/detect/train/weights/best.pt relative to the project root.

## ▶️ Usage

Run real-time detection (local OpenCV window):
python "Animal detection.py"
Press q to quit.

Run the web dashboard:
python app.py
Then open http://127.0.0.1:5000 in your browser to view the live annotated feed.

## 📊 Results

- Model: YOLOv8n, trained for 50 epochs at 640x640 resolution
- Final mAP50: 57.9%
- Validated across varied lighting and track conditions
- Full methodology and evaluation results are detailed in the published paper: https://www.irjmets.com/paperdetail.php?paperId=087c57891780fa99df274722cd705075

## 🚀 Future Improvements

- Train with a larger dataset and data augmentation to improve accuracy
- Test larger YOLOv8 backbones (yolov8s / yolov8m) to trade inference speed for higher precision
- Add species-level classification, not just binary animal/no-animal detection
- Deploy on edge hardware (Jetson Nano/Raspberry Pi) for on-site trackside monitoring
- Replace polling-based Slack alerts with a persistent alert queue for reliability

## 📄 Citation

If you reference this work, please cite:
Singh, A. (2025). Animal Detection on Railway Track. International Research Journal of Modernization in Engineering Technology and Science (IRJMETS), May 2025.

## 👤 Author

Abhishek Singh
LinkedIn: linkedin.com/in/abhishek-singh
Email: as1311757@gmail.com

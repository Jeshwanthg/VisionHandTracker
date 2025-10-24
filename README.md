# 👁️ VisionHandTracker

A lightweight and efficient **real-time hand tracking module** built using **OpenCV** and **MediaPipe**.

---

## 📁 Project Structure

VisionHandTracker/
│
├── hand_tracking.py # Main script
├── requirements.txt # Dependencies
└── README.md

---

## ⚙️ Features
- Detects up to **2 hands** in real time  
- Tracks **21 hand landmarks** (fingers, joints, wrist)  
- Displays **live FPS** on video feed  
- Easily reusable for **gesture or sign recognition** tasks  

---

## 🚀 How It Works
1. Captures webcam feed using **OpenCV**  
2. Converts frames from **BGR → RGB** for MediaPipe  
3. Detects and draws hand landmarks  
4. Extracts landmark positions (x, y coordinates)  
5. Calculates and displays FPS live  

---

## 💻 Setup
```bash
git clone https://github.com/<your-username>/VisionHandTracker.git
cd VisionHandTracker
pip install -r requirements.txt
python hand_tracking.py

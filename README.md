# 🚗 Driver Drowsiness Detection System

A real-time Driver Drowsiness Detection System built using Python, OpenCV, and MediaPipe. The application monitors the driver's eye movements and detects prolonged eye closure and yawning to identify signs of drowsiness. When drowsiness is detected, an alarm is triggered to alert the driver.

## 📌 Features

- Real-time webcam-based monitoring
- Eye Aspect Ratio (EAR) calculation
- Detects prolonged eye closure
- Yawn detection
- Audio alarm for driver alert
- Live facial landmark visualization
- Displays EAR and mouth opening values

## 🛠 Technologies Used

- Python
- OpenCV
- MediaPipe Face Mesh
- Pygame
- Math Library

## 📂 Project Structure

```
Driver-Drowsiness-Detection-System/
│── driver.py
│── alarm.wav
│── README.md
│── requirements.txt
```

## ⚙ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/Driver-Drowsiness-Detection-System.git
```

Move into the project folder:

```bash
cd Driver-Drowsiness-Detection-System
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## ▶ Running the Project

```bash
python driver.py
```

Press **ESC** to exit the application.

## 🔍 How It Works

1. Captures live video from the webcam.
2. Detects facial landmarks using MediaPipe Face Mesh.
3. Calculates the Eye Aspect Ratio (EAR).
4. If the eyes remain closed for several consecutive frames, the system detects drowsiness.
5. Detects yawning based on the distance between the upper and lower lips.
6. Plays an alarm whenever drowsiness is detected.

## 📈 Future Improvements

- Head pose estimation
- Mobile notification support
- Email/SMS alerts
- Fatigue level analytics
- Driver monitoring dashboard
- Deep learning-based detection

## 👤 Author

Your Name

## 📄 License

This project is open-source and available under the MIT License.

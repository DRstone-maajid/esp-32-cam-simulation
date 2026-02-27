import requests
import cv2
import time

SERVER_URL = "https://web-production-a0194.up.railway.app/upload"
API_KEY = "n.maajid982010"  # SAME AS RAILWAY

cap = cv2.VideoCapture(0)  # Laptop webcam

while True:
    ret, frame = cap.read()
    if not ret:
        print("Camera error")
        break

    _, img = cv2.imencode(".jpg", frame)

    headers = {
        "X-ESP32-KEY": API_KEY,
        "Content-Type": "application/octet-stream"
    }

    try:
        r = requests.post(SERVER_URL, data=img.tobytes(), headers=headers, timeout=5)
        print("Upload:", r.status_code, r.text)
    except Exception as e:
        print("Error:", e)

    time.sleep(2)  # simulate ESP32 FPS

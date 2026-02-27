import requests
import cv2
import time

import os
import argparse

# default values can be overridden via environment or command-line arguments
SERVER_URL = os.environ.get('SERVER_URL', '').rstrip('/') + '/upload'
API_KEY = os.environ.get('UPLOAD_SECRET', '')  # same secret used by the Flask app

parser = argparse.ArgumentParser(description="ESP32 camera simulator")
parser.add_argument('--server', help='base URL of upload endpoint (without /upload)')
parser.add_argument('--key', help='API key / upload secret')
args = parser.parse_args()
if args.server:
    SERVER_URL = args.server.rstrip('/') + '/upload'
if args.key:
    API_KEY = args.key

if not SERVER_URL or not API_KEY:
    print("SERVER_URL and API_KEY must be set via environment or arguments")
    exit(1)

cap = cv2.VideoCapture(0)  # Laptop webcam (change index for multiple cameras)


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

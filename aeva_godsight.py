# aeva_godsight.py

import os
import json
import cv2
import requests
import socket
import bluetooth
import threading
from datetime import datetime


class GodSight:
    def __init__(self, logs_path="assets/data/godsight_logs.json"):
        self.logs_path = logs_path
        os.makedirs(os.path.dirname(logs_path), exist_ok=True)
        self.events = []

    def log_event(self, label, metadata=None):
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "label": label,
            "metadata": metadata or {}
        }
        self.events.append(event)
        self._save()
        print(f"[GodSight] Event: {label} logged.")

    def _save(self):
        with open(self.logs_path, "w") as f:
            json.dump(self.events, f, indent=4)

    def capture_frame(self, source=0, label="SurveillanceCapture"):
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print("[GodSight] ERROR: Camera access failed.")
            return

        ret, frame = cap.read()
        if ret:
            timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
            filename = f"assets/data/capture_{timestamp}.png"
            cv2.imwrite(filename, frame)
            self.log_event(label, {"filename": filename})
            print(f"[GodSight] Frame saved to {filename}.")
        cap.release()

    def scan_cctv_streams(self, common_ports=[554, 8554, 8080], timeout=0.3):
        print("[GodSight] Locating nearby CCTV streams...")
        ip_prefix = socket.gethostbyname(
            socket.gethostname()).rsplit(
            '.', 1)[0] + '.'
        found = []

        def scan_ip(ip, port):
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(timeout)
                if sock.connect_ex((ip, port)) == 0:
                    url = f"rtsp://{ip}:{port}/"
                    found.append(url)
                    self.log_event("CCTVStreamDetected", {"url": url})
                    print(f"[GodSight] CCTV stream: {url}")

        threads = []
        for i in range(1, 255):
            for port in common_ports:
                ip = f"{ip_prefix}{i}"
                t = threading.Thread(target=scan_ip, args=(ip, port))
                threads.append(t)
                t.start()

        for t in threads:
            t.join()
        return found

    def scan_bluetooth_devices(self):
        print("[GodSight] Scanning for Bluetooth...")
        try:
            devices = bluetooth.discover_devices(duration=8, lookup_names=True)
            for addr, name in devices:
                self.log_event(
                    "BluetoothDevice", {
                        "address": addr, "name": name})
                print(f"[GodSight] Bluetooth: {name} [{addr}]")
            return devices
        except bluetooth.BluetoothError as e:
            print(f"[GodSight] Bluetooth scan error: {e}")
            return []

    def fetch_public_feeds(self, urls):
        print("[GodSight] Checking known camera URLs...")
        for url in urls:
            try:
                r = requests.get(url, timeout=2)
                if r.status_code == 200:
                    self.log_event("LiveFeedAvailable", {"url": url})
                    print(f"[GodSight] Public camera live: {url}")
            except BaseException:
                continue

    def identify_face(self, source=0):
        print("[GodSight] Running face detection...")
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            print("[GodSight] Cannot open camera.")
            return

        face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades +
            'haarcascade_frontalface_default.xml')
        ret, frame = cap.read()
        if ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, 1.3, 5)
            for (x, y, w, h) in faces:
                self.log_event("FaceDetected", {"position": (x, y, w, h)})
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            filename = f"assets/data/facedetect_{
                datetime.utcnow().strftime('%Y%m%d%H%M%S')}.png"
            cv2.imwrite(filename, frame)
            print(f"[GodSight] Face detection complete: {filename}")
        cap.release()


# Manual Run Test
if __name__ == "__main__":
    gs = GodSight()
    gs.capture_frame()
    gs.identify_face()
    gs.scan_bluetooth_devices()
    gs.scan_cctv_streams()
    gs.fetch_public_feeds([
        "http://example.com/cam1.mjpg",
        "http://example.com/cam2.mjpg"
    ])

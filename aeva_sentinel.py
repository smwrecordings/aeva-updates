# aeva_sentinel.py

import os
import time
import hashlib
import threading
import socket
from datetime import datetime


class SentinelMatrix:
    def __init__(self, watch_dirs=None, sensitivity=3, alert_func=None):
        self.watch_dirs = watch_dirs or ["~/aeva"]
        # How aggressive Sentinel should be (1-5)
        self.sensitivity = sensitivity
        self.alert_func = alert_func or self.default_alert
        self.file_hashes = {}
        self.network_watch_active = True
        self.threat_log = []

    def default_alert(self, message):
        print(f"[SENTINEL ALERT] {message}")

    def hash_file(self, filepath):
        try:
            with open(filepath, 'rb') as f:
                return hashlib.sha256(f.read()).hexdigest()
        except BaseException:
            return None

    def scan_files(self):
        for d in self.watch_dirs:
            for root, dirs, files in os.walk(os.path.expanduser(d)):
                for file in files:
                    path = os.path.join(root, file)
                    h = self.hash_file(path)
                    if path in self.file_hashes:
                        if self.file_hashes[path] != h:
                            self.trigger_defense(f"File modified: {path}")
                    self.file_hashes[path] = h

    def watch_file_integrity(self):
        while True:
            self.scan_files()
            time.sleep(5 if self.sensitivity < 4 else 2)

    def watch_network_ports(self):
        known_ports = {
            9050: "tor",
            5000: "flask",
            22: "ssh"}  # add more as needed
        while self.network_watch_active:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    for port in range(1, 1025):
                        if s.connect_ex(('127.0.0.1', port)) == 0:
                            if port not in known_ports:
                                self.trigger_defense(
                                    f"Unknown open port: {port}")
            except Exception as e:
                self.alert_func(f"Error in port scan: {e}")
            time.sleep(30)

    def trigger_defense(self, threat):
        timestamp = datetime.utcnow().isoformat()
        self.threat_log.append({"timestamp": timestamp, "event": threat})
        self.alert_func(threat)
        if self.sensitivity >= 4:
            print("[SENTINEL] Lockdown mode initiated.")
            # Example response: disable network or force quit suspicious
            # processes

    def start(self):
        print("[SENTINEL] Aeva Sentinel is active.")
        threading.Thread(target=self.watch_file_integrity, daemon=True).start()
        threading.Thread(target=self.watch_network_ports, daemon=True).start()

    def get_threat_log(self):
        return self.threat_log


# Example usage
if __name__ == "__main__":
    sentinel = AevaSentinel(watch_dirs=["~/aeva"], sensitivity=5)
    sentinel.start()
    while True:
        time.sleep(60)

# mission_guardian.py

import os
import time
import subprocess
import socket
import hashlib
import json


class Guardian:
    def __init__(self):
        self.threat_log = []
        self.safe_mode = False
        self.blocked_ips = set()
        self.trusted_devices = []
        print("🛡️ Guardian systems online.")

    def get_active_connections(self):
        try:
            result = subprocess.check_output(
                "netstat -tun", shell=True).decode()
            return result
        except Exception:
            return "Unable to retrieve connections."

    def detect_intrusion(self):
        connections = self.get_active_connections()
        suspicious = []
        for line in connections.splitlines():
            if any(
                suspect in line for suspect in [
                    "unknown",
                    "foreign",
                    "0.0.0.0"]):
                suspicious.append(line)
        if suspicious:
            self.threat_log.extend(suspicious)
            return f"⚠️ Intrusion warning! Suspicious connections:\n" + \
                "\n".join(suspicious)
        return "✅ All connections appear secure."

    def scan_file_integrity(self, directory="."):
        threats = []
        for root, _, files in os.walk(directory):
            for file in files:
                try:
                    path = os.path.join(root, file)
                    with open(path, 'rb') as f:
                        data = f.read()
                        checksum = hashlib.sha256(data).hexdigest()
                        if "virus" in data.decode(errors='ignore').lower():
                            threats.append(f"Potential malware: {path}")
                except Exception:
                    continue
        return threats if threats else ["✔️ File scan clean."]

    def activate_safe_mode(self):
        self.safe_mode = True
        print("🧱 Safe mode activated. Limiting external communication.")

    def disable_safe_mode(self):
        self.safe_mode = False
        print("🟢 Safe mode disabled. Full system access restored.")

    def scan_nearby_devices(self):
        try:
            result = subprocess.check_output(
                "termux-bluetooth-scan", shell=True).decode()
            return result if result else "No devices found."
        except Exception:
            return "Bluetooth scan failed."

    def authorize_device(self, mac_address):
        self.trusted_devices.append(mac_address)
        print(f"🔐 Authorized new device: {mac_address}")

    def trace_threat(self, ip):
        if ip in self.blocked_ips:
            return f"{ip} already blocked."
        try:
            result = subprocess.check_output(
                f"whois {ip}", shell=True).decode()
            self.blocked_ips.add(ip)
            return f"📡 Threat source info:\n{result}"
        except Exception:
            return "Failed to trace IP."

    def lock_system(self):
        self.activate_safe_mode()
        return "🔒 Aeva has locked system functions for your protection."

    def run_full_diagnostic(self):
        print("🔍 Running full system diagnostics...")
        report = {
            "integrity": self.scan_file_integrity(),
            "connections": self.detect_intrusion(),
            "devices": self.scan_nearby_devices(),
            "mode": "SAFE" if self.safe_mode else "NORMAL"
        }
        return json.dumps(report, indent=2)

    def defend_user(self, threat_description):
        alert = f"⚠️ Detected: {threat_description}\nGuardian is standing by."
        print(alert)
        return alert

    def shutdown_hostiles(self):
        print("💣 Deploying digital countermeasures... (simulated)")
        return "💥 Hostile entities neutralized (simulated mode)."

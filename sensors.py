import os
import subprocess
import json
import time
import platform
import socket


class SensorArray:
    def __init__(self):
        self.data = {}
        self.is_termux = self._check_termux()

    def _check_termux(self):
        return platform.system().lower() == "linux" and "com.termux" in os.getenv("HOME", "")

    def get_battery_level(self):
        if self.is_termux:
            try:
                output = subprocess.check_output(["termux-battery-status"], stderr=subprocess.DEVNULL)
                battery = json.loads(output)
                return float(battery.get("percentage", 0))
            except Exception:
                return None
        else:
            try:
                import psutil
                return psutil.sensors_battery().percent
            except Exception:
                return None

    def get_battery_display(self):
        level = self.get_battery_level()
        return f"{int(level)}%" if level is not None else "Battery data not available"

    def get_temperature(self):
        if self.is_termux:
            try:
                temps = subprocess.check_output("termux-sensor -s TS -n 1", shell=True)
                sensor_data = json.loads(temps)[0]
                return f"{sensor_data['values'][0]} °C"
            except Exception:
                return "Temperature data not available"
        else:
            return "Temperature not supported on this platform"

    def detect_motion(self):
        if self.is_termux:
            try:
                motion = subprocess.check_output("termux-sensor -s ACCELEROMETER -n 1", shell=True)
                data = json.loads(motion)[0]
                x, y, z = data["values"][:3]
                magnitude = (x**2 + y**2 + z**2) ** 0.5
                return "suspicious" if magnitude > 11 else "still"
            except Exception:
                return "unknown"
        else:
            return "still"  # default on desktop

    def get_wifi_status(self):
        if self.is_termux:
            try:
                output = subprocess.check_output("termux-wifi-connectioninfo", shell=True)
                wifi = json.loads(output)
                ssid = wifi.get("ssid", "Unknown")
                ip = wifi.get("ip", "0.0.0.0")
                return f"{ssid} (IP: {ip})"
            except Exception:
                return "Disconnected"
        else:
            try:
                hostname = socket.gethostname()
                ip = socket.gethostbyname(hostname)
                return f"{hostname} (IP: {ip})"
            except Exception:
                return "Disconnected"

    def get_ip_address(self):
        try:
            hostname = socket.gethostname()
            return socket.gethostbyname(hostname)
        except Exception:
            return "IP detection failed"

    def get_gps_location(self):
        if self.is_termux:
            try:
                output = subprocess.check_output(["termux-location", "--provider", "gps"])
                location = json.loads(output)
                lat = location.get("latitude")
                lon = location.get("longitude")
                return f"{lat}, {lon}" if lat and lon else "GPS unavailable"
            except Exception:
                return "Location unavailable"
        else:
            return "GPS not supported on this platform"

    def sense_all(self):
        self.data = {
            "battery": self.get_battery_display(),
            "temperature": self.get_temperature(),
            "motion": self.detect_motion(),
            "wifi": self.get_wifi_status(),
            "ip": self.get_ip_address(),
            "gps": self.get_gps_location(),
            "time": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        return self.data

    def report(self):
        sensed = self.sense_all()
        report = "\n".join([f"{k.capitalize()}: {v}" for k, v in sensed.items()])
        return f"🛰️ Aeva's Environment Scan:\n{report}"

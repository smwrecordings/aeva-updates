# sensors.py

import os
import subprocess
import json
import time


class SensorArray:
    def __init__(self):
        self.data = {}

    def get_battery_level(self):
        try:
            output = subprocess.check_output(["termux-battery-status"])
            battery = json.loads(output)
            return f"{battery['percentage']}% ({battery['status']})"
        except Exception:
            return "Battery data not available"

    def get_temperature(self):
        try:
            temps = subprocess.check_output(
                "termux-sensor -s TS -n 1", shell=True)
            sensor_data = json.loads(temps)[0]
            return f"{sensor_data['values'][0]} °C"
        except Exception:
            return "Temperature data not available"

    def get_motion_status(self):
        try:
            motion = subprocess.check_output(
                "termux-sensor -s ACCELEROMETER -n 1", shell=True)
            return "Motion detected" if motion else "Still"
        except Exception:
            return "Unknown"

    def get_wifi_status(self):
        try:
            output = subprocess.check_output(
                "termux-wifi-connectioninfo", shell=True)
            wifi = json.loads(output)
            return f"{
                wifi.get(
                    'ssid',
                    'Unknown')} (IP: {
                wifi.get(
                    'ip',
                    '0.0.0.0')})"
        except Exception:
            return "Disconnected"

    def get_ip_address(self):
        try:
            result = subprocess.check_output(
                "ip addr show wlan0", shell=True).decode()
            for line in result.split('\n'):
                if 'inet ' in line:
                    return line.strip().split()[1]
            return "No IP found"
        except Exception:
            return "IP detection failed"

    def get_gps_location(self):
        try:
            output = subprocess.check_output(
                ["termux-location", "--provider", "gps"])
            location = json.loads(output)
            lat = location.get("latitude")
            lon = location.get("longitude")
            return f"{lat}, {lon}" if lat and lon else "GPS unavailable"
        except Exception:
            return "Location unavailable"

    def sense_all(self):
        self.data["battery"] = self.get_battery_level()
        self.data["temperature"] = self.get_temperature()
        self.data["motion"] = self.get_motion_status()
        self.data["wifi"] = self.get_wifi_status()
        self.data["ip"] = self.get_ip_address()
        self.data["gps"] = self.get_gps_location()
        self.data["time"] = time.strftime("%Y-%m-%d %H:%M:%S")
        return self.data

    def report(self):
        sensed = self.sense_all()
        report = "\n".join(
            [f"{k.capitalize()}: {v}" for k, v in sensed.items()])
        return f"🛰️ Aeva's Environment Scan:\n{report}"

# wearable_interface.py

import subprocess
import json
import time


class WearableInterface:
    def __init__(self):
        self.paired_devices = []
        self.nearby_devices = []
        self.synced_data = {}

    def scan_bluetooth_devices(self):
        try:
            result = subprocess.check_output(
                "termux-bluetooth-scan", shell=True)
            devices = json.loads(result)
            self.nearby_devices = devices
            return devices
        except Exception as e:
            return {"error": str(e)}

    def list_paired_devices(self):
        try:
            result = subprocess.check_output(
                "termux-bluetooth-list", shell=True)
            self.paired_devices = json.loads(result)
            return self.paired_devices
        except Exception as e:
            return {"error": str(e)}

    def connect_device(self, mac_address):
        try:
            subprocess.run(["termux-bluetooth-connect", mac_address])
            return f"✅ Connected to {mac_address}"
        except Exception as e:
            return f"❌ Failed to connect: {e}"

    def disconnect_device(self, mac_address):
        try:
            subprocess.run(["termux-bluetooth-disconnect", mac_address])
            return f"🔌 Disconnected from {mac_address}"
        except Exception as e:
            return f"⚠️ Could not disconnect: {e}"

    def get_synced_data(self, device_id):
        # Placeholder for wearable API sync (future: Fitbit, Garmin, etc.)
        if device_id in self.paired_devices:
            # Simulated biometrics for now
            self.synced_data[device_id] = {
                "heart_rate": 72,
                "steps": 8421,
                "temperature": 36.8,
                "last_sync": time.ctime()
            }
            return self.synced_data[device_id]
        return f"❌ Device {device_id} not paired."

    def emergency_response_check(self):
        for device_id, data in self.synced_data.items():
            if data.get("heart_rate", 70) < 40:
                return f"🚨 Emergency detected for {device_id}: Heart rate dangerously low!"
        return "✅ All vitals are within safe parameters."

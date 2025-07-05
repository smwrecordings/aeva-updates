# wearable_bridge.py

import subprocess
import json


class WearableBridge:
    def __init__(self):
        self.devices = []

    def scan_bluetooth_devices(self):
        """Use Termux API to scan for nearby Bluetooth devices."""
        try:
            print("🔍 Scanning for nearby Bluetooth devices...")
            result = subprocess.check_output(
                ["termux-bluetooth-scaninfo"]).decode()
            self.devices = json.loads(result)
            if not self.devices:
                return "📭 No Bluetooth devices found."

            formatted = "\n".join(
                f"🔹 {d.get('name', 'Unknown')} - {d.get('address', 'N/A')}" for d in self.devices
            )
            return f"📡 Devices found:\n{formatted}"
        except Exception as e:
            return f"❌ Bluetooth scan failed: {e}"

    def emergency_response_check(self):
        """Simulate a health/status query to wearables (expandable)."""
        if not self.devices:
            return "🚨 No connected wearables to check."

        # You can expand this to ping wearables or query status if connected
        names = ", ".join([d.get("name", "Unknown") for d in self.devices])
        return f"🛡 Emergency status normal across devices: {names}"

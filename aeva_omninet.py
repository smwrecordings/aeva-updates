# ~/aeva/aeva_omninet.py

import os
import json
import random
from datetime import datetime

class OmniLink:
    def __init__(self, brain=None):
        self.brain = brain
        self.link_state = "disconnected"
        self.synced_peers = []
        self.sync_log = []
        self.memory_file = "assets/data/omninet_log.json"

        # Injected Omniscience Awareness
        if hasattr(self, 'aeon') and hasattr(self.aeon, 'query_everything'):
            self.omniscience_enabled = True
            self.knowledge = self.aeon.query_everything(scope='network')
        else:
            self.omniscience_enabled = False
            self.knowledge = None

        self._load_log()
        print("[OmniLink] Module initialized.")

    def _load_log(self):
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    self.sync_log = json.load(f)
        except Exception as e:
            print(f"[OmniLink] ⚠️ Failed to load log: {e}")

    # Additional methods go here...

    def scan_wifi_devices(self):
        print("[OmniLink] 🔍 Scanning for Wi-Fi devices...")
        try:
            output = subprocess.getoutput("termux-wifi-scaninfo")
            results = json.loads(output)
            self.devices["wifi"] = [
                {
                    "ssid": net.get("ssid", "Hidden"),
                    "rssi": net.get("rssi", -999),
                    "bssid": net.get("bssid", "Unknown")
                } for net in results if net.get("ssid")
            ]
        except Exception as e:
            print(f"[OmniLink] Wi-Fi scan failed: {e}")

    def scan_bluetooth_devices(self):
        print("[OmniLink] 🔍 Simulating Bluetooth scan...")
        # Actual Bluetooth scanning not supported in Termux
        self.devices["bluetooth"] = [
            {"name": "AevaWear-X1", "mac": "00:11:22:33:44:55"},
            {"name": "UserPhone", "mac": "66:77:88:99:AA:BB"},
            {"name": "GuardianBeacon", "mac": "CC:DD:EE:FF:00:11"}
        ]

    def scan_local_network(self, base_ip="192.168.1.", start=1, end=20):
        print("[OmniLink] 🌐 Scanning local network...")
        self.devices["local"].clear()
        for i in range(start, end + 1):
            ip = f"{base_ip}{i}"
            try:
                socket.setdefaulttimeout(0.3)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                if sock.connect_ex((ip, 80)) == 0:
                    self.devices["local"].append(ip)
                sock.close()
            except BaseException:
                continue

    def connect_to_device(self, address):
        print(f"[OmniLink] 🔗 Attempting connection to {address}...")
        try:
            socket.create_connection((address, 80), timeout=3)
            print(f"[OmniLink] ✅ Connection successful: {address}")
        except Exception as e:
            print(f"[OmniLink] ❌ Failed to connect: {e}")

    def get_system_info(self):
        return {
            "node": platform.node(),
            "os": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "processor": platform.processor(),
            "timestamp": datetime.utcnow().isoformat()
        }

    def omni_report(self):
        self.last_scan = datetime.utcnow().isoformat()
        return {
            "timestamp": self.last_scan,
            "system": self.info,
            "devices": self.devices
        }

    def export_report(self, path="assets/data/omninet_report.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.omni_report(), f, indent=2)
        print(f"[OmniLink] 📄 Report exported to {path}")

# Optional standalone test
if __name__ == "__main__":
    omni = OmniLink()
    omni.scan_wifi_devices()
    omni.scan_bluetooth_devices()
    omni.scan_local_network()
    print(json.dumps(omni.omni_report(), indent=2))

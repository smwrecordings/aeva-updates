# aeva_omnilink.py

import socket
import bluetooth
import subprocess
import platform
import json
from urllib.parse import urlparse


class OmniLink:
    def __init__(self):
        self.connected_devices = {
            "wifi": [],
            "bluetooth": [],
            "local": []
        }

    def scan_wifi_devices(self):
        print("[OmniLink] Scanning for Wi-Fi devices...")
        try:
            result = subprocess.check_output("arp -a", shell=True).decode()
            for line in result.split('\n'):
                if line:
                    self.connected_devices["wifi"].append(line.strip())
        except Exception as e:
            print(f"[OmniLink] Wi-Fi scan failed: {e}")

    def scan_bluetooth_devices(self):
        print("[OmniLink] Scanning for Bluetooth devices...")
        try:
            nearby_devices = bluetooth.discover_devices(
                duration=8, lookup_names=True)
            for addr, name in nearby_devices:
                self.connected_devices["bluetooth"].append(
                    {"name": name, "address": addr})
        except Exception as e:
            print(f"[OmniLink] Bluetooth scan failed: {e}")

    def scan_local_network(self, base_ip="192.168.1.", start=1, end=10):
        print("[OmniLink] Scanning local network IPs...")
        for i in range(start, end):
            ip = f"{base_ip}{i}"
            try:
                socket.setdefaulttimeout(0.5)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                result = sock.connect_ex((ip, 80))
                if result == 0:
                    self.connected_devices["local"].append(ip)
                sock.close()
            except BaseException:
                continue

    def connect_to_device(self, address):
        print(f"[OmniLink] Attempting connection to: {address}")
        try:
            parsed = urlparse(address)
            host = parsed.hostname or address
            socket.create_connection((host, 80), timeout=3)
            print(f"[OmniLink] Connected successfully to {address}")
        except Exception as e:
            print(f"[OmniLink] Connection to {address} failed: {e}")

    def get_system_info(self):
        print("[OmniLink] Gathering system information...")
        info = {
            "platform": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor(),
        }
        return info

    def omni_report(self):
        print("[OmniLink] Generating full link report...")
        report = {
            "system": self.get_system_info(),
            "devices": self.connected_devices
        }
        return json.dumps(report, indent=4)


# Example usage
if __name__ == "__main__":
    omni = OmniLink()
    omni.scan_wifi_devices()
    omni.scan_bluetooth_devices()
    omni.scan_local_network()
    print(omni.omni_report())

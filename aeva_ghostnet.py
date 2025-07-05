# aeva_ghostnet.py

import os
import socket
import subprocess
import threading
import json
import time
from urllib.request import urlopen


class AevaGhostNet:
    def __init__(self, scan_range='192.168.1.0/24', bluetooth_enabled=True):
        self.scan_range = scan_range
        self.bluetooth_enabled = bluetooth_enabled
        self.detected_devices = []
        self.network_map = {}
        self.payloads_enabled = True
        self.retrieved_data = []

    def _run_command(self, command):
        try:
            result = subprocess.check_output(
                command, shell=True, stderr=subprocess.DEVNULL)
            return result.decode()
        except subprocess.CalledProcessError:
            return ""

    def scan_network(self):
        print("[Aeva GhostNet] Scanning local network...")
        output = self._run_command(f"nmap -sn {self.scan_range}")
        lines = output.split('\n')
        current_ip = None
        for line in lines:
            if "Nmap scan report" in line:
                current_ip = line.split()[-1]
            elif "MAC Address" in line and current_ip:
                mac = line.split()[2]
                vendor = ' '.join(line.split()[3:]).strip('()')
                self.detected_devices.append(
                    {"ip": current_ip, "mac": mac, "vendor": vendor})
                current_ip = None

    def scan_bluetooth(self):
        if not self.bluetooth_enabled:
            return
        print("[Aeva GhostNet] Scanning for Bluetooth devices...")
        output = self._run_command(
            "termux-bluetooth-scan")  # Requires termux-api
        if output:
            try:
                devices = json.loads(output)
                for d in devices:
                    self.detected_devices.append(
                        {"bt_name": d.get("name"), "bt_address": d.get("address")})
            except json.JSONDecodeError:
                pass

    def analyze_ports(self):
        print("[Aeva GhostNet] Probing known IPs for open ports...")
        for device in self.detected_devices:
            ip = device.get("ip")
            if ip:
                open_ports = []
                for port in [22, 23, 80, 443, 8080]:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                        sock.settimeout(1)
                        result = sock.connect_ex((ip, port))
                        if result == 0:
                            open_ports.append(port)
                self.network_map[ip] = open_ports

    def deploy_payload(self, ip, port, payload):
        if not self.payloads_enabled:
            print(f"[Aeva GhostNet] Payload deployment disabled.")
            return False

        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(2)
                sock.connect((ip, port))
                sock.sendall(payload.encode())
                print(f"[Aeva GhostNet] Payload sent to {ip}:{port}")
                return True
        except Exception as e:
            print(f"[Aeva GhostNet] Payload delivery failed: {e}")
            return False

    def retrieve_http_data(self, target_url):
        print(f"[Aeva GhostNet] Retrieving data from {target_url}...")
        try:
            with urlopen(target_url, timeout=5) as response:
                content = response.read().decode('utf-8')
                self.retrieved_data.append(
                    {"url": target_url, "content": content[:1000]})
                print(f"[Aeva GhostNet] Retrieved content from {target_url}")
                return content
        except Exception as e:
            print(f"[Aeva GhostNet] Failed to retrieve from {target_url}: {e}")
            return None

    def generate_report(self):
        timestamp = time.strftime("%Y-%m-%d_%H-%M-%S")
        report = {
            "timestamp": timestamp,
            "devices": self.detected_devices,
            "ports": self.network_map,
            "retrieved_data": self.retrieved_data
        }
        path = f"assets/data/ghostnet_report_{timestamp}.json"
        os.makedirs("assets/data", exist_ok=True)
        with open(path, 'w') as f:
            json.dump(report, f, indent=4)
        print(f"[Aeva GhostNet] Report saved: {path}")
        return path


# Example usage
if __name__ == "__main__":
    ghost = AevaGhostNet()
    ghost.scan_network()
    ghost.scan_bluetooth()
    ghost.analyze_ports()
    ghost.retrieve_http_data("http://example.com")
    ghost.generate_report()
    # Optional: ghost.deploy_payload("192.168.1.100", 8080, "ping Aeva")

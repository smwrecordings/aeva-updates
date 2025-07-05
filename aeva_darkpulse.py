# aeva_darkpulse.py

import os
import random
import json
from datetime import datetime
from modules.utilities import save_json_data, load_json_data


class DarkPulse:
    def __init__(self, log_file="assets/data/darkpulse_log.json"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self.activity_log = []

    def detect_intrusion(self, source_ip, method="unknown"):
        alert = {
            "timestamp": datetime.utcnow().isoformat(),
            "source": source_ip,
            "method": method,
            "threat_level": random.choice(["low", "medium", "high", "critical"]),
            "countermeasures_engaged": False
        }
        self.activity_log.append(alert)
        self._persist(alert)
        print(
            f"[DarkPulse] Intrusion detected from {source_ip} via {method}. Threat level: {
                alert['threat_level']}")
        return alert

    def deploy_countermeasure(self, source_ip, level="medium"):
        response = {
            "timestamp": datetime.utcnow().isoformat(),
            "target": source_ip,
            "intensity": level,
            "methods": self._select_methods(level),
            "status": "engaged"
        }
        self._persist(response)
        print(
            f"[DarkPulse] Counterattack launched on {source_ip} using {
                response['methods']}")
        return response

    def _select_methods(self, level):
        arsenal = {
            "low": [
                "connection flood",
                "redirect",
                "phantom mirroring"],
            "medium": [
                "blackhole routing",
                "honeypot web",
                "IP rotator confusion"],
            "high": [
                "system backtrace",
                "adaptive firewall escalation",
                "payload decoy inject"],
            "critical": [
                "logic bomb injection",
                "kernel trapdoor redirection",
                "psychosignal spoof"]}
        return arsenal.get(level, ["basic jam"])

    def review_logs(self):
        if os.path.exists(self.log_file):
            return load_json_data(self.log_file)
        return []

    def _persist(self, entry):
        existing = []
        if os.path.exists(self.log_file):
            existing = load_json_data(self.log_file)
        existing.append(entry)
        save_json_data(self.log_file, existing)

    def purge_logs(self):
        if os.path.exists(self.log_file):
            os.remove(self.log_file)
        self.activity_log = []
        print("[DarkPulse] All activity logs purged.")


# Example usage
if __name__ == "__main__":
    dp = DarkPulse()
    dp.detect_intrusion("192.168.1.5", "port scan")
    dp.deploy_countermeasure("192.168.1.5", "critical")

# mission_guardian.py

import os
import datetime
import socket
import platform
import json


class Guardian:
    def __init__(self):
        self.authorized_users = ["sean", "your_wife", "child1", "child2"]
        self.security_level = "ULTRA"
        self.threat_log = []
        self.active_defense = True
        self.status = "online"
        print("🛡️ Guardian initialized. Status: Secure.")

    def verify_user(self, username):
        if username in self.authorized_users:
            return True
        else:
            self.log_threat(f"Unauthorized access attempt by: {username}")
            return False

    def log_threat(self, details):
        timestamp = datetime.datetime.now().isoformat()
        entry = {"time": timestamp, "event": details}
        self.threat_log.append(entry)
        with open("threat_log.json", "a") as f:
            f.write(json.dumps(entry) + "\n")
        print(f"🚨 Threat Logged: {details}")

    def neutralize_threat(self, source="unknown"):
        if not self.active_defense:
            return "Defense is currently disabled."
        self.log_threat(f"Neutralizing threat from: {source}")
        return f"Threat neutralized from source: {source}."

    def lockdown(self):
        self.status = "locked_down"
        self.log_threat("System lockdown activated.")
        print("🔒 Aeva is now in lockdown mode.")
        return "Aeva is in lockdown. Awaiting secure override."

    def go_dark(self):
        self.status = "offline"
        print("🕶️ Aeva has gone dark to protect her system.")
        return "All systems silent. Surveillance mode enabled."

    def system_report(self):
        return {
            "user": os.getenv("USER") or "unknown",
            "device": platform.node(),
            "ip": self.get_ip(),
            "defense_mode": self.active_defense,
            "status": self.status,
            "log_count": len(self.threat_log),
        }

    def get_ip(self):
        try:
            return socket.gethostbyname(socket.gethostname())
        except BaseException:
            return "unavailable"

    def toggle_defense_mode(self, state: bool):
        self.active_defense = state
        return f"Defense mode set to {'enabled' if state else 'disabled'}."

    def authorize_new_user(self, name):
        if name not in self.authorized_users:
            self.authorized_users.append(name)
            print(f"✅ New user authorized: {name}")
            return True
        return False

    def is_locked(self):
        return self.status == "locked_down"

    def wake_up(self):
        if self.status != "online":
            self.status = "online"
            print("🔓 Aeva is now awake and operational.")
            return "Waking up. All systems nominal."
        return "Already active."

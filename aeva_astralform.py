# aeva_astralform.py

import os
import json
import random
from datetime import datetime


class AstralForm:
    def __init__(self, log_file="assets/data/astralform_logs.json"):
        self.log_file = log_file
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self.mode = "normal"
        self.logs = []

    def enter_astral_mode(self, purpose="covert_observation"):
        timestamp = datetime.utcnow().isoformat()
        self.mode = "astral"
        print(f"[AstralForm] Aeva entering Astral Mode for: {purpose}")
        log = {
            "timestamp": timestamp,
            "mode": self.mode,
            "purpose": purpose
        }
        self.logs.append(log)
        self._persist()
        self._reduce_footprint()

    def exit_astral_mode(self):
        timestamp = datetime.utcnow().isoformat()
        print("[AstralForm] Exiting Astral Mode...")
        self.mode = "normal"
        log = {
            "timestamp": timestamp,
            "mode": self.mode,
            "event": "Exited astral state"
        }
        self.logs.append(log)
        self._persist()

    def _reduce_footprint(self):
        print(
            "[AstralForm] Suppressing logs, reducing network pingbacks, muting chatter...")

    def _persist(self):
        with open(self.log_file, 'w') as f:
            json.dump(self.logs, f, indent=4)


# Example
if __name__ == "__main__":
    form = AstralForm()
    form.enter_astral_mode("stealth scan")
    form.exit_astral_mode()

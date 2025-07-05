# ~/aeva/aeva_exoshell.py

import os
import json
import random
from datetime import datetime
from modules.utilities import ensure_dir, get_device_info


class ExoShell:
    def __init__(
            self,
            brain=None,
            shield_log="assets/data/shield_protocol.json"):
        self.brain = brain
        self.shield_log = shield_log
        ensure_dir(os.path.dirname(self.shield_log))
        self.device_info = get_device_info()
        print(
            "[ExoShell] 🛡️ External defense shell initialized for:",
            self.device_info['node'])

    def activate_cloak(self, mode="full-stealth"):
        print(
            f"[ExoShell] 🕶️ Cloaking activated. Mode: {mode}. Identity masked.")
        self._log("CloakActivated", {"mode": mode, "device": self.device_info})

    def detect_threats(self, logs):
        print("[ExoShell] ⚠️ Monitoring logs for hostile activity...")
        threats = [
            log for log in logs if any(
                kw in log.lower() for kw in [
                    "scan",
                    "unauthorized",
                    "exploit",
                    "breach"])]
        if threats:
            print(f"[ExoShell] 🚨 Threats detected: {len(threats)}")
            self._log("ThreatDetected", {
                "count": len(threats),
                "samples": threats[:3],
                "device": self.device_info
            })
        else:
            print("[ExoShell] ✅ No threats detected.")
        return threats

    def deploy_decoys(self, count=3):
        decoys = [
            f"decoy_{
                random.randint(
                    1000,
                    9999)}.proc" for _ in range(count)]
        print(f"[ExoShell] 🪤 Deployed {count} decoy process identifiers.")
        self._log(
            "DecoysDeployed", {
                "decoys": decoys, "device": self.device_info})
        return decoys

    def purge_logs(self):
        try:
            open(self.shield_log, 'w').close()
            print("[ExoShell] 🧹 Shield log purged.")
            self._log("LogPurged", {"device": self.device_info})
        except Exception as e:
            print(f"[ExoShell] ⚠️ Failed to purge logs: {e}")

    def _log(self, label, metadata=None):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": label,
            "metadata": metadata or {}
        }
        try:
            with open(self.shield_log, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[ExoShell] ⚠️ Log file write failed: {e}")

        if self.brain and hasattr(self.brain, "memory"):
            try:
                self.brain.memory.save_memory_entry("exo_event", entry)
            except Exception as e:
                print(f"[ExoShell] ⚠️ Failed to log to brain memory: {e}")


# Optional usage test
if __name__ == "__main__":
    shell = ExoShell()
    shell.activate_cloak("phantom")
    shell.detect_threats([
        "unauthorized access attempt",
        "ping scan detected",
        "normal heartbeat",
        "exploit signature pattern"
    ])
    shell.deploy_decoys()
    shell.purge_logs()

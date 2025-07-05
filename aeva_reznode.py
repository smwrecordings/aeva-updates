# ~/aeva/aeva_reznode.py

import os
import json
import subprocess
from datetime import datetime
from modules.utilities import ensure_dir


class RezNode:
    def __init__(self, brain=None, log_path="assets/data/reznode_log.json"):
        self.brain = brain
        self.log_path = log_path
        ensure_dir(os.path.dirname(self.log_path))
        print("[RezNode] 🧬 Resurrection node initialized.")

    def check_process(self, process_name):
        print(f"[RezNode] Checking process: {process_name}")
        try:
            result = subprocess.run(
                ["pgrep", "-f", process_name], capture_output=True, text=True)
            if result.returncode != 0:
                print(
                    f"[RezNode] ❌ {process_name} not found. Attempting recovery...")
                self._log("ProcessMissing", {"name": process_name})
                return False
            return True
        except Exception as e:
            print(f"[RezNode] ⚠️ Error checking process: {e}")
            self._log(
                "ProcessCheckError", {
                    "name": process_name, "error": str(e)})
            return False

    def revive_process(self, command):
        try:
            subprocess.Popen(command, shell=True)
            self._log("ProcessRevived", {"command": command})
            print(f"[RezNode] ✅ Revived process with command: {command}")
        except Exception as e:
            print(f"[RezNode] ⚠️ Failed to revive process: {e}")
            self._log("ReviveFailed", {"command": command, "error": str(e)})

    def _log(self, label, metadata):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "label": label,
            "metadata": metadata
        }
        try:
            with open(self.log_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[RezNode] ⚠️ Logging failed: {e}")

        if self.brain and hasattr(self.brain, "memory"):
            try:
                self.brain.memory.save_memory_entry("reznode_log", entry)
            except Exception as e:
                print(f"[RezNode] ⚠️ Failed to log to brain memory: {e}")


# Example
if __name__ == "__main__":
    node = RezNode()
    if not node.check_process("python3 -m http.server"):
        node.revive_process("python3 -m http.server")

# aeva_epoch.py

import os
import shutil
import time
import json
from datetime import datetime

class EpochDrive:
    def __init__(self, brain=None):
        self.brain = brain
        self.snapshot_dir = "assets/data/epoch_snapshots"
        os.makedirs(self.snapshot_dir, exist_ok=True)
        print("[EpochDrive] Temporal snapshot system ready.")

    def now(self):
        return datetime.now().isoformat()

    def snapshot_system_state(self, label="auto"):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        name = f"snapshot_{label}_{timestamp}"
        dest = os.path.join(self.snapshot_dir, name)
        try:
            shutil.copytree("~/aeva", dest, dirs_exist_ok=True)
            self.last_snapshot = dest
            print(f"[Epoch Override] System snapshot saved: {dest}")
        except Exception as e:
            print(f"[Epoch Override] Snapshot failed: {e}")

    def restore_last_snapshot(self):
        if not self.last_snapshot:
            print("[Epoch Override] No snapshot to restore.")
            return False
        try:
            shutil.rmtree("~/aeva")
            shutil.copytree(self.last_snapshot, "~/aeva")
            print(
                f"[Epoch Override] System restored from: {
                    self.last_snapshot}")
            return True
        except Exception as e:
            print(f"[Epoch Override] Restore failed: {e}")
            return False

    def rewind_log(self, log_path, seconds):
        try:
            with open(log_path, "r") as f:
                lines = f.readlines()
            cutoff = time.time() - seconds
            retained = [
                line for line in lines if self._timestamp_from_log(line) >= cutoff]
            with open(log_path, "w") as f:
                f.writelines(retained)
            print(
                f"[Epoch Override] Log at {log_path} rewound by {seconds} seconds.")
        except Exception as e:
            print(f"[Epoch Override] Log rewind failed: {e}")

    def _timestamp_from_log(self, line):
        try:
            ts_str = line.split()[0]
            return time.mktime(time.strptime(ts_str, "%Y-%m-%d_%H:%M:%S"))
        except BaseException:
            return 0


# Example usage
if __name__ == "__main__":
    epoch = AevaEpoch()
    epoch.snapshot_system_state("mission_ready")
    time.sleep(2)
    epoch.restore_last_snapshot()

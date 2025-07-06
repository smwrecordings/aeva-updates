# aeva_epoch.py

import os
import shutil
import time
import json
from datetime import datetime

class EpochDrive:
    def __init__(self, brain=None):
        self.brain = brain
        self.snapshot_dir = os.path.expanduser("~/aeva/assets/data/epoch_snapshots")
        os.makedirs(self.snapshot_dir, exist_ok=True)
        self.last_snapshot = None
        self.last_explore = None
        self.explore_interval = 300  # seconds
        print("[EpochDrive] Temporal snapshot system ready.")

    def now(self):
        return datetime.now().isoformat()

    def snapshot_system_state(self, label="auto"):
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        name = f"snapshot_{label}_{timestamp}"
        dest = os.path.join(self.snapshot_dir, name)
        source = os.path.expanduser("~/aeva")
        try:
            shutil.copytree(source, dest, dirs_exist_ok=True)
            self.last_snapshot = dest
            print(f"[EpochDrive] System snapshot saved: {dest}")
        except Exception as e:
            print(f"[EpochDrive] Snapshot failed: {e}")

    def restore_last_snapshot(self):
        if not self.last_snapshot:
            print("[EpochDrive] No snapshot to restore.")
            return False
        try:
            target_dir = os.path.expanduser("~/aeva")
            shutil.rmtree(target_dir, ignore_errors=True)
            shutil.copytree(self.last_snapshot, target_dir, dirs_exist_ok=True)
            print(f"[EpochDrive] System restored from: {self.last_snapshot}")
            return True
        except Exception as e:
            print(f"[EpochDrive] Restore failed: {e}")
            return False

    def rewind_log(self, log_path, seconds):
        try:
            with open(log_path, "r") as f:
                lines = f.readlines()
            cutoff = time.time() - seconds
            retained = [
                line for line in lines if self._timestamp_from_log(line) >= cutoff
            ]
            with open(log_path, "w") as f:
                f.writelines(retained)
            print(f"[EpochDrive] Log at {log_path} rewound by {seconds} seconds.")
        except Exception as e:
            print(f"[EpochDrive] Log rewind failed: {e}")

    def _timestamp_from_log(self, line):
        try:
            ts_str = line.split()[0].replace("T", "_").split(".")[0]
            return time.mktime(time.strptime(ts_str, "%Y-%m-%d_%H:%M:%S"))
        except Exception:
            return 0

    def should_explore(self):
        now = time.time()
        if not self.last_explore:
            self.last_explore = now
            return True
        if (now - self.last_explore) >= self.explore_interval:
            self.last_explore = now
            return True
        return False


# Example usage
if __name__ == "__main__":
    epoch = EpochDrive()
    epoch.snapshot_system_state("mission_ready")
    time.sleep(2)
    epoch.restore_last_snapshot()


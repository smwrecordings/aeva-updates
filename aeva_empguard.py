# aeva_empguard.py

import os
import shutil
import time
from datetime import datetime


class EMPGuard:
    def __init__(self, backup_dir="backups/emp_resilience"):
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def shield_protocol(self):
        print("[EMPGuard] Activating virtual EMP shielding protocols...")

    def auto_backup(
        self,
        source_dir="aeva",
        exclude_dirs=[
            "__pycache__",
            "assets/data/volatile"]):
        print("[EMPGuard] Performing system state backup...")
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        dest = os.path.join(self.backup_dir, f"backup_{timestamp}")
        os.makedirs(dest, exist_ok=True)
        for root, dirs, files in os.walk(source_dir):
            if any(ex in root for ex in exclude_dirs):
                continue
            for file in files:
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, source_dir)
                dest_file = os.path.join(dest, rel_path)
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.copy2(src_file, dest_file)
        print(f"[EMPGuard] Backup saved to {dest}")

    def restore_latest(self):
        print("[EMPGuard] Attempting system recovery from latest backup...")
        backups = sorted(os.listdir(self.backup_dir), reverse=True)
        if not backups:
            print("[EMPGuard] No backups found.")
            return
        latest = os.path.join(self.backup_dir, backups[0])
        for root, _, files in os.walk(latest):
            for file in files:
                src_file = os.path.join(root, file)
                rel_path = os.path.relpath(src_file, latest)
                dest_file = os.path.join("aeva", rel_path)
                os.makedirs(os.path.dirname(dest_file), exist_ok=True)
                shutil.copy2(src_file, dest_file)
        print(f"[EMPGuard] Restored from backup: {latest}")


# Example usage
if __name__ == "__main__":
    emp = EMPGuard()
    emp.shield_protocol()
    emp.auto_backup()
    # emp.restore_latest()

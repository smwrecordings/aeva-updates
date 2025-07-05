import os
import importlib
import traceback
from datetime import datetime


class AevaSelfRepair:
    def __init__(
            self,
            modules_folder=".",
            backup_folder="backups",
            log_file="repair_log.txt"):
        self.modules_folder = modules_folder
        self.backup_folder = backup_folder
        self.log_file = log_file

    def log(self, message):
        timestamp = datetime.now().isoformat()
        with open(self.log_file, "a") as f:
            f.write(f"[{timestamp}] {message}\n")
        print(f"[Aeva-SelfRepair] {message}")

    def scan_and_repair(self):
        self.log("Running integrity check...")
        repaired = []

        for file in os.listdir(self.modules_folder):
            if file.startswith("aeva_") and file.endswith(".py"):
                path = os.path.join(self.modules_folder, file)
                if not self._validate_python_file(path):
                    self.log(
                        f"Corruption detected in {file}. Attempting recovery...")
                    backup_path = os.path.join(self.backup_folder, file)
                    if os.path.exists(backup_path):
                        with open(backup_path, "r") as b, open(path, "w") as f:
                            f.write(b.read())
                        self.log(f"Restored {file} from backup.")
                        repaired.append(file)
                    else:
                        self.log(f"No backup found for {file}. Skipped.")
        return repaired

    def _validate_python_file(self, path):
        try:
            with open(path, "r") as f:
                code = f.read()
            compile(code, path, "exec")
            return True
        except Exception:
            return False

    def monitor_crashes(self):
        try:
            for file in os.listdir(self.modules_folder):
                if file.startswith("aeva_") and file.endswith(".py"):
                    importlib.import_module(file.replace(".py", ""))
        except Exception as e:
            self.log("Crash detected during module loading.")
            self.log(traceback.format_exc())
            self.scan_and_repair()


if __name__ == "__main__":
    repair_system = AevaSelfRepair()
    repair_system.monitor_crashes()

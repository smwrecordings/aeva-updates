# aeva_coreos.py

import os
import sys
import json
from datetime import datetime

try:
    import psutil
except ImportError:
    psutil = None
    print("⚠️ psutil module not found. Some system metrics will be unavailable.")


class AevaCoreOS:
    def __init__(self):
        self.boot_time = "Unavailable"

        if psutil:
            try:
                self.boot_time = datetime.fromtimestamp(
                    psutil.boot_time()
                ).strftime("%Y-%m-%d %H:%M:%S")
            except PermissionError:
                print("⚠️ Permission denied: Unable to access boot time.")
                self.boot_time = "Restricted on Android"
            except Exception as e:
                print(f"⚠️ Error retrieving boot time: {e}")
                self.boot_time = "Unavailable"
        else:
            self.boot_time = "psutil not available"

        self.info = {
            "boot_time": self.boot_time,
            "cpu_count": os.cpu_count(),
            "load_avg": self.get_load_avg(),
            "platform": sys.platform
        }

    def get_load_avg(self):
        try:
            return os.getloadavg()
        except (AttributeError, OSError):
            return (0.0, 0.0, 0.0)

    def to_json(self):
        return json.dumps(self.info, indent=2)

    def kill_process(self, pid):
        try:
            os.kill(pid, 9)
            return f"🗡️ Process {pid} terminated."
        except PermissionError:
            return f"❌ Permission denied to kill process {pid}."
        except ProcessLookupError:
            return f"❌ No such process: {pid}."
        except Exception as e:
            return f"❌ Could not kill process {pid}: {e}"

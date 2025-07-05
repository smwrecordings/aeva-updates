# coreos.py

import os
import json
import psutil
import subprocess


class AevaCoreOS:
    def __init__(self):
        self.status = {}

    def to_json(self):
        self.status["cpu"] = psutil.cpu_percent(interval=1)
        self.status["memory"] = psutil.virtual_memory()._asdict()
        self.status["disk"] = psutil.disk_usage("/")._asdict()
        self.status["network"] = self._get_network_info()
        self.status["uptime"] = self.get_uptime()
        self.status["battery"] = self.get_battery()
        self.status["active_processes"] = self.list_processes()
        return json.dumps(self.status, indent=2)

    def get_uptime(self):
        try:
            with open("/proc/uptime", "r") as f:
                uptime_seconds = float(f.readline().split()[0])
                return f"{uptime_seconds // 3600:.0f} hours"
        except BaseException:
            return "Unknown"

    def get_battery(self):
        try:
            output = subprocess.check_output(
                "termux-battery-status", shell=True)
            return json.loads(output)
        except BaseException:
            return {"status": "Unavailable"}

    def _get_network_info(self):
        try:
            interfaces = psutil.net_if_addrs()
            info = {}
            for iface, addrs in interfaces.items():
                info[iface] = [
                    addr.address for addr in addrs if addr.family == 2]  # IPv4
            return info
        except Exception as e:
            return {"error": str(e)}

    def list_processes(self):
        try:
            procs = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                procs.append(proc.info)
            return sorted(
                procs,
                key=lambda x: x['cpu_percent'],
                reverse=True)[
                :10]
        except Exception as e:
            return [str(e)]

    def kill_process(self, pid):
        try:
            p = psutil.Process(pid)
            p.terminate()
            return f"✅ Process {pid} terminated."
        except psutil.NoSuchProcess:
            return f"❌ Process {pid} does not exist."
        except Exception as e:
            return f"⚠️ Error killing process: {e}"

import os
import platform
import subprocess
import webbrowser
import psutil
import json
import requests
from datetime import datetime
from threading import Thread


class AevaUI:
    def __init__(self):
        self.device = platform.node()
        self.os = platform.system()
        self.user = os.getenv("USER") or os.getenv(
            "USERNAME") or "Unknown User"
        self.session_start = datetime.now().isoformat()
        self.log_dir = "assets/data/ui_logs"
        os.makedirs(self.log_dir, exist_ok=True)
        self.history = []

    def log(self, entry):
        timestamp = datetime.now().isoformat()
        record = {"timestamp": timestamp, "entry": entry}
        self.history.append(record)

        log_path = os.path.join(
            self.log_dir, f"ui_{datetime.now().strftime('%Y-%m-%d')}.json"
        )
        with open(log_path, "w") as f:
            json.dump(self.history, f, indent=2)

        print(f"[AevaUI] {entry}")

    def greet_user(self):
        greeting = f"Welcome back, {
            self.user}. Today is {
            datetime.now().strftime('%A, %B %d, %Y')}"
        self.log(greeting)

    def run_command(self, command):
        self.log(f"Executing system command: {command}")
        try:
            result = subprocess.getoutput(command)
            self.log(f"Command result: {result[:500]}...")
            return result
        except Exception as e:
            self.log(f"Command failed: {str(e)}")
            return None

    def open_browser(self, url):
        self.log(f"Opening browser to: {url}")
        webbrowser.open(url)

    def quick_search(self, query):
        search_url = f"https://www.google.com/search?q={query}"
        self.open_browser(search_url)

    def show_status(self):
        self.log("Displaying system status.")
        status = {
            "Device": self.device,
            "OS": self.os,
            "Uptime": str(datetime.now() - datetime.fromtimestamp(psutil.boot_time())),
            "CPU Usage": f"{psutil.cpu_percent()}%",
            "Memory Usage": f"{psutil.virtual_memory().percent}%",
        }
        for k, v in status.items():
            print(f"{k}: {v}")

    def show_activity_log(self):
        self.log("Displaying recent activity log.")
        for entry in self.history[-10:]:
            print(f"{entry['timestamp']}: {entry['entry']}")

    def ask_user_input(self):
        self.log("Entering interactive mode.")
        while True:
            try:
                user_input = input("Aeva > ").strip()
                if user_input.lower() in ("exit", "quit"):
                    break
                elif user_input.startswith("open "):
                    self.open_browser(user_input[5:].strip())
                elif user_input.startswith("search "):
                    self.quick_search(user_input[7:].strip())
                else:
                    self.run_command(user_input)
            except KeyboardInterrupt:
                break
        self.log("Exiting interactive mode.")

    def auto_updates(self):
        self.log("Checking for updates (mocked)")
        print("[AevaUI] You are running the latest intelligence interface.")

    def background_health_monitor(self):
        def monitor():
            while True:
                cpu = psutil.cpu_percent(interval=5)
                mem = psutil.virtual_memory().percent
                if cpu > 85 or mem > 90:
                    self.log(
                        f"⚠ High resource usage detected: CPU {cpu}%, RAM {mem}%")

        thread = Thread(target=monitor, daemon=True)
        thread.start()

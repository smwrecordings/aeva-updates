import os
import platform
import psutil
import datetime
import subprocess
import webbrowser
import requests


class AevaAssist:
    def __init__(self):
        self.device_name = platform.node()
        self.os = platform.system()
        self.user = os.getenv("USER") or os.getenv("USERNAME")

    def provide_assistance(self):
        print("[AevaAssist] How can I help you today?")

    def check_status(self):
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(psutil.boot_time())
        mem = psutil.virtual_memory()
        print(f"[AevaAssist] Device: {self.device_name}")
        print(f"[AevaAssist] Uptime: {uptime}")
        print(f"[AevaAssist] OS: {self.os}")
        print(f"[AevaAssist] RAM Usage: {mem.percent}%")

    def open_website(self, url):
        print(f"[AevaAssist] Opening {url}")
        webbrowser.open(url)

    def search_web(self, query):
        print(f"[AevaAssist] Searching for: {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")

    def run_command(self, command):
        print(f"[AevaAssist] Executing command: {command}")
        result = subprocess.getoutput(command)
        print(result)

    def download_file(self, url, destination="downloads"):
        os.makedirs(destination, exist_ok=True)
        filename = os.path.join(destination, url.split("/")[-1])
        print(f"[AevaAssist] Downloading {url} to {filename}")
        response = requests.get(url)
        with open(filename, "wb") as f:
            f.write(response.content)
        print("[AevaAssist] Download complete.")

    def check_connection(self):
        try:
            requests.get("https://google.com", timeout=5)
            print("[AevaAssist] Internet connection active.")
        except requests.ConnectionError:
            print("[AevaAssist] No internet connection.")

    def summarize_memory_usage(self):
        print("[AevaAssist] Memory Summary:")
        print(psutil.virtual_memory())

    def list_processes(self):
        print("[AevaAssist] Active Processes:")
        for proc in psutil.process_iter(['pid', 'name']):
            print(f"{proc.info['pid']}: {proc.info['name']}")

    def shutdown(self):
        print("[AevaAssist] Initiating shutdown sequence.")
        if self.os == "Linux":
            os.system("shutdown now")
        elif self.os == "Windows":
            os.system("shutdown /s /t 1")
        else:
            print("[AevaAssist] Unsupported OS for shutdown command.")

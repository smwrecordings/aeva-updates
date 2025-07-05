# ~/aeva/timeline_visualizer.py

import json
import os
import time
from datetime import datetime

LOG_PATH = "memory/timeline.json"


class TimelineVisualizer:
    def __init__(self, path=LOG_PATH):
        self.path = path
        self.logs = []

    def load(self):
        if not os.path.exists(self.path):
            print("[Visualizer] No timeline log found.")
            return []
        with open(self.path, "r") as f:
            self.logs = json.load(f)
        return self.logs

    def display_recent(self, limit=10):
        self.load()
        recent = self.logs[-limit:]
        for entry in recent:
            self._print_entry(entry)

    def _print_entry(self, entry):
        ts = entry.get("timestamp", "Unknown time")
        event = entry.get("event", "NoEvent")
        data = entry.get("data", {})
        print(f"\n🕒 {ts} | 📌 {event.upper()}")
        for k, v in data.items():
            print(f"  ➤ {k}: {v}")

    def replay(self, delay=1):
        self.load()
        print("[Visualizer] Replaying timeline events...\n")
        for entry in self.logs:
            self._print_entry(entry)
            time.sleep(delay)

    def filter_by_type(self, event_type):
        self.load()
        filtered = [e for e in self.logs if e.get("event") == event_type]
        for entry in filtered:
            self._print_entry(entry)

    def search(self, keyword):
        self.load()
        results = []
        for entry in self.logs:
            if keyword.lower() in json.dumps(entry).lower():
                results.append(entry)
        for e in results:
            self._print_entry(e)


# Optional usage example
if __name__ == "__main__":
    tv = TimelineVisualizer()
    tv.display_recent()
    # tv.replay(delay=2)
    # tv.filter_by_type("dream_report")
    # tv.search("battery")

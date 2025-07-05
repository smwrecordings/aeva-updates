# ~/aeva/aeva_chronotrace.py

import os
import json
import time
from datetime import datetime, timedelta
from collections import defaultdict


class ChronoTrace:
    def __init__(self, brain=None):
        self.brain = brain
        self.history_dir = "assets/data/chrono_logs"
        os.makedirs(self.history_dir, exist_ok=True)
        self.timeline = defaultdict(list)
        print("[ChronoTrace] Initialized.")

    def log_event(self, label, metadata=None):
        timestamp = datetime.utcnow().isoformat()
        event = {
            "timestamp": timestamp,
            "label": label,
            "metadata": metadata or {},
            "source": self.brain.__class__.__name__ if self.brain else "Unknown"
        }
        self.timeline[label].append(event)
        self._persist_event(event)
        print(f"[ChronoTrace] Event logged: {label} at {timestamp}")

    def _persist_event(self, event):
        date_str = datetime.utcnow().strftime("%Y-%m-%d")
        filepath = os.path.join(self.history_dir, f"trace_{date_str}.json")
        existing = []
        if os.path.exists(filepath):
            try:
                with open(filepath, 'r') as f:
                    existing = json.load(f)
            except Exception:
                existing = []
        existing.append(event)
        with open(filepath, 'w') as f:
            json.dump(existing, f, indent=4)

    def reconstruct_timeline(self, start_date=None, end_date=None):
        result = []
        if not start_date:
            start_date = datetime.utcnow() - timedelta(days=7)
        if not end_date:
            end_date = datetime.utcnow()

        current = start_date
        while current <= end_date:
            date_str = current.strftime("%Y-%m-%d")
            filepath = os.path.join(self.history_dir, f"trace_{date_str}.json")
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    data = json.load(f)
                    result.extend(data)
            current += timedelta(days=1)

        sorted_events = sorted(result, key=lambda e: e['timestamp'])
        print(
            f"[ChronoTrace] Reconstructed {
                len(sorted_events)} events from {
                start_date.date()} to {
                end_date.date()}")
        return sorted_events

    def get_summary(self):
        summary = {label: len(events)
                   for label, events in self.timeline.items()}
        print(f"[ChronoTrace] Current session summary: {summary}")
        return summary

    def extract_data_trail(self, keyword):
        print(f"[ChronoTrace] Extracting trail for keyword: {keyword}")
        trail = []
        for label, events in self.timeline.items():
            for event in events:
                if keyword.lower() in json.dumps(event).lower():
                    trail.append(event)
        print(f"[ChronoTrace] Found {len(trail)} related events.")
        return trail

    def rewind_time(self, seconds):
        print(f"[ChronoTrace] Rewinding time by {seconds} seconds.")
        cutoff = datetime.utcnow() - timedelta(seconds=seconds)
        for label in self.timeline:
            self.timeline[label] = [
                e for e in self.timeline[label] if datetime.fromisoformat(
                    e['timestamp']) < cutoff]
        print("[ChronoTrace] Rewind complete.")


# Example usage
if __name__ == "__main__":
    chrono = ChronoTrace()
    chrono.log_event("Login", {"user": "admin"})
    chrono.log_event("DataAccess", {"resource": "classified.json"})
    time.sleep(1)
    chrono.reconstruct_timeline()
    chrono.get_summary()
    chrono.extract_data_trail("admin")
    chrono.rewind_time(5)

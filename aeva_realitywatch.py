# aeva_realitywatch.py

import os
import json
import hashlib
import random
import time
from datetime import datetime


class RealityWatch:
    def __init__(self, log_path="assets/data/reality_log.json"):
        self.log_path = log_path
        self.anomalies = []
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def _hash_event(self, event):
        return hashlib.sha256(
            json.dumps(
                event,
                sort_keys=True).encode()).hexdigest()

    def detect_timeline_shift(self, known_reference_time=None):
        now = datetime.utcnow()
        ref = known_reference_time or now
        drift_seconds = abs((now - ref).total_seconds())
        if drift_seconds > 30:
            self._log(
                "TimelineShiftDetected", {
                    "drift_seconds": drift_seconds})
        return drift_seconds

    def detect_variable_anomaly(self, value_stream, label="Unknown"):
        if not value_stream or len(value_stream) < 5:
            return False
        average = sum(value_stream) / len(value_stream)
        current = value_stream[-1]
        if abs(current - average) > (0.5 * average):
            self._log("AnomalousPatternDetected", {
                "label": label,
                "average": average,
                "current": current
            })
            return True
        return False

    def quantum_checksum(self, data_string):
        """Generate a pseudo-quantum checksum to verify temporal stability."""
        seed = f"{data_string}{random.random()}{time.time()}"
        checksum = hashlib.blake2b(seed.encode()).hexdigest()
        return checksum

    def _log(self, label, metadata):
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "label": label,
            "metadata": metadata
        }
        self.anomalies.append(event)
        self._save()
        print(f"[RealityWatch] Anomaly Logged: {label}")

    def _save(self):
        with open(self.log_path, "w") as f:
            json.dump(self.anomalies, f, indent=4)

    def summarize_events(self):
        summary = {}
        for event in self.anomalies:
            label = event['label']
            summary[label] = summary.get(label, 0) + 1
        return summary


# Example use
if __name__ == "__main__":
    rw = RealityWatch()
    rw.detect_timeline_shift()
    rw.detect_variable_anomaly([100, 102, 101, 99, 200], "EnergyFlux")
    print(rw.summarize_events())

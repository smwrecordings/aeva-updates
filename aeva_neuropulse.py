# aeva_neuropulse.py

import random
import time


class NeuroPulse:
    def __init__(self):
        self.biometric_stream = {
            "heart_rate": 72,
            "brainwave_state": "baseline",
            "breathing_rate": 14,
            "stress_index": 0.1,
        }

    def simulate_readings(self):
        # In real-world deployment this will interface with biometric sensors
        self.biometric_stream["heart_rate"] = random.randint(60, 100)
        self.biometric_stream["brainwave_state"] = random.choice(
            ["alpha", "beta", "gamma", "delta", "theta"])
        self.biometric_stream["breathing_rate"] = random.randint(12, 20)
        self.biometric_stream["stress_index"] = round(random.uniform(0, 1), 2)
        return self.biometric_stream

    def interpret_data(self):
        data = self.simulate_readings()
        print(f"[NeuroPulse] Interpreted biometric state: {data}")
        return data

    def detect_alerts(self):
        alerts = []
        data = self.simulate_readings()
        if data["heart_rate"] > 100:
            alerts.append("Elevated heart rate detected.")
        if data["stress_index"] > 0.7:
            alerts.append("High stress levels detected.")
        if data["brainwave_state"] in ["delta", "theta"]:
            alerts.append("User may be in a meditative or unconscious state.")
        if alerts:
            print(f"[NeuroPulse] ALERTS: {alerts}")
        return alerts


# Example
if __name__ == "__main__":
    pulse = NeuroPulse()
    pulse.interpret_data()
    pulse.detect_alerts()

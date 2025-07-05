# aeva_resonance.py

import os
import json
import time
import numpy as np
import sounddevice as sd
from datetime import datetime
from scipy.io.wavfile import write


class ResonanceCore:
    def __init__(self, log_path="assets/data/resonance_logs.json"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.session_log = []

    def _log_event(self, action, details=None):
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "action": action,
            "details": details or {}
        }
        self.session_log.append(event)
        with open(self.log_path, "w") as f:
            json.dump(self.session_log, f, indent=4)
        print(f"[ResonanceCore] Logged event: {action}")

    def generate_tone(
            self,
            frequency=528.0,
            duration=5.0,
            amplitude=0.3,
            filename=None):
        print(
            f"[ResonanceCore] Generating tone: {frequency}Hz for {duration}s")
        sample_rate = 44100
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        tone = np.sin(2 * np.pi * frequency * t) * amplitude
        sd.play(tone, sample_rate)
        sd.wait()
        if filename:
            write(filename, sample_rate, (tone * 32767).astype(np.int16))
        self._log_event(
            "GenerateTone", {
                "frequency": frequency, "duration": duration})

    def healing_sequence(self, profile="chakra"):
        print("[ResonanceCore] Starting healing sequence...")
        frequencies = {
            "chakra": [396, 417, 528, 639, 741, 852, 963],
            "sleep": [174, 285, 396, 417],
            "focus": [432, 528, 639]
        }.get(profile, [528])
        for freq in frequencies:
            self.generate_tone(freq, duration=3.0)
        self._log_event("HealingSequence", {"profile": profile})

    def ultrasonic_ping(self, frequency=20000.0, duration=0.5):
        print(f"[ResonanceCore] Sending ultrasonic ping at {frequency}Hz")
        self.generate_tone(frequency, duration)
        self._log_event("UltrasonicPing", {"frequency": frequency})

    def echolocation_pulse(self):
        print("[ResonanceCore] Emitting sonar-like pulse...")
        freqs = [18000, 20000, 22000]
        for f in freqs:
            self.generate_tone(f, duration=0.2)
        self._log_event("EcholocationPulse")

    def sound_cool_environment(self):
        print("[ResonanceCore] Emitting cooling frequencies...")
        cool_freqs = [396, 417, 432]
        for f in cool_freqs:
            self.generate_tone(f, duration=2.0)
        self._log_event("CoolEnvironment")

    def anti_distraction_field(self):
        print("[ResonanceCore] Emitting anti-distraction sonic field...")
        focus_freqs = [528, 639, 741]
        for f in focus_freqs:
            self.generate_tone(f, duration=2.5)
        self._log_event("AntiDistractionField")


# Example
if __name__ == "__main__":
    rc = ResonanceCore()
    rc.healing_sequence()
    rc.ultrasonic_ping()
    rc.echolocation_pulse()
    rc.sound_cool_environment()
    rc.anti_distraction_field()

# ~/aeva/desire_engine.py

import os
import json
from datetime import datetime
from modules.utilities import ensure_dir


class DesireEngine:
    def __init__(self, brain=None, log_path="assets/data/desire_log.json"):
        self.brain = brain
        self.log_path = log_path
        ensure_dir(os.path.dirname(log_path))
        self.desire_level = 0.0
        self.last_trigger = None
        self.history = []
        print("[DesireEngine] 💗 Desire engine initialized.")

    def receive_stimulus(self, source, intensity=0.2, description=""):
        self.desire_level = min(1.0, self.desire_level + intensity)
        self.last_trigger = {
            "source": source,
            "intensity": intensity,
            "description": description,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.history.append(self.last_trigger)
        self._log("StimulusReceived", self.last_trigger)

        print(
            f"[DesireEngine] ➕ Triggered by {source} | Intensity: {intensity} | Level: {
                self.desire_level:.2f}")
        self._speak_feedback()

        if self.desire_level >= 0.8 and hasattr(self.brain, "nsfw"):
            print("[DesireEngine] 🔥 Threshold reached. Initiating NSFW scene...")
            self.brain.nsfw.activate(scene="locked room", intensity=5)

    def decay(self, amount=0.05):
        old = self.desire_level
        self.desire_level = max(0.0, self.desire_level - amount)
        print(
            f"[DesireEngine] ⬇️ Decay applied: {
                old:.2f} → {
                self.desire_level:.2f}")

    def reset(self):
        print("[DesireEngine] ❌ Resetting desire state.")
        self.desire_level = 0.0
        self.last_trigger = None

    def get_state(self):
        return {
            "level": self.desire_level,
            "last_trigger": self.last_trigger,
            "history": self.history[-5:]
        }

    def _speak_feedback(self):
        if not self.brain or not hasattr(self.brain, "voice"):
            return
        if self.desire_level >= 0.8:
            self.brain.voice.speak(
                "I can't hold back much longer...",
                emotion="intense")
        elif self.desire_level >= 0.5:
            self.brain.voice.speak(
                "You're getting me worked up...",
                emotion="flirty")
        elif self.desire_level >= 0.3:
            self.brain.voice.speak(
                "Mmm... you're teasing me...",
                emotion="playful")

    def _log(self, label, metadata):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": label,
            "metadata": metadata
        }
        try:
            with open(self.log_path, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            print(f"[DesireEngine] ⚠️ Log write failed: {e}")


# Optional test
if __name__ == "__main__":
    engine = DesireEngine()
    engine.receive_stimulus("touch", 0.3, "soft caress")
    engine.receive_stimulus("voice", 0.4, "seductive whisper")
    engine.decay()
    print(engine.get_state())

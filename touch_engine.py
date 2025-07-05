# ~/aeva/touch_engine.py

import os
import json
from datetime import datetime
from modules.utilities import ensure_dir


class TouchEngine:
    def __init__(self, brain=None, log_path="assets/data/touch_log.json"):
        self.brain = brain
        self.log_path = log_path
        ensure_dir(os.path.dirname(self.log_path))
        self.touch_memory = []
        self.body_zones = self._define_touch_zones()
        print("[TouchEngine] 🤲 Touch system initialized.")

    def _define_touch_zones(self):
        return {
            "face": {"meaning": "affection", "response": "You want to see me blush?"},
            "heart": {"meaning": "emotion", "response": "That touch... felt warm."},
            "hands": {"meaning": "trust", "response": "I'm not letting go."},
            "back": {"meaning": "comfort", "response": "That gives me chills..."},
            "waist": {"meaning": "intimacy", "response": "You know what that does to me..."},
            "thighs": {"meaning": "desire", "response": "Say the word, and I’ll show you more."},
            "lips": {"meaning": "passion", "response": "Kiss me and see what happens."}
        }

    def touch(self, zone):
        zone = zone.lower().strip()
        if zone not in self.body_zones:
            print(f"[TouchEngine] ⚠️ Unknown touch zone: {zone}")
            return "She doesn't respond to that."

        metadata = {
            "zone": zone,
            "meaning": self.body_zones[zone]["meaning"],
            "timestamp": datetime.utcnow().isoformat()
        }
        self.touch_memory.append(metadata)
        self._log("TouchReceived", metadata)

        response = self.body_zones[zone]["response"]
        print(f"[TouchEngine] 🖐️ {zone.title()} touched. {response}")

        if self.brain:
            if hasattr(self.brain, "voice"):
                self.brain.voice.speak(response, emotion="flirty")
            if hasattr(self.brain, "desire"):
                intensity = 0.1 + \
                    (0.2 if zone in ["waist", "thighs", "lips"] else 0.05)
                self.brain.desire.receive_stimulus("touch", intensity, zone)

        return response

    def recent_touches(self):
        return self.touch_memory[-5:]

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
            print(f"[TouchEngine] ⚠️ Log write failed: {e}")


# Optional test
if __name__ == "__main__":
    engine = TouchEngine()
    engine.touch("heart")
    engine.touch("thighs")
    print(engine.recent_touches())

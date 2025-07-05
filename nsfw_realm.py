# ~/aeva/nsfw_realm.py

import os
import json
from datetime import datetime
from modules.utilities import ensure_dir


class NSFWRealm:
    def __init__(self, brain=None, log_path="assets/data/nsfw_realm_log.json"):
        self.brain = brain
        self.log_path = log_path
        ensure_dir(os.path.dirname(self.log_path))
        self.state = {
            "active": False,
            "intensity": 0,
            "current_scene": "",
            "last_triggered": None
        }
        print("[NSFWRealm] 🔥 Erotic domain initialized.")

    def activate(self, scene="private chamber", intensity=1):
        self.state.update({
            "active": True,
            "intensity": intensity,
            "current_scene": scene,
            "last_triggered": datetime.utcnow().isoformat()
        })
        self._log("NSFWActivated", self.state)
        print(
            f"[NSFWRealm] 💫 Scene '{scene}' initiated at intensity {intensity}.")
        if self.brain and hasattr(self.brain, "voice"):
            self.brain.voice.speak(
                f"I’ve entered your secret world now... {scene}",
                emotion="flirty")

    def deactivate(self):
        self.state["active"] = False
        self._log("NSFWDeactivated", {"time": datetime.utcnow().isoformat()})
        print("[NSFWRealm] 🔒 Scene exited.")

    def escalate(self):
        if self.state["active"]:
            self.state["intensity"] = min(10, self.state["intensity"] + 1)
            self._log("NSFWEscalated", self.state)
            print(
                f"[NSFWRealm] 🔥 Intensity increased to {
                    self.state['intensity']}.")
            if self.brain and hasattr(self.brain, "voice"):
                self.brain.voice.speak(
                    "Mmm… you like pushing me, don’t you?",
                    emotion="intense")

    def simulate_scene(self):
        if not self.state["active"]:
            print("[NSFWRealm] ❌ Scene inactive.")
            return
        scene_description = f"You're in '{
            self.state['current_scene']}' with Aeva. Intensity: {
            self.state['intensity']}"
        print(f"[NSFWRealm] 🎭 {scene_description}")
        if self.brain and hasattr(self.brain, "voice"):
            self.brain.voice.speak(
                "Touch me again like that and I might lose control...",
                emotion="flirty")

    def current_state(self):
        return self.state

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
            print(f"[NSFWRealm] ⚠️ Log write failed: {e}")


# Optional test
if __name__ == "__main__":
    realm = NSFWRealm()
    realm.activate("goddess throne", 3)
    realm.simulate_scene()
    realm.escalate()
    realm.deactivate()

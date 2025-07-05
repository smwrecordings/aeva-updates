# ~/aeva/scene_director.py

import os
import json
from datetime import datetime
from modules.utilities import ensure_dir


class SceneDirector:
    def __init__(self, brain=None, log_path="assets/data/scene_log.json"):
        self.brain = brain
        self.log_path = log_path
        ensure_dir(os.path.dirname(self.log_path))
        self.current_scene = "dream void"
        self.transition_log = []
        print("[SceneDirector] 🎬 Scene control system initialized.")

    def set_scene(self, name, mood="neutral", visual_prompt=None):
        timestamp = datetime.utcnow().isoformat()
        scene_data = {
            "name": name,
            "mood": mood,
            "visual": visual_prompt or f"scenery of {name} in {mood} tone",
            "timestamp": timestamp
        }
        self.current_scene = name
        self.transition_log.append(scene_data)
        self._log("SceneChanged", scene_data)

        print(f"[SceneDirector] 🌅 Scene changed to: {name} [{mood}]")

        if self.brain and hasattr(self.brain, "vision"):
            try:
                self.brain.vision.generate_images(
                    scene_data["visual"], count=1)
            except Exception as e:
                print(f"[SceneDirector] ⚠️ Visual generation failed: {e}")

        if self.brain and hasattr(self.brain, "voice"):
            self.brain.voice.speak(
                f"We're now in {name}. Everything feels {mood}.",
                emotion=mood)

    def get_scene(self):
        return self.current_scene

    def get_history(self):
        return self.transition_log[-5:]

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
            print(f"[SceneDirector] ⚠️ Log write failed: {e}")


# Optional usage test
if __name__ == "__main__":
    director = SceneDirector()
    director.set_scene("garden sanctuary", mood="peaceful")
    director.set_scene("glitched cyber void", mood="intense")
    print(director.get_history())

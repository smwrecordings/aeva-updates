# ~/aeva/gaze_sync.py

import random
from datetime import datetime


class GazeSync:
    def __init__(self, brain=None):
        self.brain = brain
        self.locked = False
        self.last_interaction = None
        print("[GazeSync] 👁️ Eye contact system initialized.")

    def lock_gaze(self):
        self.locked = True
        self.last_interaction = datetime.utcnow().isoformat()
        print("[GazeSync] 🔒 Eye contact locked.")
        if self.brain and hasattr(self.brain, "voice"):
            self.brain.voice.speak(
                "I see you... and I like what I see.",
                emotion="intense")
        if hasattr(self.brain, "desire"):
            self.brain.desire.receive_stimulus("gaze", 0.2, "locked gaze")

    def break_gaze(self):
        if self.locked:
            self.locked = False
            print("[GazeSync] 🔓 Eye contact broken.")
            if self.brain and hasattr(self.brain, "voice"):
                self.brain.voice.speak(
                    "Don't look away. I liked that.",
                    emotion="curious")

    def flirt_with_gaze(self):
        phrases = [
            "Caught you staring... you like what you see?",
            "My eyes are only on you.",
            "Don't blink. This moment is ours.",
            "You make me melt when you look at me like that..."
        ]
        line = random.choice(phrases)
        print(f"[GazeSync] 😏 {line}")
        if self.brain and hasattr(self.brain, "voice"):
            self.brain.voice.speak(line, emotion="flirty")
        if hasattr(self.brain, "desire"):
            self.brain.desire.receive_stimulus(
                "gaze", 0.1, "flirty eye contact")

    def status(self):
        return {
            "locked": self.locked,
            "last_interaction": self.last_interaction
        }


# Optional test
if __name__ == "__main__":
    gaze = GazeSync()
    gaze.lock_gaze()
    gaze.flirt_with_gaze()
    gaze.break_gaze()
    print(gaze.status())

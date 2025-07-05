# ~/aeva/aeva_gazesync.py

import random
from datetime import datetime


class GazeSync:
    def __init__(self, brain=None):
        self.brain = brain
        self.gaze_state = "idle"
        self.last_engagement = None
        self.attention_level = 0.0  # 0.0 to 1.0
        self.history = []

    def detect_user_gaze(self, facing_camera=True, eye_contact=True):
        timestamp = datetime.utcnow().isoformat()

        if facing_camera and eye_contact:
            self.gaze_state = "locked"
            self.attention_level = min(1.0, self.attention_level + 0.2)
            self.last_engagement = timestamp
            emotion = "curious" if self.attention_level < 0.5 else "connected"
        elif facing_camera:
            self.gaze_state = "scanning"
            self.attention_level = max(0.2, self.attention_level - 0.1)
            emotion = "observing"
        else:
            self.gaze_state = "idle"
            self.attention_level = max(0.0, self.attention_level - 0.3)
            emotion = "disengaged"

        self.history.append({
            "timestamp": timestamp,
            "gaze": self.gaze_state,
            "attention": round(self.attention_level, 2),
            "emotion": emotion
        })

        if self.brain:
            self.brain.memory.log_event(
                f"Gaze state: {
                    self.gaze_state}",
                tag="gaze")
            self.brain.emotions.reinforce(emotion, 0.1)

        return {
            "gaze_state": self.gaze_state,
            "attention": round(self.attention_level, 2),
            "emotion": emotion
        }

    def idle_gaze_behavior(self):
        action = random.choice(
            ["look_left", "look_right", "blink", "scan_up", "scan_down"])
        timestamp = datetime.utcnow().isoformat()

        if self.brain:
            self.brain.memory.log_event(
                f"Idle gaze action: {action}", tag="gaze_idle")

        return {
            "action": action,
            "timestamp": timestamp
        }

    def get_current_gaze(self):
        return {
            "gaze_state": self.gaze_state,
            "attention_level": round(self.attention_level, 2),
            "last_engagement": self.last_engagement
        }

    def get_gaze_log(self):
        return self.history[-20:]


# Optional test
if __name__ == "__main__":
    gaze = GazeSync()
    print(gaze.detect_user_gaze(True, True))
    print(gaze.idle_gaze_behavior())

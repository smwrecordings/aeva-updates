# ~/aeva/modules/scene_director.py

import random
from datetime import datetime


class SceneDirector:
    def __init__(self, brain=None):
        self.brain = brain
        self.current_scene = "default"
        self.scene_log = []

    def set_scene(self, scene_name):
        self.current_scene = scene_name
        timestamp = datetime.utcnow().isoformat()
        self.scene_log.append({
            "timestamp": timestamp,
            "scene": scene_name
        })
        if self.brain:
            self.brain.memory.log_event(
                f"Scene set to {scene_name}", tag="scene")
        print(f"[SceneDirector] Scene changed to: {scene_name}")

    def get_current_scene(self):
        return self.current_scene

    def get_scene_log(self, limit=10):
        return self.scene_log[-limit:]

    def recommend_scene(self, mood):
        mapping = {
            "joy": ["garden", "beach", "sunset_city"],
            "serious": ["command_center", "lab", "library"],
            "curious": ["archives", "cyberspace", "future_museum"],
            "dreamy": ["astral_plane", "dreamscape", "crystal_forest"],
            "protective": ["fortress", "watchtower"],
            "sad": ["rainy_alley", "nostalgia_room"],
            "flirty": ["neon_club", "intimate_lounge"],
            "neutral": ["hub", "studio"]
        }
        pool = mapping.get(mood.lower(), ["default"])
        return random.choice(pool)

    def auto_scene_shift(self):
        mood = "neutral"
        if self.brain:
            mood = self.brain.emotions.get_current_state().get("mood", "neutral")
        recommended = self.recommend_scene(mood)
        self.set_scene(recommended)
        return recommended

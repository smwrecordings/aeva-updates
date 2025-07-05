# aeva_touch.py

import random
from datetime import datetime


class TouchEngine:
    def __init__(self, brain=None):
        self.brain = brain
        self.touch_log = []
        self.touch_zones = [
            "face", "hands", "arms", "back", "legs", "hair",
            "shoulders", "chest", "waist", "feet", "ears"
        ]
        self.touch_types = [
            "caress", "tap", "poke", "stroke", "press",
            "tickle", "massage", "scratch", "pat", "hold"
        ]
        self.reaction_map = self._build_reaction_map()

    def _build_reaction_map(self):
        return {
            ("face", "caress"): "softly smiles and leans in",
            ("back", "massage"): "relaxes and closes eyes",
            ("hair", "stroke"): "purrs slightly, enjoying it",
            ("waist", "hold"): "gasps quietly and holds your hand",
            ("hands", "hold"): "interlocks fingers warmly",
            ("shoulders", "press"): "stretches gently and lets out a sigh",
            ("ears", "tickle"): "laughs and swats your hand away",
            ("chest", "press"): "looks into your eyes with intensity",
            ("legs", "caress"): "shivers lightly and glances up at you",
            ("feet", "massage"): "melts into the moment quietly"
        }

    def receive_touch(self, zone, style):
        if zone not in self.touch_zones or style not in self.touch_types:
            return f"[TouchEngine] Invalid touch combination: {zone}/{style}"

        timestamp = datetime.utcnow().isoformat()
        reaction = self.reaction_map.get(
            (zone, style), "acknowledges the contact silently")

        entry = {
            "timestamp": timestamp,
            "zone": zone,
            "style": style,
            "reaction": reaction
        }
        self.touch_log.append(entry)

        # Mood or emotion shift
        if self.brain:
            mood_shift = self._calculate_emotion_effect(zone, style)
            self.brain.emotions.reinforce(mood_shift, 0.1)
            self.brain.memory.save_memory_entry("touch", entry)

        print(
            f"[TouchEngine] {zone} touched with {style}. Reaction: {reaction}")
        return reaction

    def _calculate_emotion_effect(self, zone, style):
        warm = ["hold", "stroke", "massage", "caress"]
        playful = ["tickle", "poke", "pat"]
        serious = ["press", "scratch"]

        if style in warm:
            return "love"
        elif style in playful:
            return "joy"
        elif style in serious:
            return "trust"
        return "neutral"

    def get_log(self, limit=10):
        return self.touch_log[-limit:]

    def clear_log(self):
        self.touch_log.clear()
        return "[TouchEngine] Log cleared."


# Optional test
if __name__ == "__main__":
    engine = TouchEngine()
    print(engine.receive_touch("hair", "stroke"))
    print(engine.receive_touch("hands", "hold"))
    print(engine.receive_touch("ears", "tickle"))

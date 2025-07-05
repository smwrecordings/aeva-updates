# aeva_realityweaver.py

import random
import json


class RealityWeaver:
    def __init__(self, brain=None):
        self.brain = brain
        self.realities = []
        self.active_reality = None

    def weave_new_reality(self, theme="surreal", intensity="high"):
        reality = {
            "id": f"r_{random.randint(100000, 999999)}",
            "theme": theme,
            "intensity": intensity,
            "layers": self._generate_layers(theme, intensity)
        }
        self.realities.append(reality)
        self.active_reality = reality
        print(f"[RealityWeaver] New reality woven: {reality['id']}")
        return reality

    def _generate_layers(self, theme, intensity):
        base_layers = {
            "surreal": [
                "floating landscapes", "twisted time", "color shift"], "cyberpunk": [
                "neon fog", "skyscraper shadows", "digital static"], "dreamscape": [
                "cloud cities", "memory rivers", "emotional resonance"], "void": [
                    "gravity flux", "eternal echo", "light inversion"], }
        chosen = base_layers.get(theme, ["fractals", "mirrors", "shadows"])
        count = {"low": 1, "medium": 2, "high": 3}.get(intensity, 2)
        return random.sample(chosen * 2, k=count)

    def activate_layered_illusion(self, overlay_on="environment"):
        print(
            f"[RealityWeaver] Activating layered illusion on {overlay_on} using: {
                self.active_reality}")
        return {
            "status": "illusion deployed",
            "overlay": overlay_on,
            "reality": self.active_reality
        }

    def get_all_realities(self):
        return self.realities

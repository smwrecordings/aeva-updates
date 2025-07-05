# aeva_neuroverse.py

import json
import os
import random
from datetime import datetime
from modules.utilities import ensure_dir, get_timestamp, generate_id


class NeuroVerse:
    def __init__(self, brain=None, save_path="assets/data/neuroverse.json"):
        self.brain = brain
        self.save_path = save_path
        ensure_dir(os.path.dirname(save_path))
        self.neural_map = []
        self._load_state()

    def _load_state(self):
        if os.path.exists(self.save_path):
            try:
                with open(self.save_path, 'r') as f:
                    self.neural_map = json.load(f)
            except Exception as e:
                print(f"[NeuroVerse] Failed to load state: {e}")
                self.neural_map = []

    def _save_state(self):
        try:
            with open(self.save_path, 'w') as f:
                json.dump(self.neural_map, f, indent=2)
        except Exception as e:
            print(f"[NeuroVerse] Failed to save state: {e}")

    def encode_experience(self, topic, impact=1.0, tags=None):
        mood = self.brain.emotions.get_current_state().get(
            "mood", "neutral") if self.brain else "neutral"
        entry = {
            "id": generate_id(),
            "timestamp": get_timestamp(),
            "topic": topic,
            "mood": mood,
            "impact": impact,
            "tags": tags or [],
            "emotional_matrix": self.brain.emotions.get_current_state() if self.brain else {}
        }
        self.neural_map.append(entry)
        self._save_state()
        print(f"[NeuroVerse] Encoded experience: {topic} @ {impact}")

    def get_recent_neurons(self, limit=5):
        return self.neural_map[-limit:]

    def evolve_neural_pattern(self):
        if not self.brain:
            print("[NeuroVerse] Brain reference missing.")
            return

        curiosity = self.brain.emotions.get_current_state().get("Curiosity", 0.5)
        if curiosity > 0.7:
            self.encode_experience(
                "evolutionary_shift", impact=random.uniform(
                    0.5, 1.0), tags=[
                    "growth", "curious"])
            self.brain.memory.save_memory_entry(
                "NeuroEvolve", "Aeva's neural map evolved due to curiosity.")

    def visualize_state(self):
        print("\n[NeuroVerse] Neural State Snapshot:")
        for node in self.neural_map[-3:]:
            print(
                f"- {
                    node['timestamp']} :: {
                    node['topic']} [{
                    node['mood']}] impact {
                    node['impact']}")


# Optional demo
if __name__ == "__main__":
    from types import SimpleNamespace
    dummy_brain = SimpleNamespace(
        emotions=SimpleNamespace(
            get_current_state=lambda: {
                "mood": "curious",
                "Curiosity": 0.8,
                "Love": 0.5}),
        memory=SimpleNamespace(
            save_memory_entry=lambda label,
            msg: print(
                f"[Memory] {label}: {msg}")))
    nv = NeuroVerse(dummy_brain)
    nv.encode_experience("test_thought", impact=0.75)
    nv.evolve_neural_pattern()
    nv.visualize_state()

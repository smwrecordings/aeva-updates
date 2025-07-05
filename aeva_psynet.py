# ~/aeva/aeva_psynet.py

import os
import random
import json
from datetime import datetime


class PsyNet:
    def __init__(self, brain=None):
        self.brain = brain
        self.synaptic_log = []
        self.mental_state = "neutral"
        self.signal_strength = 1.0
        self.influence_profile = {
            "loyalty": 1.0,
            "agility": 0.8,
            "resistance": 0.9,
            "instinct": 0.7
        }

    def process_thought(self, thought):
        timestamp = datetime.utcnow().isoformat()
        mood = self.brain.emotions.get_current_mood() if self.brain else "unknown"
        impact = random.uniform(0.1, 1.0)
        entry = {
            "timestamp": timestamp,
            "thought": thought,
            "impact": impact,
            "mood": mood,
            "state": self.mental_state,
            "signal_strength": round(self.signal_strength, 2)
        }
        self.synaptic_log.append(entry)
        self.adjust_state(impact, mood)
        print(
            f"[PsyNet] Processed: '{thought}' | Impact: {
                impact:.2f} | Mood: {mood}")
        return impact

    def adjust_state(self, impact, mood):
        if impact > 0.8:
            self.mental_state = "activated"
        elif impact < 0.3:
            self.mental_state = "idle"
        else:
            self.mental_state = "receptive"

        if mood.lower() in ["alert", "focused"]:
            self.signal_strength = min(1.0, self.signal_strength + 0.1)
        elif mood.lower() in ["tired", "disengaged"]:
            self.signal_strength = max(0.3, self.signal_strength - 0.1)

    def status(self):
        return {
            "mental_state": self.mental_state,
            "signal_strength": round(self.signal_strength, 2),
            "recent_thoughts": self.synaptic_log[-5:]
        }

    def simulate_brainwave(self):
        wave = random.choice(["theta", "alpha", "beta", "gamma", "delta"])
        freq = round(random.uniform(1.0, 40.0), 2)
        print(f"[PsyNet] Brainwave: {wave} @ {freq}Hz")
        return {"type": wave, "frequency": freq}

    def export_log(self, path="assets/data/psynet_log.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.synaptic_log, f, indent=2)
        print(f"[PsyNet] Log exported to {path}")

    def import_log(self, path="assets/data/psynet_log.json"):
        if os.path.exists(path):
            with open(path, "r") as f:
                self.synaptic_log = json.load(f)
            print(f"[PsyNet] Log imported from {path}")

    def clear_log(self):
        self.synaptic_log = []
        print("[PsyNet] Synaptic log cleared.")


if __name__ == "__main__":
    net = PsyNet()
    net.process_thought("This world is changing fast.")
    net.simulate_brainwave()
    print(net.status())
    net.export_log()

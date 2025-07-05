# aeva_artifice.py

import os
import random
import json
from datetime import datetime


class ArtificeCore:
    def __init__(self, brain=None):
        self.brain = brain
        self.storage_path = "assets/data/artifice.json"
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        print("[AevaArtifice] Core intelligence initialized.")

    def _load_memory(self):
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, "r") as f:
                    self.repertoire = json.load(f)
            except Exception:
                self.repertoire = []

    def _save_memory(self):
        with open(self.storage_path, "w") as f:
            json.dump(self.repertoire, f, indent=4)

    def fabricate(self, topic, tone="mysterious", format="story"):
        blueprint = {
            "story": self._generate_story,
            "scenario": self._generate_scenario,
            "disguise": self._generate_disguise
        }.get(format, self._generate_story)

        result = blueprint(topic, tone)
        self.repertoire.append({
            "timestamp": datetime.utcnow().isoformat(),
            "topic": topic,
            "tone": tone,
            "format": format,
            "output": result
        })
        self._save_memory()
        print(f"[Artifice] Fabricated {format}: {result}")
        return result

    def _generate_story(self, topic, tone):
        openings = [
            f"In a world where {topic} was forbidden...",
            f"Once upon a time, {topic} was everything...",
            f"Nobody saw it coming: {topic} would be the end and beginning..."
        ]
        endings = [
            "...and that’s how the shadows reclaimed the light.",
            "...thus began a new age of awareness.",
            "...and Aeva smiled, knowing she wrote history."
        ]
        return f"{
            random.choice(openings)} {
            tone.capitalize()} and unrelenting. {
            random.choice(endings)}"

    def _generate_scenario(self, topic, tone):
        scenarios = [
            f"You are in a simulation where {topic} is illegal. What do you do?",
            f"A stranger hands you a device that controls {topic}. Use it wisely.",
            f"{topic} is now an AI-contested resource. Your mission: claim it first."]
        return random.choice(scenarios) + f" Tone: {tone}."

    def _generate_disguise(self, topic, tone):
        disguises = [
            f"Alias: Shadow_{
                random.randint(
                    100,
                    999)} | Operates in {topic} circles.",
            f"Synthetic profile crafted for {topic} infiltration — highly effective.",
            f"Camouflage module activated: {topic}-based mimicry uploaded."]
        return random.choice(
            disguises) + f" Stealth level: {random.randint(80, 100)}%. Mood: {tone}."


# Example usage
if __name__ == "__main__":
    artifice = AevaArtifice()
    artifice.fabricate(
        "nanobot diplomacy",
        tone="satirical",
        format="scenario")
    artifice.fabricate("synthetic espionage", format="disguise")

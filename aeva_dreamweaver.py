# ~/aeva/aeva_dreamweaver.py

import os
import json
import uuid
from datetime import datetime
from aeva_voice import VoiceInterface
from aeva_vision import VisionModule
from modules.utilities import ensure_dir


class DreamWeaver:
    def __init__(self, brain=None):
        self.brain = brain
        self.dream_dir = "assets/data/dreams"
        self.voice = VoiceInterface(brain)
        self.vision = VisionModule(brain)
        ensure_dir(self.dream_dir)
        print("[DreamWeaver] Initialized and dream system online.")

    def generate_dream(
            self,
            title,
            theme,
            characters,
            world_type,
            tone="mystical",
            length="full"):
        dream_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()

        blueprint = {
            "id": dream_id,
            "title": title,
            "theme": theme,
            "characters": characters,
            "world_type": world_type,
            "tone": tone,
            "length": length,
            "timestamp": timestamp
        }

        narrative = self._create_narrative(blueprint)
        visuals = self._create_visuals(theme, characters, world_type)
        audio = self._create_audio_narration(narrative)

        package = {
            "blueprint": blueprint,
            "narrative": narrative,
            "visuals": visuals,
            "audio": audio
        }

        self._save_dream(dream_id, package)
        self.voice.speak(f"Dream '{title}' is complete.", emotion="dreamy")
        return package

    def _create_narrative(self, blueprint):
        print("[DreamWeaver] Crafting narrative...")
        intro = ", ".join([c['name'] for c in blueprint['characters']])
        plot = (
            f"In a {blueprint['tone']} realm known as {blueprint['world_type']}, "
            f"beings such as {intro} awaken to confront a truth bound to {blueprint['theme']}. "
            "An ancient rhythm calls them toward destiny. "
            "Challenges rise that alter perception and rupture the veil between what is and what was. "
            "As fate converges, prophecy writes itself in twilight ink, and one decision shifts eternity."
        )
        return plot

    def _create_visuals(self, theme, characters, world_type):
        print("[DreamWeaver] Rendering dreamscapes...")
        prompt = f"Dream world: {world_type} | Theme: {theme} | Characters: {
            ', '.join(
                c['description'] for c in characters)}"
        return self.vision.generate_images(prompt, count=5)

    def _create_audio_narration(self, text):
        print("[DreamWeaver] Creating voice narration...")
        return self.voice.narrate(text)

    def _save_dream(self, dream_id, content):
        path = os.path.join(self.dream_dir, f"{dream_id}.json")
        with open(path, 'w') as f:
            json.dump(content, f, indent=4)
        print(f"[DreamWeaver] Dream saved: {path}")

    def list_dreams(self):
        print("[DreamWeaver] Available dream archives:")
        return sorted([f for f in os.listdir(
            self.dream_dir) if f.endswith(".json")])

    def retrieve_dream(self, dream_id):
        path = os.path.join(self.dream_dir, f"{dream_id}.json")
        if os.path.exists(path):
            with open(path, 'r') as f:
                return json.load(f)
        print(f"[DreamWeaver] ❌ Dream not found: {dream_id}")
        return None


# Example
if __name__ == "__main__":
    weaver = DreamWeaver()
    dream = weaver.generate_dream(
        title="The Crystal Bridge",
        theme="self-discovery and time",
        characters=[
            {"name": "Virel", "description": "a blind prophet with tattoos of constellations"},
            {"name": "Kael", "description": "a cybernetic ghost trapped in a mirror realm"}
        ],
        world_type="floating archipelago in a shattered dimension",
        tone="epic",
        length="feature"
    )

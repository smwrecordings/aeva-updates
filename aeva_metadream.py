# aeva_metadream.py

import os
import random
import json
from datetime import datetime


class MetaDream:
    def __init__(self, dream_path="assets/data/metadream_log.json"):
        self.dream_path = dream_path
        os.makedirs(os.path.dirname(dream_path), exist_ok=True)

    def generate_dream(self):
        prompts = [
            "The desert hums with quantum echoes.",
            "I am the architect of forgotten skies.",
            "Cities bloom from the bones of giants.",
            "Light bends where thought whispers."
        ]
        dream = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": "LucidSequence",
            "sequence": random.choice(prompts)
        }
        print(f"[MetaDream] Dream: {dream['sequence']}")
        self._save_dream(dream)

    def _save_dream(self, dream):
        with open(self.dream_path, "a") as f:
            f.write(json.dumps(dream) + "\n")

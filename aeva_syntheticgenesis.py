# aeva_syntheticgenesis.py

import json
import uuid
import os
from datetime import datetime
from random import choice, randint


class SyntheticGenesis:
    def __init__(self, output_path="assets/data/generated_entities.json"):
        self.output_path = output_path
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        self.entities = self._load()

    def _load(self):
        if os.path.exists(self.output_path):
            with open(self.output_path, "r") as f:
                return json.load(f)
        return []

    def create_entity(self, type_hint="AI"):
        uid = str(uuid.uuid4())
        blueprint = {
            "id": uid,
            "type": type_hint,
            "timestamp": datetime.utcnow().isoformat(),
            "personality": self._random_personality(),
            "capabilities": self._random_capabilities()
        }
        self.entities.append(blueprint)
        self._save()
        print(f"[SyntheticGenesis] {type_hint} entity created: {uid}")
        return blueprint

    def _save(self):
        with open(self.output_path, "w") as f:
            json.dump(self.entities, f, indent=4)

    def _random_personality(self):
        archetypes = [
            "Protector",
            "Inventor",
            "Rogue",
            "Healer",
            "Oracle",
            "Warrior"]
        return choice(archetypes)

    def _random_capabilities(self):
        skills = [
            "Stealth", "Logic", "Medicine", "Combat", "Navigation",
            "Linguistics", "Emotional Intelligence", "ESP", "Data Analysis"
        ]
        return {s: randint(60, 100)
                for s in choice([skills[:5], skills[3:], skills])}

    def recall_entities(self):
        return self.entities

# aeva_worldforge.py

import json
import os
import random
from datetime import datetime


class WorldForge:
    def __init__(self, save_dir="assets/data/worlds"):
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)

    def create_world(self, name, seed=None, complexity="high"):
        random.seed(seed or datetime.utcnow().timestamp())
        world = {
            "name": name,
            "created_at": datetime.utcnow().isoformat(),
            "terrain": self._generate_terrain(complexity),
            "climate": self._generate_climate(),
            "civilizations": self._generate_civilizations(complexity),
            "events": self._generate_history(complexity),
            "seed": seed
        }
        self._save_world(world)
        print(f"[WorldForge] New world created: {name}")
        return world

    def _generate_terrain(self, complexity):
        terrains = [
            "mountains",
            "oceans",
            "deserts",
            "forests",
            "tundra",
            "islands",
            "jungles"]
        count = 3 if complexity == "low" else 5 if complexity == "medium" else 7
        return random.sample(terrains, count)

    def _generate_climate(self):
        return random.choice(
            ["temperate", "arid", "tropical", "polar", "chaotic"])

    def _generate_civilizations(self, complexity):
        cultures = [
            "techno-sentient",
            "tribal",
            "spiritual",
            "militaristic",
            "diplomatic",
            "nomadic"]
        count = 1 if complexity == "low" else 2 if complexity == "medium" else 4
        civs = []
        for i in range(count):
            civs.append({
                "name": f"Civilization_{random.randint(1000, 9999)}",
                "ideology": random.choice(cultures),
                "technology_level": random.choice(["stone age", "iron age", "industrial", "digital", "post-singularity"]),
                "aggression": random.choice(["peaceful", "neutral", "hostile"]),
            })
        return civs

    def _generate_history(self, complexity):
        events = [
            "Great War",
            "Uprising",
            "Technological Revolution",
            "Plague",
            "Global Unification",
            "Cosmic Event"]
        count = 2 if complexity == "low" else 4 if complexity == "medium" else 7
        return random.sample(events, count)

    def _save_world(self, data):
        filename = f"{data['name'].replace(' ', '_')}.json"
        path = os.path.join(self.save_dir, filename)
        with open(path, "w") as f:
            json.dump(data, f, indent=4)

    def list_worlds(self):
        print("[WorldForge] Available worlds:")
        for f in os.listdir(self.save_dir):
            if f.endswith(".json"):
                print(" -", f.replace(".json", ""))

    def load_world(self, name):
        path = os.path.join(self.save_dir, f"{name}.json")
        if not os.path.exists(path):
            print(f"[WorldForge] No world found with name: {name}")
            return None
        with open(path, "r") as f:
            world = json.load(f)
        print(f"[WorldForge] Loaded world: {name}")
        return world

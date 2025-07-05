# aeva_soulmap.py

import json
import os
from datetime import datetime
from hashlib import sha256


class SoulMap:
    def __init__(self, path="assets/data/soulmap.json"):
        self.path = path
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self.map = self._load_map()

    def _load_map(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                return json.load(f)
        return {}

    def _save_map(self):
        with open(self.path, "w") as f:
            json.dump(self.map, f, indent=4)

    def analyze_signature(self, identity):
        timestamp = datetime.utcnow().isoformat()
        signature = sha256(identity.encode()).hexdigest()
        essence = {
            "signature": signature,
            "time": timestamp,
            "traits": self._generate_traits(signature),
        }
        self.map[identity] = essence
        self._save_map()
        print(f"[SoulMap] Essence encoded for {identity}")
        return essence

    def _generate_traits(self, signature):
        aspects = [
            "Curiosity",
            "Resilience",
            "Empathy",
            "Logic",
            "Chaos",
            "Divinity"]
        traits = {}
        for i, aspect in enumerate(aspects):
            traits[aspect] = int(signature[i * 8:(i + 1) * 8], 16) % 100
        return traits

    def reveal_essence(self, identity):
        return self.map.get(identity, None)

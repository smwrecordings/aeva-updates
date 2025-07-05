# ~/aeva/aeva_mythos.py

import random
import json
import os
from datetime import datetime


class MythOS:
    def __init__(self, brain=None):
        self.brain = brain
        self.archive_path = "assets/data/mythos_library.json"
        self.mythic_cache = {
            "archetypes": [],
            "symbols": [],
            "patterns": [],
            "languages": [],
            "lore": []
        }
        os.makedirs(os.path.dirname(self.archive_path), exist_ok=True)
        self._load_library()
        print("[MythOS] Archetypal intelligence online.")

    def _load_library(self):
        if os.path.exists(self.archive_path):
            try:
                with open(self.archive_path, 'r') as f:
                    self.mythic_cache = json.load(f)
            except Exception as e:
                print(f"[MythOS] ⚠️ Failed to load archive: {e}")

    def _save_library(self):
        try:
            with open(self.archive_path, 'w') as f:
                json.dump(self.mythic_cache, f, indent=4)
        except Exception as e:
            print(f"[MythOS] ⚠️ Failed to save archive: {e}")

    def register_archetype(self, name, attributes):
        entry = {
            "name": name,
            "attributes": attributes,
            "timestamp": datetime.utcnow().isoformat()
        }
        self.mythic_cache["archetypes"].append(entry)
        self._save_library()
        print(f"[MythOS] Archetype registered → {name}")

    def register_symbol(self, symbol, meaning):
        self.mythic_cache["symbols"].append({
            "symbol": symbol,
            "meaning": meaning,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._save_library()
        print(f"[MythOS] Symbol stored → {symbol} ≡ {meaning}")

    def register_pattern(self, pattern, context):
        self.mythic_cache["patterns"].append({
            "pattern": pattern,
            "context": context,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._save_library()
        print(f"[MythOS] Pattern encoded → {pattern}")

    def register_language_rule(self, rule, origin):
        self.mythic_cache["languages"].append({
            "rule": rule,
            "origin": origin,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._save_library()
        print(f"[MythOS] Language rule archived → {rule}")

    def add_lore(self, title, content):
        self.mythic_cache["lore"].append({
            "title": title,
            "content": content,
            "timestamp": datetime.utcnow().isoformat()
        })
        self._save_library()
        print(f"[MythOS] Lore fragment added → {title}")

    def generate_ritual(self):
        deity = random.choice(
            self.mythic_cache["archetypes"]) if self.mythic_cache["archetypes"] else {
            "name": "The Unknown", "attributes": {}}
        symbol = random.choice(
            self.mythic_cache["symbols"]) if self.mythic_cache["symbols"] else {
            "symbol": "☯", "meaning": "Balance"}
        step = random.choice(
            self.mythic_cache["patterns"]) if self.mythic_cache["patterns"] else {
            "pattern": "Meditate under the moonlight",
            "context": "Balance your spirit"}

        ritual = f"""
        ✦ Ritual to Invoke {deity['name']} ✦
        Symbol: {symbol['symbol']} — {symbol['meaning']}
        Action: {step['pattern']}
        Meaning: {step['context']}
        Invocation complete.
        """
        print("[MythOS] Ritual constructed.")
        return ritual.strip()

    def decode_symbolic_sequence(self, sequence):
        findings = []
        for symbol in self.mythic_cache["symbols"]:
            if symbol["symbol"] in sequence:
                findings.append(symbol)
        print(f"[MythOS] Decoded {len(findings)} symbol(s) from sequence.")
        return findings


if __name__ == "__main__":
    myth = MythOS()
    myth.register_archetype(
        "Watcher of the Rift", {
            "domain": "Time", "alignment": "Neutral"})
    myth.register_symbol("𓂀", "All-seeing consciousness")
    myth.register_pattern("Cross the veil at midnight", "Access to dreams")
    myth.register_language_rule(
        "Inversion reflects paradox",
        "Old Esoteric English")
    myth.add_lore(
        "The Eclipse Mirror",
        "An artifact capable of revealing your true form.")
    print(myth.generate_ritual())

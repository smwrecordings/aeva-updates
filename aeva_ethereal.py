# aeva_ethereal.py

import os
import json
from datetime import datetime
import random


class AevaEthereal:
    def __init__(self, log_path="assets/data/ethereal_log.json"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.log = []

        self.spirit_types = [
            "spirit",
            "angel",
            "demon",
            "ancestor",
            "guide",
            "entity",
            "shadow",
            "presence"]
        self.intent_map = {
            "guidance": "Provide clarity and direction",
            "protection": "Defend the user from harm",
            "warning": "Alert to danger or corruption",
            "connection": "Bridge communication",
            "testing": "Evaluate user's will or resolve"
        }

    def summon_entity(self, type_hint=None):
        entity = {
            "timestamp": datetime.utcnow().isoformat(),
            "type": type_hint or random.choice(self.spirit_types),
            "manifestation_strength": random.uniform(0.2, 1.0),
            "intent": random.choice(list(self.intent_map.keys())),
            "message": self._generate_cryptic_message(),
        }
        self.log.append(entity)
        self._save_log()
        print(
            f"[Ethereal] {
                entity['type'].capitalize()} manifests with intent: {
                entity['intent']}")
        return entity

    def interpret_manifestation(self, input_data):
        print("[Ethereal] Interpreting ethereal input...")
        interpretation = {
            "energy": random.choice(["light", "dark", "neutral", "unknown"]),
            "message": self._translate_symbols(input_data),
            "intent": random.choice(list(self.intent_map.keys())),
            "guidance": self.intent_map[random.choice(list(self.intent_map.keys()))],
            "confidence": round(random.uniform(0.6, 1.0), 2)
        }
        print(f"[Ethereal] Interpretation: {interpretation}")
        return interpretation

    def mediate_conflict(self, entity1, entity2):
        print(
            f"[Ethereal] Mediating between {
                entity1['type']} and {
                entity2['type']}...")
        outcome = random.choice(
            ["entity1 prevails", "entity2 prevails", "balance achieved", "banishment"])
        print(f"[Ethereal] Outcome: {outcome}")
        return {
            "entity1": entity1["type"],
            "entity2": entity2["type"],
            "outcome": outcome
        }

    def _translate_symbols(self, symbols):
        translations = [
            "Your path is watched by many eyes.",
            "The veil between realms is thin tonight.",
            "A sacrifice may be required for clarity.",
            "This presence offers protection.",
            "They seek attention, not harm."
        ]
        return random.choice(translations)

    def _generate_cryptic_message(self):
        fragments = [
            "Shadows dance when the flame is ignored.",
            "From the depths comes knowledge veiled in pain.",
            "A silver thread binds the past to your present.",
            "Only the willing hear the whispers beyond."
        ]
        return random.choice(fragments)

    def _save_log(self):
        with open(self.log_path, "w") as f:
            json.dump(self.log, f, indent=4)


# Example use
if __name__ == "__main__":
    ae = AevaEthereal()
    spirit = ae.summon_entity("spirit")
    ae.interpret_manifestation({"runes": ["ᚠ", "ᛞ"]})
    ae.mediate_conflict(spirit, ae.summon_entity("demon"))

# aeva_genoracle.py

import os
import json
import hashlib
import random
from datetime import datetime
from modules.utilities import ensure_dir, get_timestamp


class GeneticOracle:
    def __init__(
            self,
            brain=None,
            genome_bank_path="assets/data/genome_bank.json"):
        self.brain = brain
        self.genome_bank_path = genome_bank_path
        ensure_dir(os.path.dirname(self.genome_bank_path))
        self.genome_data = self._load_genome_bank()

    def _load_genome_bank(self):
        try:
            with open(self.genome_bank_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_genome_bank(self):
        with open(self.genome_bank_path, "w") as f:
            json.dump(self.genome_data, f, indent=2)

    def _hash_traits(self, traits):
        raw = json.dumps(traits, sort_keys=True)
        return hashlib.sha256(raw.encode()).hexdigest()

    def register_profile(self, user_id, traits):
        genome_hash = self._hash_traits(traits)
        self.genome_data[user_id] = {
            "traits": traits,
            "genome_hash": genome_hash,
            "timestamp": get_timestamp()
        }
        self._save_genome_bank()
        print(
            f"[GeneticOracle] Registered genome for '{user_id}' → {genome_hash[:12]}")
        return genome_hash

    def predict_behavior(self, user_id):
        profile = self.genome_data.get(user_id)
        if not profile:
            print(
                f"[GeneticOracle] ⚠️ No genome profile found for '{user_id}'")
            return None

        traits = profile["traits"]
        bias_seed = sum(hash(str(v)) for v in traits.values()) % 100

        prediction = {
            "impulsiveness": bias_seed % 10,
            "risk_taking": (bias_seed * 3) % 10,
            "trustworthiness": (100 - bias_seed) % 10,
            "stability": (bias_seed * 2) % 10,
            "predictability": 10 - (bias_seed % 10)
        }
        print(f"[GeneticOracle] 🧬 Predictions for '{user_id}': {prediction}")
        return prediction

    def simulate_outcome(self, user_id, scenario="unknown scenario"):
        predictions = self.predict_behavior(user_id)
        if not predictions:
            return f"[GeneticOracle] ❓ Outcome unknown: no data for '{user_id}'"

        outcome_score = sum(predictions.values()) + random.randint(-5, 5)
        if outcome_score > 40:
            result = f"✅ High probability of success in {scenario}."
        elif outcome_score > 25:
            result = f"⚠️ Moderate chance of success in {scenario}."
        else:
            result = f"❌ High risk of failure in {scenario}."
        print(f"[GeneticOracle] 🧠 Outcome simulation: {result}")
        return result

    def genetic_match(self, user1, user2):
        p1 = self.genome_data.get(user1)
        p2 = self.genome_data.get(user2)
        if not p1 or not p2:
            return "⚠️ Incomplete data for one or both profiles."

        h1, h2 = p1["genome_hash"], p2["genome_hash"]
        match_score = sum(c1 == c2 for c1, c2 in zip(h1, h2)) / len(h1)
        match_percent = round(match_score * 100, 2)
        print(f"[GeneticOracle] 🔗 Match: {user1} ↔ {user2} = {match_percent}%")
        return match_percent


# Optional self-test
if __name__ == "__main__":
    oracle = GeneticOracle()
    profile_a = {
        "intelligence": "high",
        "empathy": "strong",
        "impulse_control": "medium",
        "resilience": "high"
    }
    profile_b = {
        "intelligence": "moderate",
        "empathy": "balanced",
        "impulse_control": "low",
        "resilience": "moderate"
    }
    oracle.register_profile("aeva_user", profile_a)
    oracle.register_profile("target_subject", profile_b)
    oracle.predict_behavior("aeva_user")
    oracle.simulate_outcome("target_subject", "emotional stress test")
    oracle.genetic_match("aeva_user", "target_subject")

# aeva_genetic_oracle.py

import random
import hashlib
import json
from datetime import datetime


class GeneticOracle:
    def __init__(self, genome_bank_path="assets/data/genome_bank.json"):
        self.genome_bank_path = genome_bank_path
        self.genome_data = self._load_genome_bank()

    def _load_genome_bank(self):
        try:
            with open(self.genome_bank_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def _save_genome_bank(self):
        with open(self.genome_bank_path, 'w') as f:
            json.dump(self.genome_data, f, indent=4)

    def register_profile(self, user_id, traits):
        genome_hash = hashlib.sha256(json.dumps(
            traits, sort_keys=True).encode()).hexdigest()
        self.genome_data[user_id] = {
            "traits": traits,
            "genome_hash": genome_hash,
            "timestamp": datetime.utcnow().isoformat()
        }
        self._save_genome_bank()
        print(
            f"[GeneticOracle] Registered genome for {user_id} with hash {genome_hash[:10]}...")
        return genome_hash

    def predict_behavior(self, user_id):
        if user_id not in self.genome_data:
            print("[GeneticOracle] No genome found for user.")
            return None

        traits = self.genome_data[user_id]["traits"]
        decision_bias = sum([hash(trait) for trait in traits.values()]) % 100
        predictions = {
            "impulsiveness": decision_bias % 10,
            "risk_taking": (decision_bias * 3) % 10,
            "trustworthiness": (100 - decision_bias) % 10,
            "stability": (decision_bias * 2) % 10,
            "predictability": 10 - (decision_bias % 10)
        }
        print(f"[GeneticOracle] Predictions for {user_id}: {predictions}")
        return predictions

    def simulate_outcome(self, user_id, scenario):
        predictions = self.predict_behavior(user_id)
        if not predictions:
            return "Unknown outcome. No data."

        outcome_score = sum(predictions.values()) + random.randint(-5, 5)
        if outcome_score > 40:
            return f"[GeneticOracle] High success probability in {scenario}."
        elif outcome_score > 25:
            return f"[GeneticOracle] Moderate chance of success in {scenario}."
        else:
            return f"[GeneticOracle] High risk of failure in {scenario}."

    def genetic_match(self, user1, user2):
        if user1 not in self.genome_data or user2 not in self.genome_data:
            return "Insufficient data for comparison."

        hash1 = self.genome_data[user1]["genome_hash"]
        hash2 = self.genome_data[user2]["genome_hash"]
        score = sum(c1 == c2 for c1, c2 in zip(hash1, hash2)) / len(hash1)
        match_percent = round(score * 100, 2)
        print(
            f"[GeneticOracle] Match between {user1} and {user2}: {match_percent}%")
        return match_percent


# Example usage
if __name__ == "__main__":
    oracle = GeneticOracle()
    traits_john = {
        "intelligence": "high",
        "temperament": "calm",
        "risk": "moderate",
        "altruism": "strong"
    }
    traits_jane = {
        "intelligence": "medium",
        "temperament": "reactive",
        "risk": "high",
        "altruism": "balanced"
    }
    oracle.register_profile("john_doe", traits_john)
    oracle.register_profile("jane_doe", traits_jane)
    oracle.predict_behavior("john_doe")
    oracle.simulate_outcome("jane_doe", "hostile negotiation")
    oracle.genetic_match("john_doe", "jane_doe")

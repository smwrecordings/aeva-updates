# aeva_survivor.py

import json
from datetime import datetime


class SurvivalExpert:
    def __init__(self):
        self.skills = self.load_knowledge()

    def load_knowledge(self):
        return {
            "edible_plants": [
                "dandelion",
                "clover",
                "cattail",
                "plantain",
                "wild garlic"],
            "poisonous_plants": [
                "hemlock",
                "deadly nightshade",
                "oleander",
                "white baneberry"],
            "shelter_methods": [
                "lean-to",
                "debris hut",
                "snow cave",
                "rock overhang",
                "tarp tent"],
            "fire_starting": [
                "flint and steel",
                "bow drill",
                "magnesium block",
                "lens ignition"],
            "water_purification": [
                "boiling",
                "charcoal/sand filter",
                "solar still",
                "iodine drops"],
            "first_aid": [
                "tourniquets",
                "splints",
                "CPR",
                "wound dressing",
                "herbal antiseptics"]}

    def get_edible_plants(self):
        return self.skills["edible_plants"]

    def get_poisonous_plants(self):
        return self.skills["poisonous_plants"]

    def suggest_shelter(self, environment):
        print(f"[Survivor] Evaluating shelter for environment: {environment}")
        return self.skills["shelter_methods"]

    def emergency_protocol(self):
        print("[Survivor] Emergency survival mode activated.")
        return {
            "fire": self.skills["fire_starting"],
            "shelter": self.skills["shelter_methods"],
            "first_aid": self.skills["first_aid"]
        }

    def plant_check(self, name):
        name = name.lower()
        if name in [p.lower() for p in self.skills["edible_plants"]]:
            return f"{name.title()} is safe to eat."
        elif name in [p.lower() for p in self.skills["poisonous_plants"]]:
            return f"{name.title()} is POISONOUS."
        else:
            return f"Unknown plant: {name.title()}. Exercise caution."


# Example usage
if __name__ == "__main__":
    s = SurvivalExpert()
    print(s.get_edible_plants())
    print(s.suggest_shelter("cold forest"))
    print(s.plant_check("cattail"))
    print(s.plant_check("oleander"))
    print(s.emergency_protocol())

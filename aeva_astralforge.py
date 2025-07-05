# aeva_astralforge.py

import os
import json
from datetime import datetime
from random import choice, randint


class AstralForge:
    def __init__(self, output_dir="assets/data/astral_realms"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        self.templates = self._load_templates()

    def _load_templates(self):
        return {
            "sanctuary": {
                "description": "A glowing sanctuary of floating islands surrounded by stardust and silence.",
                "elements": [
                    "crystal towers",
                    "whispering trees",
                    "gravity wells",
                    "luminous fauna"]},
            "abyss": {
                "description": "A shadow world layered in echoes and pulsating alien energies.",
                "elements": [
                    "black sun",
                    "thought-consuming fog",
                    "shifting labyrinths",
                    "static stars"]},
            "dream_city": {
                "description": "A neo-ancient city with fractal spires and melodic lights.",
                "elements": [
                    "liquid glass roads",
                    "sentient statues",
                    "floating trams",
                    "sky whales"]}}

    def generate_realm(self, name=None):
        template = self.templates.get(name) if name else choice(
            list(self.templates.values()))
        if not template:
            raise ValueError("No valid astral realm template found.")

        realm = {
            "name": name or "unnamed_realm",
            "description": template["description"],
            "elements": [
                choice(
                    template["elements"]) for _ in range(
                    randint(
                        3,
                        6))],
            "timestamp": datetime.utcnow().isoformat()}
        self._save_realm(realm)
        print(f"[AstralForge] Realm '{realm['name']}' created.")
        return realm

    def _save_realm(self, realm):
        filename = f"{
            realm['name']}_{
            datetime.utcnow().strftime('%Y%m%d%H%M%S')}.json"
        path = os.path.join(self.output_dir, filename)
        with open(path, "w") as f:
            json.dump(realm, f, indent=4)

    def list_templates(self):
        return list(self.templates.keys())


# Example usage
if __name__ == "__main__":
    af = AstralForge()
    print("Templates:", af.list_templates())
    realm = af.generate_realm("sanctuary")
    print(json.dumps(realm, indent=2))

# aeva_starforge.py

import random
import json
import os


class Starforge:
    def __init__(self, universe_dir="assets/data/starforge_universes"):
        self.universe_dir = universe_dir
        os.makedirs(self.universe_dir, exist_ok=True)

    def forge_universe(
            self,
            name="Unnamed",
            style="sci-fi",
            complexity="high",
            seed=None):
        seed = seed or random.randint(100000, 999999)
        universe = {
            "name": name,
            "style": style,
            "complexity": complexity,
            "seed": seed,
            "star_systems": self._generate_star_systems(seed, complexity),
            "civilizations": self._generate_civilizations(style, complexity),
            "mysteries": self._generate_mysteries(style),
            "lore": self._generate_lore(name)
        }
        self._save_universe(universe)
        print(f"[Starforge] Universe '{name}' forged with seed {seed}")
        return universe

    def _generate_star_systems(self, seed, complexity):
        random.seed(seed)
        count = {"low": 5, "medium": 15, "high": 30}.get(complexity, 15)
        return [
            f"System-{i}-{random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZ')}" for i in range(1, count + 1)]

    def _generate_civilizations(self, style, complexity):
        civ_styles = {
            "sci-fi": ["Xenon Dominion", "Nova Federation", "Omega Syndicate"],
            "fantasy": ["Emerald Kingdom", "Ashen Order", "Luminari"],
            "dark": ["The Eclipsed", "Voidborn", "Flesh Architects"]
        }
        base = civ_styles.get(style, ["Nomads", "Warborn", "Seekers"])
        count = {"low": 1, "medium": 3, "high": 5}.get(complexity, 3)
        return random.sample(base * 2, count)

    def _generate_mysteries(self, style):
        mysteries = {
            "sci-fi": ["Time-fold Rift", "Living Black Hole", "Lost Planet of AI Gods"],
            "fantasy": ["Well of Eternity", "Godspeakers' Tomb", "The Cursed Comet"],
            "dark": ["The Unknowing Spiral", "The Whispering Dark", "Starless Realm"]
        }
        return random.sample(mysteries.get(style, []), k=2)

    def _generate_lore(self, name):
        return f"The tale of '{name}' began in the shattered age after the Celestial Collapse. Born from chaos, it now spirals toward unknown futures..."

    def _save_universe(self, universe):
        path = os.path.join(
            self.universe_dir, f"{
                universe['name'].replace(
                    ' ', '_')}.json")
        with open(path, 'w') as f:
            json.dump(universe, f, indent=4)

    def list_universes(self):
        return [
            f for f in os.listdir(
                self.universe_dir) if f.endswith(".json")]

    def load_universe(self, name):
        filepath = os.path.join(self.universe_dir, f"{name}.json")
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                universe = json.load(f)
            print(f"[Starforge] Universe '{name}' loaded.")
            return universe
        else:
            print(f"[Starforge] Universe '{name}' not found.")
            return None


# Example use
if __name__ == "__main__":
    forge = Starforge()
    forge.forge_universe(name="Elysium Drift", style="dark", complexity="high")
    print(forge.list_universes())

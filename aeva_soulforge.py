# aeva_soulforge.py

class SoulForge:
    def __init__(self):
        self.inner_fires = {}

    def ignite_trait(self, trait, intensity=10):
        self.inner_fires[trait] = intensity
        print(f"[SoulForge] Trait '{trait}' ignited at intensity {intensity}.")
        return self.inner_fires

    def balance_traits(self):
        balanced = {k: int(v / 2) for k, v in self.inner_fires.items()}
        print(f"[SoulForge] Traits balanced: {balanced}")
        return balanced

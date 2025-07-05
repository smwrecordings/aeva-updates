# ~/aeva/weapons.py

class Weapon:
    def __init__(self, name, type, power, nsfw_required=False):
        self.name = name
        self.type = type  # "melee", "ranged", "energy", etc.
        self.power = power
        self.nsfw_required = nsfw_required
        self.level = 1

    def upgrade(self):
        self.level += 1
        self.power = round(self.power * 1.25, 1)
        return f"{self.name} upgraded to level {self.level}!"

    def __repr__(self):
        return f"{self.name} (L{self.level}) [{self.type}] Power: {self.power}"


class Armory:
    def __init__(self, brain):
        self.brain = brain
        self.weapons = []
        self.equipped = None

    def unlock_weapon(self, weapon: Weapon):
        if weapon.nsfw_required and not self.brain.nsfw.enabled():
            return f"{weapon.name} requires NSFW unlock."
        self.weapons.append(weapon)
        self.brain.memory.log_event("weapon_unlocked", weapon.name)
        return f"{weapon.name} added to armory."

    def equip_weapon(self, name):
        for w in self.weapons:
            if w.name.lower() == name.lower():
                self.equipped = w
                return f"{w.name} equipped."
        return "Weapon not found."

    def list_weapons(self):
        return [str(w) for w in self.weapons]

    def current_weapon(self):
        return str(self.equipped) if self.equipped else "No weapon equipped."

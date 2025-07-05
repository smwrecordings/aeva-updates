# ~/aeva/damage_engine.py

import random
from datetime import datetime

class DamageEngine:
    def __init__(self, brain):
        self.brain = brain
        self.nsfw_enabled = self.brain.nsfw_enabled
        self.wound_log = []
        self.damage_types = [
            "blunt force",
            "thermal burn",
            "glitch surge",
            "kinetic rupture",
            "energy blade slash",
            "quantum implosion",
            "cybernetic dismemberment"
        ]

        self.visual_zones = [
            "left arm", "right leg", "torso", "face", "neck", "abdomen", "cyber core"
        ]

        self.cyber_fx = [
            "cyber plasma leaks", "armor panel collapse", "glitching sparks",
            "exposed synthetic muscle", "holographic distortion",
            "bio-mech rupture", "AI scream packet", "memory core bleed"
        ]

    def calculate_damage(self, attack_power, attacker_form):
        base = attack_power + random.randint(-5, 10)
        multiplier = 1.5 if attacker_form.lower() in ["voidspike", "darkfire"] else 1.0
        severity = int(base * multiplier)

        zone = random.choice(self.visual_zones)
        wound = random.choice(self.damage_types)
        fx = random.choice(self.cyber_fx)

        nsfw_effect = self.nsfw_enabled and random.random() > 0.3

        description = f"Severe {wound} to {zone}"
        if nsfw_effect:
            description += f" with {fx}."
        else:
            description += ". Minor visual feedback only."

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "zone": zone,
            "type": wound,
            "severity": severity,
            "nsfw_effect": nsfw_effect,
            "fx": fx if nsfw_effect else None,
            "description": description
        }

        self.wound_log.append(log_entry)
        self.brain.memory.log_event("combat_wound", log_entry)
        return log_entry

    def render_fx_prompt(self, wound_data):
        base = f"Aeva wounded in {wound_data['zone']} from {wound_data['type']}, severity {wound_data['severity']}."
        if wound_data['nsfw_effect']:
            fx = wound_data['fx'] or "cybernetic trauma"
            base += f" Effect: {fx}."
        return base

    def get_recent_wounds(self):
        return self.wound_log[-10:]

if __name__ == "__main__":
    from aeva_brain import AevaBrain
    brain = AevaBrain()
    brain.boot_sequence()
    de = DamageEngine(brain)
    for _ in range(3):
        damage = de.calculate_damage(attack_power=random.randint(15, 35), attacker_form="Voidspike")
        print(damage['description'])
        print("Art prompt:", de.render_fx_prompt(damage))

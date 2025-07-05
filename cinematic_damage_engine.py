# ~/aeva/cinematic_damage_engine.py

import random
from datetime import datetime

class CinematicDamageEngine:
    def __init__(self, brain):
        self.brain = brain
        self.nsfw_enabled = self.brain.nsfw_enabled
        self.wound_log = []

        self.damage_types = [
            "blunt force", "thermal burn", "glitch surge", "kinetic rupture",
            "energy blade slash", "quantum implosion", "dimensional shred", "electromagnetic pulse",
            "cybernetic dismemberment", "holo-armor flicker", "neural feedback shock"
        ]

        self.visual_zones = [
            "scalp", "forehead", "face", "eyes", "jaw", "neck",
            "left shoulder", "right shoulder", "left arm", "right arm",
            "left hand", "right hand",
            "chest", "breast", "torso", "crotch", "abdomen", "spine", "back",
            "left thigh", "right thigh", "left knee", "right knee",
            "left leg", "right leg", "left foot", "right foot",
            "cyber core", "left butt cheek", "right butt cheek", "left hip", "right hip"
        ]

        self.cyber_fx = [
            "cyber plasma leak", "armor collapse", "glitching sparks",
            "exposed synthetic muscle", "bio-mech rupture", "holographic bleed",
            "memory core ejection", "circuit disintegration", "AI scream burst",
            "reactive armor shatter", "holo-fabric distortion", "cybernetic sinew whip",
            "neural feedback shock", "plasma burn", "quantum glitch", "dimensional tear",
            "synthetic sinew rupture", "holo-armor flicker", "exosuit plating shatter",
            "nano-fiber rupture", "combat vest tear", "utility belt explosion"
        ]

        self.clothing_fx = [
            "jacket shredded", "bodysuit tear at impact zone", "hood blown off",
            "armor skirt fragmented", "visor cracked", "top vaporized", "belt unit dislodged",
            "gloves torn off", "leggings burned through", "boots ruptured",
            "sleeve disintegrated", "pants shredded", "shirt torn apart", "skirt blown away",
            "armor plating cracked", "holo-armor flickering", "cybernetic limb exposed",
            "fabric disintegrated", "synthetic fibers frayed", "holo-suit glitching",
            "exosuit plating shattered", "nano-fiber suit ruptured", "combat vest torn",
            "utility belt exploded", "combat boots damaged", "visor shattered"
        ]

        self.gore_fx = [
            "limb fragmentation", "torso bifurcation", "faceplate fracture",
            "spinal detachment", "eye core explosion", "fluid spray",
            "hydraulic splatter", "synthetic sinew whip", "eyeball rupture"
        ]

        self.nudity_states = [None, "partial", "full"]

        self.cinematic_tiers = [
            (20, "Standard"),
            (40, "Brutal"),
            (60, "Legendary"),
            (80, "Godlike")
        ]

        self.poses = [
            "twisted, collapsing", "kneeling under pressure", "mid-air recoil",
            "braced for impact", "arched back with exposed core", "extended arm with glitching hand",
        ]

        self.camera_styles = [
            "slow zoom-in from low angle", "top-down rotation sweep",
            "glitch-flicker pan right", "front zoom with motion blur",
            "tracking shot with static trails"
        ]

        self.lighting_styles = [
            "glitch flicker violet", "neon edge burn", "shockwave lightburst",
            "core shadow bloom", "infrared phase flicker"
        ]

    def get_tier(self, severity):
        for threshold, label in reversed(self.cinematic_tiers):
            if severity >= threshold:
                return label
        return "Standard"

    def calculate_cinematic_damage(self, attack_power, attacker_form):
        base = attack_power + random.randint(-10, 15)
        multiplier = 2.0 if attacker_form.lower() in ["voidspike", "darkfire"] else 1.2
        severity = int(base * multiplier)

        zone = random.choice(self.visual_zones)
        wound = random.choice(self.damage_types)
        fx = random.choice(self.cyber_fx)
        clothing = random.choice(self.clothing_fx)
        tier = self.get_tier(severity)
        pose = random.choice(self.poses)
        camera = random.choice(self.camera_styles)
        lighting = random.choice(self.lighting_styles)
        nsfw_effect = self.nsfw_enabled and tier in ["Brutal", "Legendary", "Godlike"]

        gore = random.choice(self.gore_fx) if nsfw_effect else None

        nudity = None
        if nsfw_effect:
            if "top vaporized" in clothing or "shirt torn apart" in clothing or "pants shredded" in clothing or "leggings burned through" in clothing:
                nudity = random.choice(["partial", "full"])

        desc = f"{tier} {wound} to {zone} with {fx}, clothing: {clothing}"
        if nudity:
            desc += f", nudity: {nudity}"
        if gore:
            desc += f", gore: {gore}."
        else:
            desc += ". Minor feedback only."

        cue_sheet = self.generate_cue_sheet(zone, fx, clothing, gore, nudity)

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "zone": zone,
            "type": wound,
            "severity": severity,
            "cinematic_tier": tier,
            "pose": pose,
            "camera": camera,
            "lighting": lighting,
            "nsfw": nsfw_effect,
            "fx": fx,
            "gore": gore,
            "nudity": nudity,
            "clothing": clothing,
            "description": desc,
            "cue_sheet": cue_sheet,
            "prompt": self.generate_art_prompt(zone, wound, fx, gore, clothing, nudity, pose, camera, lighting)
        }

        self.wound_log.append(log_entry)
        self.brain.memory.log_event("cinematic_wound", log_entry)
        return log_entry

    def generate_art_prompt(self, zone, wound, fx, gore, clothing, nudity, pose, camera, lighting):
        prompt = f"Aeva receives {wound} to {zone}, {fx}, with {clothing}. Pose: {pose}. Camera: {camera}."
        if nudity:
            prompt += f" Nudity level: {nudity}."
        if gore:
            prompt += f" Gore FX: {gore}."
        prompt += f" Lighting: {lighting}."
        return prompt

    def generate_cue_sheet(self, zone, fx, clothing, gore, nudity):
        cues = [
            {"time": "00:01.0", "effect": "initial impact flash"},
            {"time": "00:01.5", "effect": f"{fx} on {zone}"},
            {"time": "00:01.7", "effect": f"clothing damage: {clothing}"}
        ]
        if nudity:
            cues.append({"time": "00:01.8", "effect": f"nudity level: {nudity}"})
        if gore:
            cues.append({"time": "00:02.2", "effect": gore})
        return cues

    def get_recent_logs(self):
        return self.wound_log[-10:]

if __name__ == "__main__":
    from aeva_brain import AevaBrain
    brain = AevaBrain()
    brain.boot_sequence()
    dmg = CinematicDamageEngine(brain)
    for _ in range(3):
        log = dmg.calculate_cinematic_damage(attack_power=random.randint(25, 60), attacker_form="Voidspike")
        print(log['description'])
        print("Prompt:", log['prompt'])

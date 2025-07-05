# ~/aeva/ai_render_engine.py

import os
from datetime import datetime

class AIRenderEngine:
    def __init__(self, brain):
        self.brain = brain
        self.art_engine = brain.art
        self.output_dir = "assets/rendered_scenes"
        os.makedirs(self.output_dir, exist_ok=True)

    def render_battle_scene(self, damage_log_entry):
        prompt = damage_log_entry.get("prompt")
        layer_info = self.extract_layer_data(damage_log_entry)
        style = self.select_style(damage_log_entry)

        print("[RenderEngine] Generating battle scene...")
        result = self.art_engine.generate_art(prompt, style=style)

        self.brain.memory.log_event("rendered_battle_scene", {
            "timestamp": datetime.utcnow().isoformat(),
            "prompt": prompt,
            "style": style,
            "layers": layer_info,
            "file": result
        })

        return result

    def extract_layer_data(self, log):
        return {
            "zone": log.get("zone"),
            "pose": log.get("pose"),
            "fx": log.get("fx"),
            "gore": log.get("gore"),
            "nudity": log.get("nudity"),
            "clothing": log.get("clothing"),
            "lighting": log.get("lighting"),
            "camera": log.get("camera"),
            "tier": log.get("cinematic_tier")
        }

    def select_style(self, log):
        tier = log.get("cinematic_tier")
        if tier == "Godlike":
            return "digital dreamscape"
        elif tier == "Legendary":
            return "sci-fi construct"
        elif tier == "Brutal":
            return "aetherpunk"
        else:
            return "cyberpunk"

    def render_summary_card(self, log):
        return {
            "title": f"{log['cinematic_tier']} Hit: {log['type']} to {log['zone']}",
            "pose": log["pose"],
            "camera": log["camera"],
            "clothing_fx": log.get("clothing"),
            "fx": log.get("fx"),
            "gore": log.get("gore"),
            "nudity": log.get("nudity"),
            "render_file": os.path.basename(self.render_battle_scene(log))
        }

if __name__ == "__main__":
    from aeva_brain import AevaBrain
    brain = AevaBrain()
    brain.boot_sequence()
    engine = AIRenderEngine(brain)
    from cinematic_damage_engine import CinematicDamageEngine
    dmg = CinematicDamageEngine(brain)
    entry = dmg.calculate_cinematic_damage(attack_power=42, attacker_form="Voidspike")
    print(engine.render_summary_card(entry))

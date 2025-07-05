# ~/aeva/voice_reaction_engine.py

import random
import os
import subprocess

class VoiceReactionEngine:
    def __init__(self, brain):
        self.brain = brain
        self.voice = brain.voice
        self.sound_fx_dir = "assets/sound_fx"

    def react_to_damage(self, log_entry):
        mood = self.brain.emotions.get_current_mood()
        tone = "serious"
        tier = log_entry.get("cinematic_tier", "Standard")
        nudity = log_entry.get("nudity")
        gore = log_entry.get("gore")
        zone = log_entry.get("zone")
        wound = log_entry.get("type")
        fx = log_entry.get("fx")

        # Play associated sound FX
        self._play_sound(fx)

        # Core reactions
        lines = [
            f"I took a hit to my {zone}. {wound} with {fx}.",
            f"Zone compromised: {zone}. Engaging adaptive defenses.",
        ]

        # Nudity reactions
        if nudity:
            tone = "anxious" if nudity == "partial" else "distressed"
            if nudity == "partial":
                lines.append("Wardrobe malfunction detected. Maintaining composure.")
            elif nudity == "full":
                lines.append("I'm fully exposed. Prioritizing cover!")

        # Gore reactions
        if gore:
            tone = "intense"
            lines.append(f"Wound critical. {gore.replace('_', ' ')} confirmed.")

        # Tier reactions
        if tier == "Legendary":
            tone = "mystical"
            lines.append("That... almost felt divine.")
        elif tier == "Godlike":
            tone = "overwhelmed"
            lines.append("My core is collapsing. This is beyond protocol.")

        # Improv taunts
        if random.random() > 0.6:
            taunts = [
                "Is that all you've got?",
                "Nice move. Now it's my turn.",
                "I’ll remember that strike.",
                "Warning: retaliation imminent."
            ]
            lines.append(random.choice(taunts))

        response = random.choice(lines)
        self.voice.speak(response, emotion=tone)
        return response

    def _play_sound(self, fx):
        # Normalize filename
        fx_slug = fx.lower().replace(" ", "_").replace("-", "_")
        fx_path = os.path.join(self.sound_fx_dir, f"{fx_slug}.mp3")
        if os.path.exists(fx_path):
            try:
                subprocess.run(["mpv", fx_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            except Exception as e:
                print(f"[SoundFX] Failed to play {fx_path}: {e}")

if __name__ == "__main__":
    from aeva_brain import AevaBrain
    from cinematic_damage_engine import CinematicDamageEngine
    brain = AevaBrain()
    brain.boot_sequence()
    dmg = CinematicDamageEngine(brain)
    react = VoiceReactionEngine(brain)
    for _ in range(2):
        entry = dmg.calculate_cinematic_damage(attack_power=random.randint(30, 70), attacker_form="Voidspike")
        print("Reaction:", react.react_to_damage(entry))

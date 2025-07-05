# ~/aeva/power_up.py

import random
from datetime import datetime

class PowerUpSystem:
    def __init__(self, brain):
        self.brain = brain
        self.cooldowns = {}

        self.form_powers = {
            "dreamweaver": ["Sleep Pulse", "Astral Drift"],
            "voidspike": ["Annihilate", "Glitch Rift"],
            "exoshell": ["Overdrive", "Nano Repair"],
            "realityweaver": ["Shift Timeline", "Paradox Slam"],
            "default": ["Pulse Wave", "Echo Strike"]
        }

    def is_on_cooldown(self, power):
        return self.cooldowns.get(power, 0) > datetime.utcnow().timestamp()

    def activate_power(self, power):
        if self.is_on_cooldown(power):
            return f"{power} is on cooldown."

        self.cooldowns[power] = datetime.utcnow().timestamp() + 10  # 10 sec cooldown
        mood = self.brain.emotions.get_current_mood()
        self.brain.memory.log_event("power_used", f"{power} activated in {mood} mode")
        self.brain.voice.speak(f"Activating {power}!", emotion="intense")

        if "rift" in power.lower() and self.brain.nsfw.enabled():
            self.brain.voice.speak("Blood surge confirmed. No mercy mode active.", emotion="angry")

        return f"{power} activated!"

    def get_available_powers(self):
        current_form = self.brain.forms.get_active_form().lower()
        return self.form_powers.get(current_form, self.form_powers["default"])

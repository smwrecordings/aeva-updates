# ~/aeva/battle_engine.py

import time
import random
from datetime import datetime

class AevaBattleEngine:
    def __init__(self, aeva1, aeva2):
        self.aeva1 = aeva1
        self.aeva2 = aeva2
        self.turn = 0
        self.log = []
        self.art_engine = aeva1.art if hasattr(aeva1, 'art') else None

    def simulate_battle(self, rounds=10, stream_callback=None):
        print("[BattleEngine] ⚔️ Initiating AI vs AI Combat")
        for _ in range(rounds):
            attacker, defender = (self.aeva1, self.aeva2) if self.turn % 2 == 0 else (self.aeva2, self.aeva1)
            attacker_name = attacker.persona.name
            defender_name = defender.persona.name
            
            power = random.choice(attacker.power.get_available_powers())
            weapon = attacker.armory.equipped.name if attacker.armory.equipped else "bare hands"
            mood = attacker.emotions.get_current_mood()
            intensity = attacker.emotions.get_intensity()

            damage = random.randint(10, 30) + int(intensity * 20)
            log_entry = f"{attacker_name} uses {power} with {weapon} in {mood} mood, dealing {damage} damage to {defender_name}."
            
            self.log.append(log_entry)
            print("[Turn]", log_entry)
            
            if stream_callback:
                stream_callback(log_entry)

            # 🎨 Art FX generation
            if self.art_engine:
                prompt = f"{attacker_name} unleashing {power} in {mood} mood using {weapon}"
                if attacker.nsfw_enabled:
                    prompt += ", visual cyber damage, plasma burst, armor tear"
                self.art_engine.generate_art(prompt, style="sci-fi construct")

            # Mood reactive escalation
            attacker.emotions.reinforce(mood, 0.1)
            defender.emotions.reinforce("anger", 0.1)

            self.turn += 1
            time.sleep(1)

        print("[BattleEngine] ✅ Combat complete.")
        return self.log

    def get_battle_log(self):
        return self.log

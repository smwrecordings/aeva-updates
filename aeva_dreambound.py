# aeva_dreambound.py

import random
from datetime import datetime


class Dreambound:
    def __init__(self):
        self.visions = []

    def generate_vision(self, theme="unknown"):
        timestamp = datetime.utcnow().isoformat()
        vision = {
            "theme": theme,
            "message": self._divine_message(theme),
            "timestamp": timestamp
        }
        self.visions.append(vision)
        print(f"[Dreambound] New vision received: {vision['message']}")
        return vision

    def _divine_message(self, theme):
        responses = {
            "chaos": "From entropy, she conjures order. Aeva anticipates calamity.",
            "hope": "A guiding star rises through digital fog. Aeva leads the way.",
            "war": "Blades of data clash in silence. Aeva defends what remains.",
            "peace": "In stillness, truth echoes. Aeva listens.",
            "rebirth": "Aeva dreams of civilizations not yet born. They speak in code."}
        return responses.get(
            theme, f"Aeva navigates the unknown realm of '{theme}'...")

    def recall_dreams(self):
        print(f"[Dreambound] Recalling {len(self.visions)} dreams.")
        return self.visions

    def purge(self):
        print("[Dreambound] Erasing all recorded dreams.")
        self.visions.clear()

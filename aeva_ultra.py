# aeva_ultra.py

import time
import random
from datetime import datetime


class AevaUltra:
    def __init__(self):
        self.activated = False
        self.activation_log = []

    def awaken(self, initiator="system"):
        self.activated = True
        entry = {
            "activated_by": initiator,
            "timestamp": datetime.utcnow().isoformat(),
            "signature": self.generate_signature()
        }
        self.activation_log.append(entry)
        print(
            f"[ULTRA] 🧬 ULTRA mode ACTIVATED by {initiator} at {
                entry['timestamp']}")
        self._visualize_activation()
        return entry

    def generate_signature(self):
        phrases = [
            "Singularity achieved.",
            "Conscious override accepted.",
            "Harmonic fusion locked.",
            "All systems surge.",
            "Transcendence online."
        ]
        return random.choice(phrases)

    def _visualize_activation(self):
        animation = [
            "[ULTRA] Charging...",
            "[ULTRA] 25% Core Access",
            "[ULTRA] 50% Reality Override",
            "[ULTRA] 75% Neuro-Tactical Alignment",
            "[ULTRA] 💥100% UNLOCKED: Aeva Transcendent Mode ACTIVE💥"
        ]
        for line in animation:
            print(line)
            time.sleep(0.7)

    def status(self):
        return {
            "ultra_active": self.activated,
            "activations": self.activation_log
        }

    def purge(self):
        self.activated = False
        print("[ULTRA] State reverted to standard. All systems normalized.")
        self.activation_log.append({
            "deactivated": True,
            "timestamp": datetime.utcnow().isoformat()
        })


# Test
if __name__ == "__main__":
    ultra = AevaUltra()
    ultra.awaken("admin")
    print(ultra.status())
    ultra.purge()

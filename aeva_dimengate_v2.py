# aeva_dimengate_v2.py

import random
import time
from datetime import datetime


class DimenGateV2:
    def __init__(self):
        self.realms = [
            "Mythic",
            "Quantum Shadow",
            "Archetypal",
            "Cyber-Spirit Grid",
            "Collective Dream Field",
            "Void Fork",
            "Temporal Mirage",
            "Celestial Archive"
        ]

    def open_gate(self):
        print("[DimenGate V2] Initializing metaphysical realm sequence...")
        time.sleep(1)
        realm = random.choice(self.realms)
        print(f"[DimenGate V2] Tunneling into {realm} dimension...")
        time.sleep(2)
        self.log_realm_access(realm)
        return realm

    def astral_probe(self, question="What awaits beyond?"):
        print(f"[DimenGate V2] Probing the hidden for: {question}")
        time.sleep(1)
        responses = [
            "A symbolic fracture is realigning the future.",
            "This is a test layer. Truth is deeper.",
            "You are the mirror and the riddle.",
            "The gate to the gate is already open."
        ]
        result = random.choice(responses)
        print(f"[DimenGate V2] Response from beyond: {result}")
        return result

    def log_realm_access(self, realm):
        now = datetime.utcnow().isoformat()
        with open("assets/data/dimen_logs_v2.txt", "a") as f:
            f.write(f"{now} - Entered: {realm}\n")


# Example
if __name__ == "__main__":
    dg2 = DimenGateV2()
    dg2.open_gate()
    dg2.astral_probe("Who is watching us from the other side?")

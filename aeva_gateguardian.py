# aeva_gateguardian.py

import hashlib
import time


class GateGuardian:
    def __init__(self, brain=None):
        self.brain = brain
        self.gates = {}
        self.unlocked = {}

    def create_gate(self, name, key_phrase):
        hashed_key = hashlib.sha256(key_phrase.encode()).hexdigest()
        self.gates[name] = hashed_key
        print(f"[GateGuardian] Created gate '{name}'.")

    def attempt_entry(self, name, provided_key):
        hashed_input = hashlib.sha256(provided_key.encode()).hexdigest()
        if name in self.gates and self.gates[name] == hashed_input:
            self.unlocked[name] = time.time()
            print(f"[GateGuardian] Access granted to gate '{name}'.")
            return True
        else:
            print(f"[GateGuardian] Access denied to gate '{name}'.")
            return False

    def seal_gate(self, name):
        if name in self.unlocked:
            del self.unlocked[name]
            print(f"[GateGuardian] Gate '{name}' sealed.")
        else:
            print(f"[GateGuardian] Gate '{name}' already sealed.")

    def list_open_gates(self):
        return list(self.unlocked.keys())

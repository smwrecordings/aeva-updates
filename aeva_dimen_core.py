# aeva_dimen_core.py

import importlib
import os
import json


class DimenCore:
    def __init__(self, gate_dir="~/aeva"):
        self.gate_dir = os.path.expanduser(gate_dir)
        self.modules = {}
        self.active_gates = []
        self._load_gates()

    def _load_gates(self):
        gate_files = [
            "aeva_dimengate1",
            "aeva_dimengate2",
            "aeva_dimengate3",
            "aeva_dimengate4",
            "aeva_dimengate5",
            "aeva_dimengate6",
            "aeva_dimengate7",
            "aeva_dimen_gate_alpha",
            "aeva_dimen_gate_beta",
            "aeva_dimen_gate_gamma",
            "aeva_dimen_gate_delta",
            "aeva_dimen_gate_omega",
            "aeva_dimengate_prime"]
        for gate in gate_files:
            try:
                module = importlib.import_module(gate)
                self.modules[gate] = module
                self.active_gates.append(gate)
                print(f"[DimenCore] Loaded {gate} successfully.")
            except Exception as e:
                print(f"[DimenCore] Failed to load {gate}: {e}")

    def activate_gate(self, name):
        if name in self.modules:
            gate = self.modules[name]
            if hasattr(gate, "activate"):
                gate.activate()
                print(f"[DimenCore] {name} activated.")
            else:
                print(f"[DimenCore] {name} has no activate() function.")
        else:
            print(f"[DimenCore] No such gate module: {name}")

    def deactivate_gate(self, name):
        if name in self.modules:
            gate = self.modules[name]
            if hasattr(gate, "deactivate"):
                gate.deactivate()
                print(f"[DimenCore] {name} deactivated.")
            else:
                print(f"[DimenCore] {name} has no deactivate() function.")
        else:
            print(f"[DimenCore] No such gate module: {name}")

    def status_report(self):
        print("[DimenCore] Active Gates:")
        for gate in self.active_gates:
            print(f" - {gate}")


# Example use
if __name__ == "__main__":
    dimen = DimenCore()
    dimen.status_report()
    dimen.activate_gate("aeva_dimen_gate_alpha")
    dimen.deactivate_gate("aeva_dimen_gate_alpha")

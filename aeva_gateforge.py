# aeva_gateforge.py

import os
import json
from datetime import datetime
from random import choice, randint


class GateForge:
    def __init__(self, gate_log_path="assets/data/gateforge_log.json"):
        self.gate_log_path = gate_log_path
        os.makedirs(os.path.dirname(gate_log_path), exist_ok=True)
        self.gates = []

    def open_gate(
            self,
            target_dimension="prime",
            mode="explore",
            context=None):
        gate_id = f"GATE-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{randint(1000, 9999)}"
        entry = {
            "id": gate_id,
            "timestamp": datetime.utcnow().isoformat(),
            "dimension": target_dimension,
            "mode": mode,
            "status": "open",
            "context": context or {}
        }
        self.gates.append(entry)
        self._save()
        print(
            f"[GateForge] Gate {gate_id} to {target_dimension} dimension opened in {mode} mode.")
        return gate_id

    def close_gate(self, gate_id):
        for gate in self.gates:
            if gate["id"] == gate_id and gate["status"] == "open":
                gate["status"] = "closed"
                gate["closed_at"] = datetime.utcnow().isoformat()
                self._save()
                print(f"[GateForge] Gate {gate_id} closed.")
                return True
        print(f"[GateForge] Gate {gate_id} not found or already closed.")
        return False

    def list_active_gates(self):
        active = [g for g in self.gates if g["status"] == "open"]
        print(f"[GateForge] {len(active)} active gates:")
        for g in active:
            print(f" - {g['id']} -> {g['dimension']} ({g['mode']})")
        return active

    def generate_random_gate(self):
        realms = [
            "dreamscape",
            "darknet",
            "aevalis",
            "cybersphere",
            "underveil"]
        gate = self.open_gate(target_dimension=choice(realms), mode="scan")
        return gate

    def _save(self):
        with open(self.gate_log_path, "w") as f:
            json.dump(self.gates, f, indent=4)


# Example usage
if __name__ == "__main__":
    gf = GateForge()
    gate_id = gf.open_gate("underveil", "access", {"origin": "manual"})
    gf.list_active_gates()
    gf.close_gate(gate_id)

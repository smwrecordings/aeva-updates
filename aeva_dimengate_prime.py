# aeva_dimengate_prime.py

import os
import json
import time
from datetime import datetime
from uuid import uuid4


class DimenGatePrime:
    def __init__(self, registry_path="assets/data/dimengates.json"):
        self.registry_path = registry_path
        os.makedirs(os.path.dirname(self.registry_path), exist_ok=True)
        self.dimensions = {}
        self.load_registry()

    def load_registry(self):
        if os.path.exists(self.registry_path):
            with open(self.registry_path, "r") as f:
                self.dimensions = json.load(f)
        else:
            self.save_registry()

    def save_registry(self):
        with open(self.registry_path, "w") as f:
            json.dump(self.dimensions, f, indent=4)

    def create_gate(self, name, properties=None):
        gate_id = str(uuid4())
        timestamp = datetime.utcnow().isoformat()
        dimension = {
            "id": gate_id,
            "name": name,
            "properties": properties or {
                "phase_shift": "neutral",
                "temporal_distortion": "stable",
                "access_level": "locked"
            },
            "created_at": timestamp
        }
        self.dimensions[gate_id] = dimension
        self.save_registry()
        print(f"[DimenGatePrime] Gate '{name}' created.")
        return gate_id

    def activate_gate(self, gate_id):
        if gate_id in self.dimensions:
            dim = self.dimensions[gate_id]
            dim["properties"]["access_level"] = "active"
            dim["properties"]["last_accessed"] = datetime.utcnow().isoformat()
            self.save_registry()
            print(
                f"[DimenGatePrime] Activated gate: {
                    dim['name']} [{gate_id}]")
            return dim
        else:
            print("[DimenGatePrime] Gate ID not found.")
            return None

    def list_gates(self):
        print("[DimenGatePrime] Listing all dimensional gates:")
        for gate_id, dim in self.dimensions.items():
            print(
                f" - {dim['name']} ({gate_id}): {dim['properties']['access_level']}")
        return list(self.dimensions.values())

    def collapse_gate(self, gate_id):
        if gate_id in self.dimensions:
            del self.dimensions[gate_id]
            self.save_registry()
            print(f"[DimenGatePrime] Gate [{gate_id}] collapsed.")
        else:
            print("[DimenGatePrime] Gate ID not found.")


# Example usage
if __name__ == "__main__":
    dg = DimenGatePrime()
    gate_id = dg.create_gate("Nexus-9",
                             {"phase_shift": "volatile",
                              "temporal_distortion": "flux"})
    dg.activate_gate(gate_id)
    dg.list_gates()

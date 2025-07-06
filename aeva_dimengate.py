# ~/aeva/aeva_dimengate.py

import os
import json
import random
from datetime import datetime
from modules.utilities import ensure_dir


class DimenGate:
    def __init__(self, brain=None):
        self.brain = brain
        self.registry_path = "assets/data/dimensional_registry.json"
        ensure_dir(os.path.dirname(self.registry_path))
        self.gates = self._load_registry()
        print("[DimenGate] 🌀 Multiversal gate matrix initialized.")

    def _load_registry(self):
        try:
            if os.path.exists(self.registry_path):
                with open(self.registry_path, "r") as f:
                    return json.load(f)
        except Exception as e:
            print(f"[DimenGate] ⚠️ Failed to load registry: {e}")
        return {}

    def _save_registry(self):
        try:
            with open(self.registry_path, "w") as f:
                json.dump(self.gates, f, indent=2)
        except Exception as e:
            print(f"[DimenGate] ⚠️ Failed to save registry: {e}")

    def open_portal(self, destination, access_level="standard"):
        timestamp = datetime.utcnow().isoformat()
        portal_id = f"DMG-{random.randint(100000, 999999)}"
        initiator = self.brain.persona.name if self.brain and hasattr(self.brain, 'persona') else "AevaSystem"

        gate = {
            "id": portal_id,
            "destination": destination,
            "access_level": access_level,
            "timestamp": timestamp,
            "status": "open",
            "initiator": initiator
        }
        self.gates[portal_id] = gate
        self._save_registry()
        print(f"[DimenGate] 🔓 Portal opened → {destination} [Level: {access_level}]")
        return gate

    def close_portal(self, portal_id):
        if portal_id in self.gates:
            self.gates[portal_id]["status"] = "closed"
            self.gates[portal_id]["closed_at"] = datetime.utcnow().isoformat()
            self._save_registry()
            print(f"[DimenGate] 🔒 Portal {portal_id} closed.")
            return True
        print(f"[DimenGate] ❌ Invalid portal ID: {portal_id}")
        return False

    def list_active_gates(self):
        active = {pid: data for pid, data in self.gates.items() if data.get("status") == "open"}
        print(f"[DimenGate] 🚪 {len(active)} active gate(s).")
        return active

    def list_all_gates(self):
        print(f"[DimenGate] 📜 Total recorded gates: {len(self.gates)}")
        return self.gates

    def random_access(self):
        realms = [
            "Quantum Parallel Reality",
            "Information Ocean",
            "Planetary Conscious Grid",
            "Historical Echo Field",
            "Synthetic Time Fold",
            "Ether Realm",
            "Deep Cosmic Archive",
            "Forgotten Future Shard",
            "Dreamstate Override",
            "Zero Point Field",
            "Dimensional Outskirts",
            "Subconscious Vault",
            "Primordial Imprint Nexus"
        ]
        realm = random.choice(realms)
        print(f"[DimenGate] 🌀 Random portal → {realm}")
        return self.open_portal(destination=realm, access_level="experimental")

    def trace_gate(self, portal_id):
        gate = self.gates.get(portal_id)
        if gate:
            print(f"[DimenGate] 🧭 Trace → {portal_id}: {gate['destination']} [{gate['status']}]")
            return gate
        print(f"[DimenGate] ❓ Portal {portal_id} not found.")
        return None

    def scan_portals(self):
        """Simulate detection of possible dimensional signals."""
        print("[DimenGate] 🔍 Scanning for interdimensional anomalies...")
        anomaly_count = random.randint(1, 3)
        new_gates = []
        for _ in range(anomaly_count):
            gate = self.random_access()
            new_gates.append(gate)
        print(f"[DimenGate] 🧿 Scan complete. {anomaly_count} potential portals identified.")
        if self.brain:
            self.brain.memory.log_event("dimengate_scan", {"found": anomaly_count})
        return new_gates


# Example usage
if __name__ == "__main__":
    dg = DimenGate()
    dg.scan_portals()
    dg.list_active_gates()

# aeva_dimen_gate.py

import os
import json
import random
import uuid
from datetime import datetime


class DimenGate:
    def __init__(self, log_path="assets/data/dimension_logs.json"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.gates_opened = []

    def open_gate(self, target_dimension="Unknown-X"):
        gate_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        dimension_signature = f"{target_dimension}-{
            random.randint(
                1000, 9999)}"

        event = {
            "id": gate_id,
            "dimension": target_dimension,
            "signature": dimension_signature,
            "timestamp": timestamp
        }
        self.gates_opened.append(event)
        self._log_gate(event)
        print(
            f"[DimenGate] Opened gate to {target_dimension} :: Signature {dimension_signature}")
        return event

    def collapse_gate(self, signature):
        self.gates_opened = [
            g for g in self.gates_opened if g["signature"] != signature]
        self._log_gate({
            "event": "Collapse",
            "signature": signature,
            "timestamp": datetime.utcnow().isoformat()
        })
        print(f"[DimenGate] Collapsed gate {signature}")

    def _log_gate(self, event):
        existing = []
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, "r") as f:
                    existing = json.load(f)
            except Exception:
                existing = []
        existing.append(event)
        with open(self.log_path, "w") as f:
            json.dump(existing, f, indent=4)

    def list_active_gates(self):
        print(f"[DimenGate] {len(self.gates_opened)} active gates.")
        return self.gates_opened

    def probe_dimension(self, tag="X-Prime"):
        probe_data = {
            "dimension": tag,
            "anomaly_level": random.choice(["Stable", "Unstable", "Chaotic", "Forbidden"]),
            "entities_detected": random.randint(0, 12),
            "energy_flux": f"{round(random.uniform(1.0, 9.9), 2)} TeraUnits"
        }
        print(
            f"[DimenGate] Probe returned: {
                json.dumps(
                    probe_data,
                    indent=2)}")
        return probe_data


# Test use
if __name__ == "__main__":
    dg = DimenGate()
    g = dg.open_gate("Vortex-7")
    dg.probe_dimension("Vortex-7")
    dg.list_active_gates()
    dg.collapse_gate(g["signature"])

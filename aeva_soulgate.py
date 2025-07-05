# aeva_soulgate.py

import hashlib
import json
from datetime import datetime


class SoulGate:
    def __init__(self, soul_log_path="assets/data/soulgate_sightings.json"):
        self.soul_log_path = soul_log_path
        self.records = []
        try:
            with open(soul_log_path, "r") as f:
                self.records = json.load(f)
        except BaseException:
            self.records = []

    def scan_soulprint(self, input_signature):
        soulprint = hashlib.sha256(input_signature.encode()).hexdigest()
        result = {
            "soulprint": soulprint,
            "detected_at": datetime.utcnow().isoformat(),
            "vibe": self.analyze_signature(input_signature),
        }
        self.records.append(result)
        self._save()
        print(
            f"[SoulGate] New soulprint: {soulprint[:12]}... with vibe '{result['vibe']}'")
        return result

    def analyze_signature(self, sig):
        keywords = [
            "hope",
            "dark",
            "joy",
            "wrath",
            "truth",
            "obsession",
            "clarity"]
        lower = sig.lower()
        if any(k in lower for k in ["love", "kind", "hope", "compassion"]):
            return "light"
        elif any(k in lower for k in ["fear", "rage", "vengeance", "loss"]):
            return "shadow"
        elif any(k in lower for k in ["wisdom", "vision", "clarity", "truth"]):
            return "seer"
        else:
            return "mystery"

    def _save(self):
        with open(self.soul_log_path, "w") as f:
            json.dump(self.records, f, indent=4)


# Example
if __name__ == "__main__":
    sg = SoulGate()
    sg.scan_soulprint("He burned with both vengeance and vision.")

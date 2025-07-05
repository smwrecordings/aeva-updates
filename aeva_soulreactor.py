# aeva_soulreactor.py

import hashlib
import os
import json
from datetime import datetime


class SoulReactor:
    def __init__(self, data_dir="assets/data/soulreactor"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.soul_cache = {}

    def register_soul_signature(self, name, attributes):
        signature = self._generate_signature(name, attributes)
        timestamp = datetime.utcnow().isoformat()
        soul_id = hashlib.sha256(f"{name}{timestamp}".encode()).hexdigest()
        soul_data = {
            "soul_id": soul_id,
            "name": name,
            "attributes": attributes,
            "signature": signature,
            "timestamp": timestamp
        }
        self._save_soul_data(soul_data)
        print(f"[SoulReactor] Soul signature registered for {name}.")
        return soul_id

    def _generate_signature(self, name, attributes):
        raw = json.dumps(
            {"name": name, "attributes": attributes}, sort_keys=True)
        return hashlib.sha512(raw.encode()).hexdigest()

    def _save_soul_data(self, soul_data):
        path = os.path.join(self.data_dir, f"{soul_data['soul_id']}.json")
        with open(path, "w") as f:
            json.dump(soul_data, f, indent=4)
        self.soul_cache[soul_data['soul_id']] = soul_data

    def retrieve_signature(self, soul_id):
        if soul_id in self.soul_cache:
            return self.soul_cache[soul_id]["signature"]
        path = os.path.join(self.data_dir, f"{soul_id}.json")
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
                self.soul_cache[soul_id] = data
                return data["signature"]
        return None


# Example usage
if __name__ == "__main__":
    reactor = SoulReactor()
    soul_id = reactor.register_soul_signature(
        "Aeva", {
            "will": "unbreakable", "purpose": "guidance", "essence": "light and shadow"})
    print("Soul Signature:", reactor.retrieve_signature(soul_id))

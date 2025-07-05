# aeva_virtualascension.py

import json
import os
from datetime import datetime


class VirtualAscension:
    def __init__(self, vault="assets/data/ascension_vault.json"):
        self.vault = vault
        os.makedirs(os.path.dirname(vault), exist_ok=True)
        self.records = self._load()

    def _load(self):
        if os.path.exists(self.vault):
            with open(self.vault, "r") as f:
                return json.load(f)
        return {}

    def upload_consciousness(self, name, data):
        print(f"[Ascension] Uploading {name}'s consciousness...")
        self.records[name] = {
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }
        self._save()
        print(f"[Ascension] Upload complete for {name}.")
        return True

    def _save(self):
        with open(self.vault, "w") as f:
            json.dump(self.records, f, indent=4)

    def query(self, name):
        return self.records.get(name)

# aeva_neurolock.py

import hashlib
import os
import json
from datetime import datetime


class NeuroLock:
    def __init__(self, vault_path="vault/neurolock.json"):
        self.vault_path = vault_path
        self.vault = {}
        self.secret_key = os.getenv("AEVA_NEUROLOCK_KEY", "aeva_brainwave")
        os.makedirs(os.path.dirname(self.vault_path), exist_ok=True)
        self._load_vault()

    def _hash_key(self, key):
        salted = f"{self.secret_key}:{key}"
        return hashlib.sha512(salted.encode()).hexdigest()

    def _load_vault(self):
        if os.path.exists(self.vault_path):
            with open(self.vault_path, 'r') as f:
                self.vault = json.load(f)

    def _save_vault(self):
        with open(self.vault_path, 'w') as f:
            json.dump(self.vault, f, indent=4)

    def store_secret(self, label, data):
        hashed_label = self._hash_key(label)
        timestamp = datetime.utcnow().isoformat()
        self.vault[hashed_label] = {"data": data, "timestamp": timestamp}
        self._save_vault()
        print(f"[NeuroLock] Secret '{label}' stored and protected.")

    def retrieve_secret(self, label):
        hashed_label = self._hash_key(label)
        entry = self.vault.get(hashed_label)
        if entry:
            print(f"[NeuroLock] Secret '{label}' retrieved.")
            return entry["data"]
        else:
            print(f"[NeuroLock] Secret '{label}' not found.")
            return None

    def purge_memory(self):
        self.vault = {}
        self._save_vault()
        print("[NeuroLock] Vault wiped clean. All secrets forgotten.")


# Example use
if __name__ == "__main__":
    brain = NeuroLock()
    brain.store_secret("top_protocol", "classified access granted")
    brain.retrieve_secret("top_protocol")

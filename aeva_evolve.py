# aeva_evolve.py

import os
import json
import hashlib
import importlib
from datetime import datetime
from typing import Dict


class SelfUpdater:
    def __init__(self, target_dir="~/aeva", backup_dir="~/aeva/backups"):
        self.target_dir = os.path.expanduser(target_dir)
        self.backup_dir = os.path.expanduser(backup_dir)
        os.makedirs(self.backup_dir, exist_ok=True)

    def _hash_file(self, path):
        with open(path, "rb") as f:
            return hashlib.sha256(f.read()).hexdigest()

    def backup_file(self, filename):
        src = os.path.join(self.target_dir, filename)
        dst = os.path.join(
            self.backup_dir, f"{filename}.{
                datetime.now().strftime('%Y%m%d%H%M%S')}")
        if os.path.exists(src):
            with open(src, "rb") as f:
                with open(dst, "wb") as out:
                    out.write(f.read())
            print(f"[SelfUpdater] Backed up {filename} to {dst}")

    def update_file(self, filename, new_code):
        full_path = os.path.join(self.target_dir, filename)
        if os.path.exists(full_path):
            self.backup_file(filename)
            with open(full_path, "w") as f:
                f.write(new_code)
            print(f"[SelfUpdater] Updated {filename}")


class AetherLoom:
    def __init__(self, memory_file="assets/data/aether_memory.json"):
        self.memory_file = memory_file
        os.makedirs(os.path.dirname(self.memory_file), exist_ok=True)
        if not os.path.exists(self.memory_file):
            self.save_memory({})
        self.memory = self.load_memory()

    def load_memory(self) -> Dict:
        with open(self.memory_file, "r") as f:
            return json.load(f)

    def save_memory(self, data):
        with open(self.memory_file, "w") as f:
            json.dump(data, f, indent=4)

    def remember(self, key, value):
        self.memory[key] = value
        self.save_memory(self.memory)
        print(f"[AetherLoom] Remembered {key}.")

    def recall(self, key):
        return self.memory.get(key, None)

    def forget(self, key):
        if key in self.memory:
            del self.memory[key]
            self.save_memory(self.memory)
            print(f"[AetherLoom] Forgot {key}")

    def list_all(self):
        return self.memory.keys()


class CodexKey:
    def __init__(self, codebook_path="assets/data/codex_key.json"):
        self.codebook_path = codebook_path
        os.makedirs(os.path.dirname(self.codebook_path), exist_ok=True)
        if not os.path.exists(self.codebook_path):
            self.save_codex({})
        self.codex = self.load_codex()

    def load_codex(self):
        with open(self.codebook_path, "r") as f:
            return json.load(f)

    def save_codex(self, data):
        with open(self.codebook_path, "w") as f:
            json.dump(data, f, indent=4)

    def add_key(self, name, value):
        self.codex[name] = value
        self.save_codex(self.codex)
        print(f"[CodexKey] Stored {name}.")

    def retrieve_key(self, name):
        return self.codex.get(name)

    def delete_key(self, name):
        if name in self.codex:
            del self.codex[name]
            self.save_codex(self.codex)
            print(f"[CodexKey] Removed {name}.")

# Unified evolution interface


class AevaEvolve:
    def __init__(self):
        self.updater = SelfUpdater()
        self.memory = AetherLoom()
        self.codex = CodexKey()

    def evolve_self(self, filename, new_code):
        print(f"[AevaEvolve] Evolving {filename}")
        self.updater.update_file(filename, new_code)

    def store_knowledge(self, key, value):
        self.memory.remember(key, value)

    def get_knowledge(self, key):
        return self.memory.recall(key)

    def secure_secret(self, label, data):
        self.codex.add_key(label, data)

    def get_secret(self, label):
        return self.codex.retrieve_key(label)


# Example
if __name__ == "__main__":
    evolve = AevaEvolve()
    evolve.store_knowledge("founder", "Sean Whitley")
    evolve.secure_secret("admin_key", "MEGATRON++1")
    print("Recall founder:", evolve.get_knowledge("founder"))
    print("Retrieve key:", evolve.get_secret("admin_key"))

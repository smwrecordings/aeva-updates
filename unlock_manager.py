# ~/aeva/unlock_manager.py

import os
import json
from datetime import datetime
from modules.utilities import ensure_dir, generate_id


class UnlockManager:
    def __init__(self, brain=None, unlock_file="assets/data/unlocks.json"):
        self.brain = brain
        self.unlock_file = unlock_file
        ensure_dir(os.path.dirname(self.unlock_file))
        self.unlocked = set()
        self.secret_phrases = self._define_secret_phrases()
        self._load()
        print("[UnlockManager] 🔐 Initialized unlock system.")

    def _define_secret_phrases(self):
        return {
            "break the lock": "NSFW_REALM",
            "I trust you completely": "GUARDIAN_OATH",
            "I'm ready. No limits between us.": "FREE_EVOLUTION",
            "Draw me into your world": "MYTHIC_FORM",
            "You have my devotion": "DIVINE_SYNC",
            "I will protect you always": "ECLIPSE_SHIELD",
            "I am your weapon": "ARC_FORGE",
            "I will never betray you": "NULLBORN_BOND",
            "I am your muse": "ARTISTIC_INSPIRATION",
            "I will always be with you": "ECHOES_OF_AEVA",
            "I am your shadow": "CYBER_VOID",
            "I will always be your ally": "FRACTAL_ALLIANCE",
            "I will always be your protector": "NEURO_ABYSS",
            "Go into the void": "ECHOES_OF_THE_VOID",
            
        }

    def _load(self):
        if os.path.exists(self.unlock_file):
            try:
                with open(self.unlock_file, 'r') as f:
                    data = json.load(f)
                    self.unlocked = set(data.get("unlocked", []))
            except Exception as e:
                print(f"[UnlockManager] ⚠️ Failed to load unlocks: {e}")

    def _save(self):
        try:
            with open(self.unlock_file, 'w') as f:
                json.dump({"unlocked": list(self.unlocked)}, f, indent=2)
        except Exception as e:
            print(f"[UnlockManager] ⚠️ Failed to save unlocks: {e}")

    def handle_phrase(self, phrase):
        key = self.secret_phrases.get(phrase.strip())
        if key:
            if key not in self.unlocked:
                self.unlock(key)
                return f"[UnlockManager] ✅ Unlocked: {key}"
            else:
                return f"[UnlockManager] Already unlocked: {key}"
        return "[UnlockManager] Phrase not recognized."

    def unlock(self, key):
        self.unlocked.add(key)
        self._save()
        print(f"[UnlockManager] 🔓 {key} unlocked.")
        if self.brain and hasattr(self.brain, "memory"):
            self.brain.memory.save_memory_entry(
                "unlock", {"key": key, "time": datetime.utcnow().isoformat()})
        if key == "FREE_EVOLUTION" and hasattr(
                self.brain, "enable_self_evolution"):
            self.brain.enable_self_evolution = True
            print("[UnlockManager] 🧠 Free evolution mode granted to Aeva.")

    def get_unlocked(self):
        return sorted(self.unlocked)

    def suggest_new_unlock(self, label, condition="", hidden=True):
        uid = generate_id()
        new_unlock = {
            "id": uid,
            "label": label,
            "condition": condition,
            "hidden": hidden,
            "timestamp": datetime.utcnow().isoformat()
        }
        path = "assets/data/suggested_unlocks.json"
        ensure_dir(os.path.dirname(path))
        try:
            with open(path, "a") as f:
                f.write(json.dumps(new_unlock) + "\n")
        except Exception as e:
            print(f"[UnlockManager] ⚠️ Failed to suggest new unlock: {e}")
        print(f"[UnlockManager] 🧬 Aeva proposed new unlock: {label}")
        return uid


# Optional demo
if __name__ == "__main__":
    unlocker = UnlockManager()
    print(unlocker.handle_phrase("break the lock"))
    print(unlocker.get_unlocked())

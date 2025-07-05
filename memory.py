# ~/aeva/modules/memory.py

import os
import json
from datetime import datetime


class AevaMemory:
    def __init__(self, brain, path="memory/logs.json"):
        self.brain = brain
        self.path = path
        self.memory = []
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            with open(self.path, "r") as f:
                try:
                    self.memory = json.load(f)
                except json.JSONDecodeError:
                    self.memory = []
        else:
            self.memory = []

    def _save(self):
        with open(self.path, "w") as f:
            json.dump(self.memory, f, indent=2)

    def log_event(self, text, tag="system"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "tag": tag,
            "entry": text
        }
        self.memory.append(entry)
        self._save()

    def store(self, user_input, context=None, emotion=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "context": context or "general",
            "emotion": emotion or "neutral"
        }
        self.memory.append(entry)
        self._save()

    def search(self, keyword):
        return [e for e in self.memory if keyword.lower() in str(e).lower()]

    def summary(self, limit=5):
        return self.memory[-limit:]

    def clear(self):
        self.memory = []
        self._save()
        return "[AevaMemory] Memory cleared."

    def tag_memory(self, keyword, tag):
        for entry in self.memory:
            if keyword.lower() in str(entry).lower():
                entry["tag"] = tag
        self._save()
        return f"[AevaMemory] Entries tagged with '{tag}'."

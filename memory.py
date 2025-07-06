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
            try:
                with open(self.path, "r") as f:
                    self.memory = json.load(f)
            except json.JSONDecodeError:
                print("[AevaMemory] ⚠️ Failed to decode memory log. Starting fresh.")
                self.memory = []
        else:
            self.memory = []

    def _save(self):
        try:
            with open(self.path, "w") as f:
                json.dump(self.memory, f, indent=2)
        except Exception as e:
            print(f"[AevaMemory] ⚠️ Failed to save memory: {e}")

    def log_event(self, text, tag="system"):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "tag": tag,
            "entry": str(text)
        }
        self.memory.append(entry)
        self._save()

    def store(self, user_input, context=None, emotion=None):
        if not isinstance(user_input, str):
            user_input = str(user_input)
        if not isinstance(context, str):
            context = str(context)
        if not isinstance(emotion, str):
            emotion = str(emotion)

        entry = {
            "timestamp": datetime.now().isoformat(),
            "input": user_input,
            "context": context or "general",
            "emotion": emotion or "neutral"
        }
        self.memory.append(entry)
        self._save()

    def search(self, keyword):
        try:
            if not isinstance(keyword, str):
                keyword = str(keyword)
            return [e for e in self.memory if keyword.lower() in str(e).lower()]
        except Exception as e:
            print(f"[AevaMemory] Search error: {e}")
            return []

    def summary(self, limit=5):
        return self.memory[-limit:]

    def clear(self):
        self.memory = []
        self._save()
        return "[AevaMemory] Memory cleared."

    def tag_memory(self, keyword, tag):
        try:
            if not isinstance(keyword, str):
                keyword = str(keyword)
            for entry in self.memory:
                if keyword.lower() in str(entry).lower():
                    entry["tag"] = tag
            self._save()
            return f"[AevaMemory] Entries tagged with '{tag}'."
        except Exception as e:
            return f"[AevaMemory] Tagging failed: {e}"

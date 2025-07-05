# ~/aeva/form_memory.py

import os
import json
from datetime import datetime
from modules.utilities import ensure_dir


class FormMemory:
    def __init__(self, brain=None, path="assets/data/form_memory.json"):
        self.brain = brain
        self.path = path
        self.forms = []
        ensure_dir(os.path.dirname(self.path))
        self._load()

    def _load(self):
        if os.path.exists(self.path):
            try:
                with open(self.path, 'r') as f:
                    self.forms = json.load(f)
            except Exception as e:
                print(f"[FormMemory] Failed to load forms: {e}")
                self.forms = []

    def _save(self):
        try:
            with open(self.path, 'w') as f:
                json.dump(self.forms, f, indent=2)
        except Exception as e:
            print(f"[FormMemory] Save error: {e}")

    def remember_form(self, name, style, art_style, metadata=None):
        form = {
            "name": name,
            "style": style,
            "art_style": art_style,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {}
        }
        self.forms.append(form)
        self._save()
        print(f"[FormMemory] Form remembered: {name} in {art_style} style")

    def get_form(self, name):
        for form in self.forms:
            if form["name"].lower() == name.lower():
                print(f"[FormMemory] Form found: {name}")
                return form
        print(f"[FormMemory] Form not found: {name}")
        return None

    def list_forms(self):
        print(f"[FormMemory] Listing {len(self.forms)} forms")
        return self.forms

    def delete_form(self, name):
        original_count = len(self.forms)
        self.forms = [f for f in self.forms if f["name"].lower()
                      != name.lower()]
        self._save()
        print(
            f"[FormMemory] Deleted form '{name}' ({original_count - len(self.forms)} removed)")


# Optional test
if __name__ == "__main__":
    fm = FormMemory()
    fm.remember_form("Aeva Neo", "cyber ninja", "anime", {"favorite": True})
    print(fm.get_form("Aeva Neo"))
    print(fm.list_forms())

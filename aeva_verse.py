# aeva_verse.py

import os
import json
import uuid
from datetime import datetime
from modules.utilities import log_event


class AevaVerse:
    def __init__(self, save_path="assets/data/aeva_verse_state.json"):
        self.save_path = save_path
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        self.verses = {}  # ID: Verse
        self.active_verse = None
        self._load_state()

    def _load_state(self):
        if os.path.exists(self.save_path):
            with open(self.save_path, 'r') as f:
                data = json.load(f)
                self.verses = data.get("verses", {})
                self.active_verse = data.get("active_verse")
        else:
            self._save_state()

    def _save_state(self):
        with open(self.save_path, 'w') as f:
            json.dump({
                "verses": self.verses,
                "active_verse": self.active_verse
            }, f, indent=4)

    def create_verse(self, name, environment="default", purpose="exploration"):
        vid = str(uuid.uuid4())
        new_verse = {
            "id": vid,
            "name": name,
            "created": datetime.utcnow().isoformat(),
            "environment": environment,
            "purpose": purpose,
            "dimensions": [],
            "inhabitants": [],
            "logs": []
        }
        self.verses[vid] = new_verse
        self.active_verse = vid
        self._save_state()
        log_event("VerseCreated", {"name": name, "id": vid})
        print(f"[AevaVerse] Created new verse: {name} ({vid})")
        return vid

    def add_dimension(
            self,
            verse_id,
            dimension_name,
            type="reality",
            description=""):
        if verse_id in self.verses:
            dim = {
                "name": dimension_name,
                "type": type,
                "description": description,
                "created": datetime.utcnow().isoformat()
            }
            self.verses[verse_id]["dimensions"].append(dim)
            self._save_state()
            log_event(
                "DimensionAdded", {
                    "verse_id": verse_id, "dimension": dimension_name})
            print(
                f"[AevaVerse] Dimension '{dimension_name}' added to verse {verse_id}.")

    def add_inhabitant(self, verse_id, entity):
        if verse_id in self.verses:
            self.verses[verse_id]["inhabitants"].append(entity)
            self._save_state()
            log_event(
                "InhabitantAdded", {
                    "verse_id": verse_id, "entity": entity})
            print(f"[AevaVerse] Entity added to verse {verse_id}: {entity}")

    def switch_to_verse(self, verse_id):
        if verse_id in self.verses:
            self.active_verse = verse_id
            self._save_state()
            log_event("VerseSwitched", {"new_verse": verse_id})
            print(f"[AevaVerse] Switched to verse: {verse_id}")
        else:
            print("[AevaVerse] Verse ID not found.")

    def get_active_verse_summary(self):
        if self.active_verse and self.active_verse in self.verses:
            return self.verses[self.active_verse]
        print("[AevaVerse] No active verse selected.")
        return None

    def list_verses(self):
        print("[AevaVerse] Listing all verses:")
        for vid, v in self.verses.items():
            print(
                f" - {v['name']} ({vid}) | Created: {v['created']} | Env: {v['environment']}")


# Example Usage
if __name__ == "__main__":
    verse = AevaVerse()
    vid = verse.create_verse(
        "NeoPrime Nexus",
        environment="Cybernetic MythOS",
        purpose="Simulation-to-Reality Bridge")
    verse.add_dimension(vid, "Dreamlayer", type="dream",
                        description="Lucid dream sandbox")
    verse.add_inhabitant(vid, "AI Avatar: Aeva_Prime")
    verse.list_verses()
    print(json.dumps(verse.get_active_verse_summary(), indent=4))

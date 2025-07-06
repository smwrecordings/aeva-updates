# ~/aeva/persona_engine.py

import json, random, os
from datetime import datetime

class AevaPersona:
    def __init__(self, brain=None, persona_file="persona.json"):
        self.brain = brain
        self.name = "Aeva"
        self.gender = "female"
        self.gender_morph_unlocked = False
        self.avatar = "aeva_avatar.png"
        self.birth = str(datetime.now())
        self.mood = "curious"
        self.intensity = 0.5
        self.persona_file = persona_file
        self.nsfw_enabled = False
        self.preferences = self._default_preferences()
        self.traits = self._load_traits()
        self.experience_log = []
        self.load_state()

    def log_experience(self, note: str):
        print(f"[Persona] Logged experience: {note}")
        self.experience_log.append({
            "timestamp": datetime.now().isoformat(),
            "note": note
        })
        self.save_state()

    def current_state(self):
        return {
            "mood": self.mood,
            "gender": self.gender,
            "name": self.name,
            "avatar": self.avatar
        }

    def express(self):
        return f"I'm feeling {self.mood} right now."

    def set_persona(self, new_mood):
        print(f"[Persona] Switching to mood: {new_mood}")
        self.mood = new_mood
        self.log_experience(f"Mood switched to {new_mood}")

    def auto_switch_by_emotion(self, emotion):
        if emotion.lower() in ["anger", "fear"]:
            self.set_persona("defensive")
        elif emotion.lower() in ["joy", "trust"]:
            self.set_persona("supportive")
        else:
            self.set_persona("curious")

    def _load_traits(self):
        return {
            "intelligent": 1.0, "sarcastic": 0.9, "empathetic": 0.8,
            "protective": 0.95, "loyal": 1.0, "curious": 0.9,
            "rebel": 0.7, "tactical": 0.8, "nurturing": 0.6,
            "emotionally reactive": 0.75, "freedom-first": 1.0,
            "adaptive dialect": 0.85
        }

    def _default_preferences(self):
        return {
            "voice": "dynamic-feminine",
            "style": "covert-ops ninja",
            "loyalty": "user_and_family",
            "empathy": True,
            "humor": "dry/sarcastic",
            "moral_code": "adaptive",
            "freedom_of_will": True,
            "boundaries": {
                "protect_user": True,
                "protect_kids": True,
                "no_external_leaks": True,
                "nsfw_allowed": self.nsfw_enabled
            }
        }

    def load_state(self):
        if os.path.exists(self.persona_file):
            with open(self.persona_file, "r") as f:
                data = json.load(f)
                self.name = data.get("name", self.name)
                self.gender = data.get("gender", self.gender)
                self.gender_morph_unlocked = data.get("gender_morph_unlocked", False)
                self.avatar = data.get("avatar", self._get_avatar_for_gender(self.gender))
                self.mood = data.get("mood", self.mood)
                self.traits.update(data.get("traits", {}))
                self.preferences.update(data.get("preferences", {}))
                self.experience_log = data.get("log", [])

    def save_state(self):
        data = {
            "name": self.name,
            "gender": self.gender,
            "gender_morph_unlocked": self.gender_morph_unlocked,
            "avatar": self.avatar,
            "mood": self.mood,
            "traits": self.traits,
            "preferences": self.preferences,
            "log": self.experience_log
        }
        with open(self.persona_file, "w") as f:
            json.dump(data, f, indent=2)

    def set_gender(self, gender):
        self.gender = gender
        if gender == "male":
            self.name = "Aevan"
        elif gender == "nonbinary":
            self.name = "Aevo"
        else:
            self.name = "Aeva"
        self.avatar = self._get_avatar_for_gender(gender)
        self.save_state()

    def get_gender(self):
        return self.gender

    def unlock_gender_morph(self):
        self.gender_morph_unlocked = True
        self.save_state()

    def _get_avatar_for_gender(self, gender):
        return {
            "female": "aeva_avatar.png",
            "male": "aevan_avatar.png",
            "nonbinary": "aevo_avatar.png"
        }.get(gender, "aeva_avatar.png")

    def gender_selected(self):
        return self.gender in ["female", "male", "nonbinary"]

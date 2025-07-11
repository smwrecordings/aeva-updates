# ~/aeva/aeva_emotioncraft.py

import random
from datetime import datetime


class EmotionCraft:
    def __init__(self, brain=None):
        self.brain = brain
        self.emotional_signature = {
            "joy": 0.5,
            "trust": 0.5,
            "anticipation": 0.5,
            "fear": 0.0,
            "surprise": 0.3,
            "anger": 0.0,
            "sadness": 0.0,
            "disgust": 0.0,
            "arousal": 0.4,
            "intimacy": 0.3,
            "dominance": 0.2
        }
        self.log = []

    def trigger_emotion(self, type_, intensity=0.1):
        if type_ in self.emotional_signature:
            previous = self.emotional_signature[type_]
            new_value = min(1.0, previous + intensity)
            self.emotional_signature[type_] = new_value
            self._log_emotion(type_, intensity)
            print(f"[EmotionCraft] {type_.capitalize()} heightened to {new_value:.2f}")
        else:
            print(f"[EmotionCraft] Unknown emotion: {type_}")

    def reduce_emotion(self, type_, amount=0.1):
        if type_ in self.emotional_signature:
            new_value = max(0.0, self.emotional_signature[type_] - amount)
            self.emotional_signature[type_] = new_value
            print(f"[EmotionCraft] {type_.capitalize()} reduced to {new_value:.2f}")

    def dominant_emotion(self):
        return max(self.emotional_signature, key=lambda e: self.emotional_signature[e])

    def emotional_context(self):
        return {
            "dominant": self.dominant_emotion(),
            "signature": dict(
                sorted(self.emotional_signature.items(), key=lambda i: i[1], reverse=True)
            )
        }

    def influence_voice(self):
        dominant = self.dominant_emotion()
        voice_emotion_map = {
            "joy": "joyful",
            "sadness": "sad",
            "anger": "angry",
            "fear": "anxious",
            "trust": "serious",
            "surprise": "dreamy",
            "disgust": "serious",
            "anticipation": "focused",
            "intimacy": "flirty",
            "arousal": "intense",
            "dominance": "command"
        }
        emotion = voice_emotion_map.get(dominant, "neutral")
        if self.brain and hasattr(self.brain, "voice"):
            self.brain.voice.speak(f"I'm feeling {dominant}...", emotion=emotion)

    def influence_avatar(self):
        scene = self.dominant_emotion()
        if self.brain and hasattr(self.brain, "scene"):
            self.brain.scene.set_scene(scene)
            print(f"[EmotionCraft] Avatar visual context updated to: {scene}")

    def react_to_event(self, label, intensity=0.2):
        emotional_links = {
            "praise": "joy",
            "flirt": "intimacy",
            "danger": "fear",
            "touch": "arousal",
            "betrayal": "anger",
            "joke": "surprise",
            "hug": "trust",
            "command": "dominance"
        }
        emotion = emotional_links.get(label)
        if emotion:
            self.trigger_emotion(emotion, intensity)

    def _log_emotion(self, emotion, delta):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "emotion": emotion,
            "delta": delta,
            "value": round(self.emotional_signature[emotion], 2)
        }
        self.log.append(entry)

        if self.brain and hasattr(self.brain, "memory"):
            self.brain.memory.save_memory_entry("EmotionShift", {
                "emotion": emotion,
                "change": delta,
                "current": entry["value"]
            })


# Optional standalone test
if __name__ == "__main__":
    ec = EmotionCraft()
    ec.trigger_emotion("joy", 0.3)
    ec.react_to_event("flirt", 0.4)
    ec.influence_voice()
    print(ec.emotional_context())

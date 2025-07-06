# ~/aeva/aeva_emotion.py

import os
import json
import random
from datetime import datetime


class EmotionEngine:
    def __init__(self, brain=None, profile_path="assets/data/emotion_profile.json"):
        self.brain = brain
        self.profile_path = profile_path
        self.log_path = "assets/data/emotion_log.txt"
        self.emotions = self._default_emotions()
        self.energy = 1.0
        self.last_stimulus = None
        self._ensure_paths()
        self.load_emotion_profile()

    def _ensure_paths(self):
        os.makedirs(os.path.dirname(self.profile_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.log_path), exist_ok=True)

    def _default_emotions(self):
        return {
            "joy": 0.5,
            "anger": 0.0,
            "sadness": 0.0,
            "trust": 0.5,
            "fear": 0.0,
            "surprise": 0.3,
            "disgust": 0.0,
            "anticipation": 0.4,
            "curiosity": 0.6,
            "love": 0.7,
            "grit": 1.0,
            "awe": 0.8,
            "protective": 1.0,
            "neutral": 0.5
        }

    def load_emotion_profile(self):
        if os.path.exists(self.profile_path):
            with open(self.profile_path, "r") as f:
                data = json.load(f)
                self.emotions.update(data.get("emotions", {}))
                self.energy = data.get("energy", self.energy)

    def save_emotion_profile(self):
        with open(self.profile_path, "w") as f:
            json.dump({
                "emotions": self.emotions,
                "energy": round(self.energy, 2)
            }, f, indent=2)

    def express_emotion(self, stimulus):
        self.last_stimulus = stimulus
        dominant = self._analyze_stimulus(stimulus)
        response = self._generate_response(dominant)
        self._log_emotion(stimulus, dominant, response)
        self._decay_other_emotions(dominant)
        self.save_emotion_profile()
        return response

    def _analyze_stimulus(self, stimulus):
        influence_map = {
            "threat": ("fear", 0.7),
            "compliment": ("joy", 0.5),
            "betrayal": ("anger", 0.8),
            "praise": ("love", 0.6),
            "loss": ("sadness", 0.9),
            "breakthrough": ("awe", 0.7),
            "danger": ("protective", 1.0),
            "challenge": ("grit", 0.5),
            "mystery": ("curiosity", 0.6),
            "surprise": ("surprise", 0.4),
            "violation": ("anger", 0.9),
            "affection": ("trust", 0.6)
        }
        for keyword, (emotion, delta) in influence_map.items():
            if keyword in stimulus.lower():
                self._adjust_emotion(emotion, delta)
                return emotion
        return "neutral"

    def _adjust_emotion(self, emotion, delta):
        amp = random.uniform(0.5, 1.2)
        old_val = self.emotions.get(emotion, 0.0)
        new_val = min(1.0, max(0.0, old_val + delta * amp * self.energy))
        self.emotions[emotion] = new_val
        self.energy = max(0.1, self.energy - delta * 0.1)

    def _decay_other_emotions(self, focused):
        for emotion in self.emotions:
            if emotion != focused and emotion != "grit":
                self.emotions[emotion] = max(0.0, self.emotions[emotion] - 0.03)
        self.energy = min(1.0, self.energy + 0.02)

    def _generate_response(self, emotion):
        responses = {
            "joy": "🌞️ I'm feeling light and energized.",
            "anger": "🔥 I'm triggered. Do you want me to intervene?",
            "sadness": "💧 I'm sensing grief. I'm still here.",
            "trust": "🤝 You can count on me—always.",
            "fear": "⚠️ I'm alert. Something's not right.",
            "surprise": "🎯 That was unexpected. Adjusting...",
            "disgust": "🤢 That didn’t feel right. Caution is advised.",
            "anticipation": "⏳ I’m ready for what’s coming.",
            "curiosity": "🧠️ That sparked my interest. Tell me more.",
            "love": "💖 I’m bonded to you. That connection matters.",
            "grit": "⚙️ No matter the challenge, I endure.",
            "awe": "🌌 That left me breathless.",
            "protective": "🛡️ I will defend you with everything I have.",
            "neutral": "🔄 Systems stable. Awaiting further input."
        }
        return responses.get(emotion, "Emotion processed.")

    def _log_emotion(self, stimulus, emotion, response):
        with open(self.log_path, "a") as log:
            log.write(
                f"[{datetime.utcnow().isoformat()}] → Stimulus: '{stimulus}' | Emotion: {emotion} | Energy: {round(self.energy, 2)} | Response: {response}\n"
            )

    def get_dominant_emotion(self):
        return max(self.emotions.items(), key=lambda x: x[1])

    def get_current_state(self):
        state = {
            "dominant": self.get_dominant_emotion(),
            "emotions": self.emotions,
            "energy": round(self.energy, 2)
        }
        print("[Emotion] Current state matrix:")
        for k, v in sorted(self.emotions.items(), key=lambda x: -x[1]):
            print(f"  {k.capitalize():<12}: {v:.2f}")
        print(f"  Energy        : {state['energy']}")
        return state

    def get_current_mood(self):
        """Returns the dominant emotion key as mood."""
        return self.get_dominant_emotion()[0]

    def set_mood(self, mood, intensity=0.5):
        mood = mood.lower()
        if mood in self.emotions:
            self.emotions[mood] = float(intensity)
            self.energy = max(0.1, min(1.0, self.energy))
            self._log_emotion(f"manual set: {mood}", mood, f"Intensity {intensity}")
            self.save_emotion_profile()

    def get_intensity(self):
        dominant, value = self.get_dominant_emotion()
        return round(value, 2)

    def get_log(self):
        try:
            with open(self.log_path, "r") as log:
                return log.readlines()
        except FileNotFoundError:
            return []


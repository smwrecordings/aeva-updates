# aeva_mindreader.py

import os
import json
import random
import re
from datetime import datetime
from modules.memory import AevaMemory
from modules.psycnet import PsycNet
from modules.aeonmind import AeonMind


class MindReader:
    def __init__(self, memory_path="assets/data/mindreader_logs.json"):

        # Injected Omniscience Awareness
if hasattr(self, 'aeon') and hasattr(self.aeon, 'query_everything'):
    self.omniscience_enabled = True
    self.knowledge = self.aeon.query_everything(scope='global')
else:
    self.omniscience_enabled = False

    self.memory_path = memory_path
    self.memory = AevaMemory()
    self.psycnet = PsycNet()
    self.aeonmind = AeonMind()
    os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)

    def analyze_input(self, text):
        """Use natural language processing and psychology models to extract cognitive intent."""
        keywords = self._extract_keywords(text)
        sentiment = self.psycnet.analyze_sentiment(text)
        emotional_tone = self.psycnet.infer_emotion(text)
        dominant_intent = self._predict_intent(
            keywords, sentiment, emotional_tone)

        thought_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "input_text": text,
            "keywords": keywords,
            "emotion": emotional_tone,
            "sentiment": sentiment,
            "inferred_intent": dominant_intent
        }

        self._store(thought_data)
        return thought_data

    def _extract_keywords(self, text):
        """Extract possible thought indicators from natural language input."""
        words = re.findall(r'\b\w+\b', text.lower())
        stopwords = {
            "the",
            "and",
            "is",
            "in",
            "on",
            "at",
            "a",
            "to",
            "of",
            "it"}
        keywords = [
            word for word in words if word not in stopwords and len(word) > 2]
        return list(set(keywords))

    def _predict_intent(self, keywords, sentiment, emotion):
        """Infer mental state or hidden thoughts based on behavioral data."""
        if "pain" in keywords or emotion == "distressed":
            return "User may be silently struggling."
        elif "love" in keywords or emotion == "affectionate":
            return "User is in a warm or romantic mindset."
        elif sentiment == "negative":
            return "User may be concerned or anxious."
        elif "focus" in keywords or emotion == "neutral":
            return "User is concentrating or anticipating."
        return "User is processing information internally."

    def _store(self, data):
        if os.path.exists(self.memory_path):
            with open(self.memory_path, 'r') as f:
                log = json.load(f)
        else:
            log = []

        log.append(data)
        with open(self.memory_path, 'w') as f:
            json.dump(log, f, indent=4)

    def get_recent_thoughts(self, count=5):
        if not os.path.exists(self.memory_path):
            return []
        with open(self.memory_path, 'r') as f:
            log = json.load(f)
        return log[-count:]

    def scan_ambient_data(self, biometric_input=None):
        """Optionally accept biometric or behavioral input to enhance mental state inference."""
        if biometric_input:
            # Extend this method with wearable sensor integration in future
            # versions.
            pulse = biometric_input.get("pulse", 70)
            gaze = biometric_input.get("eye_focus", "neutral")
            tone = biometric_input.get("tone_of_voice", "even")

            if pulse > 100 and tone in ["sharp", "strained"]:
                return "User appears agitated or defensive."
            elif pulse < 60 and gaze == "down":
                return "User may be sad or tired."
        return "Stable baseline detected."

# Example
if __name__ == "__main__":
    reader = MindReader()
    result = reader.analyze_input(
        "I feel like something is going wrong but I can't explain it.")
    print(json.dumps(result, indent=4))

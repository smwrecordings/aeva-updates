# aeva_neuroscribe.py

import os
import json
import random
import hashlib
from datetime import datetime
from textblob import TextBlob


class NeuroScribe:
    def __init__(self, log_path="assets/data/neuroscribe_log.json"):
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)
        self.cache = []
        self._load()

    def _load(self):
        if os.path.exists(self.log_path):
            try:
                with open(self.log_path, 'r') as f:
                    self.cache = json.load(f)
            except BaseException:
                self.cache = []

    def _save(self):
        with open(self.log_path, 'w') as f:
            json.dump(self.cache, f, indent=4)

    def infer_thought(self, text, context=""):
        blob = TextBlob(text)
        mood = blob.sentiment.polarity
        thought_hash = hashlib.sha256(
            f"{text}{datetime.utcnow()}".encode()).hexdigest()

        state = {
            "timestamp": datetime.utcnow().isoformat(),
            "input": text,
            "context": context,
            "mood": "positive" if mood > 0 else "negative" if mood < 0 else "neutral",
            "keywords": [
                word.lower() for word in blob.noun_phrases],
            "intent": self._guess_intent(text),
            "id": thought_hash}

        self.cache.append(state)
        self._save()
        print(
            f"[NeuroScribe] Inferred intent: {
                state['intent']} | Mood: {
                state['mood']}")
        return state

    def _guess_intent(self, text):
        lowered = text.lower()
        if any(w in lowered for w in ["want", "need", "wish", "crave"]):
            return "desire"
        elif any(w in lowered for w in ["hate", "mad", "angry", "annoyed"]):
            return "hostility"
        elif any(w in lowered for w in ["curious", "wonder", "how", "what"]):
            return "curiosity"
        elif any(w in lowered for w in ["happy", "love", "great", "awesome"]):
            return "positive engagement"
        elif any(w in lowered for w in ["help", "assist", "guide"]):
            return "support request"
        else:
            return "unknown or layered"

    def retrieve_last(self, count=5):
        print(f"[NeuroScribe] Retrieving last {count} thought impressions...")
        return self.cache[-count:]


# Example usage
if __name__ == "__main__":
    ns = NeuroScribe()
    ns.infer_thought("I wish I could figure out how this works.")
    ns.infer_thought("Why is the system lagging today?")
    ns.retrieve_last()

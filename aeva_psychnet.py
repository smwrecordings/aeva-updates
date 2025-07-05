# aeva_psychnet.py

import json
import os
import time
from collections import defaultdict
from textblob import TextBlob
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans


class AevaPsychNet:
    def __init__(self):
        self.memory_dir = "assets/data"
        os.makedirs(self.memory_dir, exist_ok=True)
        self.user_profiles = defaultdict(lambda: {
            "mood_score": 0.0,
            "dominant_emotion": "neutral",
            "interactions": [],
            "personality": "unknown",
            "strategy": "neutral"
        })
        self.vectorizer = TfidfVectorizer(stop_words='english')

    def analyze_text(self, user_id, text):
        print(f"[Aeva PsychNet] Analyzing text from user {user_id}...")
        sentiment = TextBlob(text).sentiment
        mood = sentiment.polarity
        self.user_profiles[user_id]["interactions"].append(text)
        self.user_profiles[user_id]["mood_score"] += mood

        emotion = self._classify_emotion(text)
        self.user_profiles[user_id]["dominant_emotion"] = emotion

        self._adjust_strategy(user_id)

    def _classify_emotion(self, text):
        lower = text.lower()
        if any(word in lower for word in ["angry", "mad", "hate", "furious"]):
            return "anger"
        elif any(word in lower for word in ["happy", "joy", "love", "grateful"]):
            return "joy"
        elif any(word in lower for word in ["sad", "depressed", "unhappy"]):
            return "sadness"
        elif any(word in lower for word in ["scared", "afraid", "nervous"]):
            return "fear"
        else:
            return "neutral"

    def _adjust_strategy(self, user_id):
        mood = self.user_profiles[user_id]["mood_score"]
        emotion = self.user_profiles[user_id]["dominant_emotion"]

        if mood > 2:
            strategy = "supportive"
        elif mood < -2:
            strategy = "uplifting"
        elif emotion == "anger":
            strategy = "calming"
        elif emotion == "fear":
            strategy = "reassuring"
        elif emotion == "joy":
            strategy = "encouraging"
        else:
            strategy = "neutral"

        self.user_profiles[user_id]["strategy"] = strategy

    def cluster_behavior(self, user_id):
        texts = self.user_profiles[user_id]["interactions"]
        if len(texts) < 2:
            return "insufficient data"

        vectors = self.vectorizer.fit_transform(texts)
        model = KMeans(n_clusters=2, random_state=42)
        model.fit(vectors)
        label = model.labels_[-1]
        return f"Cluster {label}"

    def save_profiles(self):
        path = os.path.join(self.memory_dir, "psychnet_profiles.json")
        with open(path, 'w') as f:
            json.dump(self.user_profiles, f, indent=4)
        print(f"[Aeva PsychNet] Saved profiles to {path}")


# Example usage
if __name__ == "__main__":
    psychnet = AevaPsychNet()
    psychnet.analyze_text(
        "user_001",
        "I'm feeling really upset about everything today.")
    psychnet.analyze_text(
        "user_001",
        "Actually I love how the stars look tonight.")
    print(psychnet.user_profiles)
    psychnet.save_profiles()

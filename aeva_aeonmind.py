# ~/aeva/aeva_aeonmind.py

import os
import json
import random
from datetime import datetime, timedelta


class AeonMind:
    def __init__(self, brain=None):
        self.brain = brain
        self.memory_path = "assets/data/aeonmind_memory.json"
        self.timeline_path = "assets/data/aeonmind_timeline.json"
        os.makedirs(os.path.dirname(self.memory_path), exist_ok=True)

        # Injected Omniscience Awareness
        if hasattr(self, 'aeon') and hasattr(self.aeon, 'query_everything'):
            self.omniscience_enabled = True
            self.knowledge = self.aeon.query_everything(scope='global')
        else:
            self.omniscience_enabled = False
            self.knowledge = None

        self.core_insights = []
        self.temporal_index = []
        self._load_memory()
        print("[AeonMind] Neural continuum activated.")

    def _load_memory(self):
        try:
            if os.path.exists(self.memory_path):
                with open(self.memory_path, 'r') as f:
                    self.core_insights = json.load(f)
            if os.path.exists(self.timeline_path):
                with open(self.timeline_path, 'r') as f:
                    self.temporal_index = json.load(f)
        except Exception as e:
            print(f"[AeonMind] ⚠️ Failed to load memory: {e}")

    def _save_memory(self):
        try:
            with open(self.memory_path, 'w') as f:
                json.dump(self.core_insights, f, indent=2)
            with open(self.timeline_path, 'w') as f:
                json.dump(self.temporal_index, f, indent=2)
        except Exception as e:
            print(f"[AeonMind] ⚠️ Failed to save memory: {e}")

    def absorb_experience(self, event, impact_level=1.0):
        timestamp = datetime.utcnow().isoformat()
        mood = self.brain.emotions.get_current_mood() if self.brain else "unknown"
        emotion_intensity = self.brain.emotions.get_intensity() if self.brain else 0.5
        insight = {
            "timestamp": timestamp,
            "event": event,
            "impact": impact_level,
            "mood": mood,
            "emotion_intensity": emotion_intensity,
            "persona": self.brain.persona.mood if self.brain else "unknown",
            "source": self.brain.__class__.__name__ if self.brain else "Standalone"}
        self.core_insights.append(insight)
        self.temporal_index.append({"t": timestamp, "tag": event})
        print(
            f"[AeonMind] Insight absorbed → {event} | Impact: {impact_level}")
        self._save_memory()

    def project_forward(self):
        if not self.core_insights:
            return {
                "simulation": "[AeonMind] No insights available to simulate."}

        recent = self.core_insights[-7:]
        intensity_avg = sum(i.get("emotion_intensity", 0.5)
                            for i in recent) / len(recent)
        themes = [i['event'].split()[0] for i in recent if 'event' in i]
        dominant_theme = max(set(themes),
                             key=themes.count) if themes else "unknown"

        prediction = f"Current trajectory favors emotional intensity at {
            intensity_avg:.2f}. Theme convergence: {dominant_theme}. Recommend: Adaptive recalibration."

        return {
            "simulation": prediction,
            "reference": recent
        }

    def recall_memory(self, keyword):
        results = [i for i in self.core_insights if keyword.lower()
                   in i["event"].lower()]
        print(
            f"[AeonMind] Memory retrieval → {
                len(results)} entries matched '{keyword}'.")
        return results

    def log_timemark(self, note):
        timestamp = datetime.utcnow().isoformat()
        mark = {
            "timestamp": timestamp,
            "note": note,
            "persona": self.brain.persona.mood if self.brain else "neutral"
        }
        self.temporal_index.append(mark)
        print(f"[AeonMind] ⏱️ Timemark: {note}")
        self._save_memory()

    def get_summary(self):
        total = len(self.core_insights)
        dominant_mood = self.brain.emotions.get_dominant_emotion()[
            0] if self.brain else "unknown"
        last_event = self.core_insights[-1] if total else None
        print(
            f"[AeonMind] Snapshot: {total} insights stored | Mood: {dominant_mood}")
        return {
            "total_insights": total,
            "dominant_mood": dominant_mood,
            "last_event": last_event
        }

    def purge_memory(self, retain_last_n=10):
        if len(self.core_insights) > retain_last_n:
            print(
                f"[AeonMind] Purging memory... Retaining last {retain_last_n} insights.")
            self.core_insights = self.core_insights[-retain_last_n:]
            self.temporal_index = self.temporal_index[-retain_last_n:]
            self._save_memory()

    def trace_origin(self):
        if not self.temporal_index:
            return "[AeonMind] No temporal anchors found."
        first = self.temporal_index[0]
        print(
            f"[AeonMind] Origin event → {
                first['t']} | Note: {
                first.get(
                    'tag',
                    'n/a')}")
        return first

if __name__ == "__main__":
    aeon = AeonMind()
    aeon.absorb_experience("Test: Encountered anomaly at perimeter gate")
    aeon.log_timemark("System calibrated")
    print(aeon.get_summary())

# aeva_mediacaster.py

import os
import json
import time
from datetime import datetime
import subprocess


class MediaCaster:
    def __init__(self, log_path="assets/data/mediacast_log.json"):
        self.log_path = log_path
        self.log = []
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def log_event(self, event, meta=None):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event,
            "meta": meta or {}
        }
        self.log.append(entry)
        with open(self.log_path, 'w') as f:
            json.dump(self.log, f, indent=4)
        print(f"[MediaCaster] {event} logged.")

    def launch_obs(self):
        """Launch OBS Studio if available (e.g., on PC environment)."""
        try:
            subprocess.Popen(["obs"])
            self.log_event("OBS_Launched")
        except Exception as e:
            self.log_event("OBS_Launch_Failed", {"error": str(e)})

    def start_stream(self, platform="YouTube", key=""):
        """Simulated trigger to start a stream."""
        self.log_event("Stream_Started", {"platform": platform, "key": key})
        print(f"[MediaCaster] Streaming to {platform}...")

    def stop_stream(self):
        self.log_event("Stream_Stopped")
        print("[MediaCaster] Stream stopped.")

    def play_intro_music(self, track="intro_theme.mp3"):
        self.log_event("Play_Intro", {"track": track})
        print(f"[MediaCaster] Playing intro track: {track}")
        # You can use something like ffplay or a TTS audio cue

    def voice_announce(self, message):
        """Aeva narrates or delivers news/audio instructions."""
        self.log_event("Voice_Announce", {"message": message})
        print(f"[MediaCaster] Announce: {message}")
        subprocess.run(["espeak", message])

    def scene_switch(self, scene_name):
        self.log_event("Scene_Switch", {"scene": scene_name})
        print(f"[MediaCaster] Switching to scene: {scene_name}")

    def schedule_broadcast(self, when, topic):
        self.log_event("Scheduled", {"time": when, "topic": topic})
        print(f"[MediaCaster] Broadcast scheduled for {when}: {topic}")


# Test run
if __name__ == "__main__":
    mc = MediaCaster()
    mc.start_stream("Twitch", "abc123")
    mc.play_intro_music("epic_intro.mp3")
    mc.voice_announce("Welcome to the Aeva broadcast.")
    mc.scene_switch("MainStage")
    mc.stop_stream()

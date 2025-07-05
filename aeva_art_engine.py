# ~/aeva/aeva_art_engine.py

import os
import json
import random
from datetime import datetime


class AevaArtEngine:
    def __init__(self, brain=None):
        self.brain = brain
        self.mode = "hybrid"
        self.output_dir = "assets/artwork"
        os.makedirs(self.output_dir, exist_ok=True)
        self.online = self._check_internet()
        # Placeholder for future API integration
        self.remote_api = "https://your-remote-ai-server.com/generate"

    def _check_internet(self):
        try:
            import requests
            requests.get("https://google.com", timeout=3)
            return True
        except BaseException:
            return False

    def generate_art(self, prompt, style=None):
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        filename = f"{self.output_dir}/aeva_art_{timestamp}.json"

        if self.online:
            print(f"[AevaArtEngine] (ONLINE) Delegating prompt: '{prompt}'")
            content = self._simulate_remote_call(prompt, style)
        else:
            print(
                f"[AevaArtEngine] (OFFLINE) Simulating artwork for prompt: '{prompt}'")
            content = self._simulate_local(prompt, style)

        with open(filename, "w") as f:
            json.dump(content, f, indent=2)

        print(f"[AevaArtEngine] Art entry saved: {filename}")
        return filename

    def _simulate_remote_call(self, prompt, style):
        return {
            "status": "queued",
            "timestamp": datetime.utcnow().isoformat(),
            "prompt": prompt,
            "style": style,
            "url": "https://art.ai/placeholder/generated.png",
            "note": "Remote generation simulated."
        }

    def _simulate_local(self, prompt, style):
        return {
            "status": "simulated",
            "timestamp": datetime.utcnow().isoformat(),
            "prompt": prompt,
            "style": style,
            "output": f"Simulated image: {prompt} [{style}]"
        }

    def describe_capabilities(self):
        return "Online" if self.online else "Offline simulation only"

    def list_styles(self):
        return [
            "cyberpunk", "anime", "celestial bloom", "surrealism",
            "pixel art", "noir", "aetherpunk", "dreamcore",
            "oil painting", "sci-fi construct", "digital dreamscape"
        ]

    def generate_random_art(self):
        prompt = random.choice([
            "a neon goddess surrounded by satellites",
            "a mythic dream of digital rebirth",
            "the child of time surfing the void",
            "an AI guardian protecting light",
            "an ancient machine dreaming of stars"
        ])
        style = random.choice(self.list_styles())
        return self.generate_art(prompt, style)


if __name__ == "__main__":
    engine = AevaArtEngine()
    print(engine.describe_capabilities())
    engine.generate_random_art()

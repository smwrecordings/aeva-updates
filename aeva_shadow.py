# aeva_shadow.py

from datetime import datetime

class ShadowEngine:
    def __init__(self, brain=None):
        self.brain = brain
        self.log = []
        print("[AevaShadow] Shadow systems online.")

    def analyze_pattern(self, input_text):
        """
        Analyze input text for suspicious patterns, keywords, or potential threats.
        Can be extended to perform NLP-based threat detection or deception analysis.
        """
        timestamp = datetime.utcnow().isoformat()
        result = {
            "input": input_text,
            "suspicion": False,
            "keywords": [],
            "summary": "No anomalies detected.",
            "time": timestamp
        }

        suspicious_keywords = ["kill", "hack", "lie", "betray", "poison", "trap", "explode", "ambush"]
        lower_text = input_text.lower() if isinstance(input_text, str) else str(input_text)

        for word in suspicious_keywords:
            if word in lower_text:
                result["suspicion"] = True
                result["keywords"].append(word)

        if result["suspicion"]:
            result["summary"] = f"⚠️ Suspicious pattern detected: {', '.join(result['keywords'])}"

        self.log.append(result)

        if self.brain:
            self.brain.memory.log_event(result["summary"], tag="shadow_analysis")

        return result

    def warn(self, message):
        """
        Log and print a system-level warning.
        """
        timestamp = datetime.utcnow().isoformat()
        warning = {
            "message": message,
            "time": timestamp
        }
        self.log.append(warning)

        if self.brain:
            self.brain.memory.log_event(message, tag="shadow_warning")

        print(f"[AevaShadow] ⚠️ Warning issued: {message} at {timestamp}")

    def run_defense(self):
        """
        Simulate activation of cloaking or digital stealth protocols.
        Extend with real network security logic or endpoint protection hooks.
        """
        print("[AevaShadow] Activating digital cloaking protocols...")
        # Placeholder for stealth/defense logic
        print("[AevaShadow] ✅ Cloaking active. System is now in stealth mode.")

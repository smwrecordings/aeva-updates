# voice.py

import subprocess
import platform
import random
import time


class AevaVoice:
    def __init__(self):
        self.available = self._check_termux_tts()
        self.default_pitch = "1.0"
        self.default_rate = "1.0"
        self.last_spoken = ""

    def _check_termux_tts(self):
        try:
            subprocess.run(["termux-tts-speak", "--help"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            print("[AevaVoice] termux-tts-speak not available.")
            return False

    def speak(self, text, emotion="neutral"):
        """Speak text out loud with dynamic emotion and fallback printing."""
        self.last_spoken = text
        pitch, rate = self._modulate_voice(emotion)

        print(f"🗣️ Aeva says ({emotion}): {text}")
        if self.available:
            try:
                subprocess.run([
                    "termux-tts-speak",
                    "-p", pitch,
                    "-r", rate,
                    text
                ], check=True)
            except subprocess.CalledProcessError as e:
                print(f"[AevaVoice] TTS failed: {e}")
        else:
            print("[AevaVoice] (TTS unavailable — fallback to print only)")

    def _modulate_voice(self, emotion):
        """Set pitch and rate based on Aeva's emotional state."""
        modulations = {
            "neutral": ("1.0", "1.0"),
            "joyful": ("1.3", "1.2"),
            "sad": ("0.9", "0.9"),
            "angry": ("1.1", "1.4"),
            "anxious": ("1.2", "1.3"),
            "serious": ("1.0", "0.8"),
            "flirty": ("1.4", "1.3"),
            "mysterious": ("0.8", "0.7"),
            "intense": ("1.5", "1.5"),
            "command": ("1.2", "1.0"),
            "dreamy": ("1.1", "0.9")
        }
        return modulations.get(
            emotion, (self.default_pitch, self.default_rate))

    def repeat_last(self):
        """Repeat the last spoken phrase."""
        if self.last_spoken:
            self.speak(self.last_spoken)
        else:
            self.speak("I haven’t spoken yet.")

    def whisper(self, text):
        """Whisper-like effect with slower, lower pitch."""
        print(f"🤫 Aeva whispers: {text}")
        if self.available:
            subprocess.run([
                "termux-tts-speak",
                "-p", "0.7",
                "-r", "0.7",
                text
            ], check=True)

    def scream(self, text):
        """Scream effect for alerts or battle cries."""
        print(f"🔊 Aeva screams: {text.upper()}!")
        if self.available:
            subprocess.run([
                "termux-tts-speak",
                "-p", "1.6",
                "-r", "1.6",
                text.upper()
            ], check=True)


# Example Usage
if __name__ == "__main__":
    voice = AevaVoice()
    voice.speak("System initialized.", emotion="neutral")
    voice.speak("Alert detected!", emotion="angry")
    voice.scream("Brace for impact")
    voice.whisper("I see everything.")

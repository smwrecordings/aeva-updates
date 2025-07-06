import subprocess
import platform
import random
import time
import os
import json
from datetime import datetime
import speech_recognition as sr


class VoiceInterface:
    def __init__(self, brain=None):
        self.brain = brain
        self.available = self._check_termux_tts()
        self.default_pitch = "1.0"
        self.default_rate = "1.0"
        self.last_spoken = ""
        self.log = []
        self.allow_slang = True
        self.allow_cussing = True

    def _check_termux_tts(self):
        try:
            subprocess.run(["termux-tts-speak", "--help"],
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return True
        except FileNotFoundError:
            print("[AevaVoice] termux-tts-speak not available.")
            return False

    def speak(self, text, emotion=None, tone=None):
        emotion = emotion or tone or "neutral"
        timestamp = datetime.utcnow().isoformat()
        processed_text = self._process_text(text)
        self.last_spoken = processed_text

        pitch, rate = self._modulate_voice(emotion)
        gender_pitch_offset = self._gender_pitch_offset()
        final_pitch = str(round(float(pitch) + gender_pitch_offset, 2))
        final_rate = rate

        print(f"὞3️ Aeva says ({emotion}, {self._get_gender()}): {processed_text}")
        self.log.append({
            "timestamp": timestamp,
            "emotion": emotion,
            "gender": self._get_gender(),
            "text": processed_text
        })

        if self.available:
            try:
                subprocess.run([
                    "termux-tts-speak",
                    "-p", final_pitch,
                    "-r", final_rate,
                    processed_text
                ], check=True)
            except subprocess.CalledProcessError as e:
                print(f"[AevaVoice] TTS failed: {e}")
        else:
            print("[AevaVoice] (TTS unavailable — fallback to print only)")

    def _modulate_voice(self, emotion):
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
            "dreamy": ("1.1", "0.9"),
            "concerned": ("0.9", "0.9"),
            "curious": ("1.2", "1.1"),
            "whisper": ("0.8", "0.7")
        }
        return modulations.get(emotion.lower(), (self.default_pitch, self.default_rate))

    def _gender_pitch_offset(self):
        gender = self._get_gender()
        if gender == "male":
            return -0.2
        elif gender == "nonbinary":
            return 0.0
        return 0.2

    def _get_gender(self):
        if self.brain and hasattr(self.brain, "persona"):
            return self.brain.persona.get_gender()
        return "female"

    def _process_text(self, text):
        if self.allow_slang:
            slang_replacements = {
                "hello": random.choice(["yo", "sup", "hey there", "what's good"]),
                "goodbye": random.choice(["peace", "later", "deuces", "catch ya"]),
                "amazing": random.choice(["fire", "lit", "next level", "crazy good"])
            }
            for word, slang in slang_replacements.items():
                text = text.replace(word, slang)
        if not self.allow_cussing:
            censor = {"damn": "darn", "shit": "shoot", "fuck": "fudge"}
            for word, sub in censor.items():
                text = text.replace(word, sub)
        return text

    def repeat_last(self):
        if self.last_spoken:
            self.speak(self.last_spoken)
        else:
            self.speak("I haven’t spoken yet.")

    def whisper(self, text):
        self.speak(text, emotion="whisper")

    def scream(self, text):
        processed = self._process_text(text.upper())
        print(f"🔊 Aeva screams: {processed}!")
        if self.available:
            subprocess.run([
                "termux-tts-speak",
                "-p", "1.6",
                "-r", "1.6",
                processed
            ], check=True)

    def get_voice_log(self):
        return self.log

    def last_message(self):
        return self.log[-1] if self.log else None

    def save_voice_log(self, path="assets/data/voice_log.json"):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(self.log, f, indent=2)
        print(f"[AevaVoice] Voice log saved to {path}")

    def listen_for_command(self, timeout=5, phrase_time_limit=10):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("🎤 [AevaVoice] Listening for your command...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                command = recognizer.recognize_google(audio)
                print(f"[AevaVoice] Heard: {command}")
                return command.strip()
        except sr.WaitTimeoutError:
            print("⏱️ [AevaVoice] Listening timed out.")
            return ""
        except sr.UnknownValueError:
            print("🤷 [AevaVoice] Sorry, I didn’t catch that.")
            return ""
        except sr.RequestError as e:
            print(f"❌ [AevaVoice] API error: {e}")
            return ""
        except Exception as e:
            print(f"⚠️ [AevaVoice] Mic issue: {e}")
            return input("🎤 Type your command instead: ").strip()


if __name__ == "__main__":
    voice = VoiceInterface()
    voice.speak("System initialized.", emotion="neutral")
    voice.speak("This system is amazing!", emotion="joyful")
    voice.scream("Brace for impact")
    voice.whisper("I see everything.")

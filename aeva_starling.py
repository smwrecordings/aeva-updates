# aeva_starling.py

import os
import json
import datetime
from googletrans import Translator
from langdetect import detect
from gtts import gTTS
import speech_recognition as sr


class AevaStarling:
    def __init__(self, log_path="assets/data/starling_logs.json"):
        self.translator = Translator()
        self.logs = []
        self.log_path = log_path
        os.makedirs(os.path.dirname(log_path), exist_ok=True)

    def detect_language(self, text):
        try:
            lang = detect(text)
            self._log("LanguageDetected", {"input": text, "language": lang})
            return lang
        except Exception as e:
            self._log("DetectionError", {"input": text, "error": str(e)})
            return None

    def translate(self, text, target='en'):
        try:
            translated = self.translator.translate(text, dest=target)
            self._log(
                "Translation", {
                    "input": text, "translated": translated.text, "to": target})
            return translated.text
        except Exception as e:
            self._log("TranslationError", {"input": text, "error": str(e)})
            return None

    def speak(self, text, lang='en', filename="starling_output.mp3"):
        try:
            tts = gTTS(text=text, lang=lang)
            filepath = os.path.join("assets/data", filename)
            tts.save(filepath)
            self._log(
                "SpeechGenerated", {
                    "text": text, "lang": lang, "file": filepath})
            print(f"[Starling] Speech generated at {filepath}")
            return filepath
        except Exception as e:
            self._log("SpeechError", {"text": text, "error": str(e)})
            return None

    def listen(self, timeout=5):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("[Starling] Listening...")
            try:
                audio = recognizer.listen(source, timeout=timeout)
                text = recognizer.recognize_google(audio)
                self._log("SpeechRecognized", {"output": text})
                print(f"[Starling] Recognized: {text}")
                return text
            except Exception as e:
                self._log("RecognitionError", {"error": str(e)})
                print(f"[Starling] Error: {e}")
                return None

    def _log(self, label, metadata):
        entry = {
            "timestamp": datetime.datetime.utcnow().isoformat(),
            "label": label,
            "metadata": metadata
        }
        self.logs.append(entry)
        with open(self.log_path, "w") as f:
            json.dump(self.logs, f, indent=4)


# Example usage
if __name__ == "__main__":
    starling = AevaStarling()
    sample = "Bonjour le monde"
    detected = starling.detect_language(sample)
    translated = starling.translate(sample, target='en')
    starling.speak(translated, lang='en')

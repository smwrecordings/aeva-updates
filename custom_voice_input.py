# custom_voice_input.py

import speech_recognition as sr

recognizer = sr.Recognizer()


def listen_via_mic():
    with sr.Microphone() as source:
        print("🎤 Listening (custom)...")
        audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)

    try:
        text = recognizer.recognize_google(audio)
        print(f"🧠 Recognized: {text}")
        return text.lower(), "neutral"
    except sr.UnknownValueError:
        print("❌ Could not understand audio.")
        return "", "confused"
    except sr.RequestError as e:
        print(f"⚠️ Recognition error: {e}")
        return "", "error"

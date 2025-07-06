# voice_input.py

import speech_recognition as sr

def listen_with_mic(timeout=5, phrase_time_limit=10):
    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("🎤 Mic active. Listening...")
            recognizer.adjust_for_ambient_noise(source, duration=0.3)

            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            try:
                text = recognizer.recognize_google(audio)
                print(f"🗣️ You said: {text}")
                return text.strip(), "neutral"

            except sr.UnknownValueError:
                print("🤷 I couldn’t understand the audio.")
                return "", "neutral"

            except sr.RequestError as e:
                print(f"❌ Google API error: {e}")
                return "", "neutral"

    except sr.WaitTimeoutError:
        print("⏱️ Timeout: No speech detected.")
        return "", "neutral"

    except Exception as mic_error:
        print(f"⚠️ Mic unavailable or other error: {mic_error}")
        fallback = input("⌨️ Mic failed. Type your input instead: ").strip()
        return fallback, "neutral"

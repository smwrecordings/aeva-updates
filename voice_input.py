# voice_input.py

import speech_recognition as sr


def listen_with_mic(timeout=5, phrase_time_limit=10):
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print("🎤 Mic active. Listening...")
        recognizer.adjust_for_ambient_noise(source)

        try:
            audio = recognizer.listen(
                source,
                timeout=timeout,
                phrase_time_limit=phrase_time_limit)
            text = recognizer.recognize_google(audio)
            return text.strip(), "neutral"

        except sr.WaitTimeoutError:
            print("⏱️ Timeout: No speech detected.")
            return "", "neutral"

        except sr.UnknownValueError:
            print("🤷 Could not understand audio.")
            return "", "neutral"

        except sr.RequestError as e:
            print(f"❌ Request error from Google Speech API: {e}")
            return "", "neutral"

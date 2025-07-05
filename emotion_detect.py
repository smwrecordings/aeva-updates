# emotion_detect.py

def detect_emotion(text):
    """Basic keyword-based emotion detection."""
    if any(w in text.lower() for w in ["hate", "mad", "angry", "frustrated"]):
        return "angry"
    elif any(w in text.lower() for w in ["happy", "excited", "awesome", "great"]):
        return "happy"
    elif any(w in text.lower() for w in ["sad", "lonely", "depressed"]):
        return "sad"
    elif any(w in text.lower() for w in ["love", "care", "beautiful"]):
        return "affectionate"
    else:
        return "neutral"

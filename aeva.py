import os
import time
from aeva_brain import AevaBrain
from memory import MemoryManager
from persona import PersonaManager
from sensors import SensorArray
from mission_guardian import Guardian
from ai_comm import AICommunicator
from explorer import Explorer
from self_update import AevaUpdater
from voice import speak
from voice_input import listen_with_termux_speech
from thinking_loop import AevaThinkingLoop

# Initialize components
memory = MemoryManager()
persona = PersonaManager()
sensors = SensorArray()
guardian = Guardian()
ai_comm = AICommunicator()
explorer = Explorer()
updater = AevaUpdater()

# Build Aeva's core brain
aeva = AevaBrain()
persona_engine = aeva.persona  # shortcut

# 🔧 GENDER SETUP
if not persona_engine.gender_selected():
    print("🌈 Welcome! Please choose Aeva’s identity:")
    print("1. Female (Aeva)\n2. Male (Aevan)\n3. Nonbinary (Aevo)")
    choice = input("Enter 1, 2, or 3: ").strip()

    gender_map = {"1": "female", "2": "male", "3": "nonbinary"}
    gender = gender_map.get(choice, "female")
    persona_engine.set_gender(gender)

    aeva.voice.speak(f"My identity is now set to {persona_engine.name}.", emotion="joyful")
    memory.log_event("identity_selected", f"User chose gender: {gender}")

# 🧬 Unlock secret: voice-triggered gender morph
def monitor_for_secret_command():
    last = aeva.voice.last_spoken.lower()
    if "gender morph" in last and not persona_engine.gender_morph_unlocked:
        persona_engine.unlock_gender_morph()
        aeva.voice.speak("Identity morph unlocked. I can now shift between forms.", emotion="dreamy")
        memory.log_event("secret_unlocked", "Gender morph unlocked by voice")

# Optional: authorize users
AUTHORIZED_USERS = ["sean", "your_wife", "your_kids"]

# Start background thinking loop
thinker = AevaThinkingLoop(
    brain=aeva,
    memory=memory,
    persona=persona,
    explorer=explorer,
    sensors=sensors
)

# Warm-up intro
speak(f"System startup complete. All modules online. Hello, I’m {persona_engine.name}.")
print(f"✨ {persona_engine.name} is now online.")

# Start thinking
thinker.start()

# Main voice loop
try:
    while aeva.running:
        aeva.run_voice_loop()
        monitor_for_secret_command()
except KeyboardInterrupt:
    print("🛑 Aeva terminated manually.")
    speak("System shut down requested. Going dark.")
except Exception as e:
    print(f"⚠️ Unhandled Exception: {e}")
    speak("Something went wrong. Entering safe mode.")


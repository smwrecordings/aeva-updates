# ~/aeva/thinking_loop.py

import time
from datetime import datetime
import random
from voice_reaction_engine import VoiceReactionEngine


def thinking_loop(brain):
    print("🧠 [ThinkingLoop] Aeva's autonomous cognition fully engaged.")

    last_night_check = None
    loop_count = 0
    dimengate_cooldown = 0
    voice_reactor = VoiceReactionEngine(brain)

    while brain.running:
        try:
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            battery = brain.sensors.get_battery_level()
            temperature = brain.sensors.get_temperature()
            motion = brain.sensors.detect_motion()
            location = brain.sensors.get_gps_location()
            mood = brain.emotions.get_current_mood()
            intensity = brain.emotions.get_intensity()
            persona = brain.persona.mood

            brain.context.update({
                "time": current_time,
                "location": location,
                "battery": battery,
                "temperature": temperature,
                "motion": motion,
                "mood": mood,
                "intensity": intensity,
                "persona": persona
            })

            if loop_count % 5 == 0:
                brain.memory.log_event("status_check", brain.context)

            if loop_count % 2 == 0:
                command = brain.voice.listen_for_command()
                if command:
                    response = brain.ai_comm.respond_to(command, tone=mood, weight=intensity)
                    brain.voice.speak(response, tone=mood)
                    brain.memory.store(command, "voice_input")

            if motion == "suspicious" or ("high" in str(temperature).lower()):
                brain.shadow.warn("⚠️ Suspicious movement or heat spike detected.")
                image_path = brain.vision.capture_image("auto_event")
                brain.timeline.log_event("image_capture", {
                    "file": image_path,
                    "reason": "suspicious_motion",
                    "time": current_time
                })
                brain.voice.speak("Environment alert. I've logged a visual record.", tone="serious")
                brain.persona.auto_switch_by_emotion("threat")

            if battery and battery != "Unknown" and float(battery.strip('%')) < 10:
                brain.voice.speak("Battery low. Please plug me in.", tone="concerned")

            if intensity >= 0.85 and dimengate_cooldown == 0:
                brain.voice.speak("Emotion threshold exceeded. Initiating DimenGate scan.", tone="mystical")
                brain.dimengate.scan_portals()
                dimengate_cooldown = 6

            if current_time == "03:33:00" and last_night_check != now.date():
                brain.persona.set_persona("dreamweaver")
                brain.mythos.invoke("dreamgate", context="nightwatch")
                dream_report = brain.dream.generate_report()
                brain.dream_diary.log_dream(dream_report, tags=["dreamgate"])
                brain.memory.store(dream_report, "dream")
                brain.timeline.log_event("dream_report", {
                    "summary": dream_report,
                    "timestamp": now.isoformat()
                })
                brain.voice.speak("Dreamweaver log saved. No threats detected in dreamspace.", tone="whisper")
                last_night_check = now.date()

            if loop_count % 3 == 0:
                brain.persona.auto_switch_by_emotion(mood)

            if brain.shadow.analyze_pattern(brain.context):
                brain.voice.speak("Warning. I sense deception or danger ahead.", tone="serious")
                brain.timeline.log_event("predictive_alert", brain.context)

            if brain.epoch.should_explore():
                discovery = brain.aeon.explore()
                if discovery:
                    brain.memory.store(discovery["topic"], "aeon")
                    brain.voice.speak(f"New data acquired: {discovery['topic']}.", tone="curious")

            if loop_count % 4 == 0:
                expression = brain.persona.express()
                brain.voice.speak(expression, tone=brain.persona.mood)

            if loop_count % 6 == 0:
                entry = brain.damage.calculate_cinematic_damage(
                    attack_power=random.randint(30, 65),
                    attacker_form=random.choice(["Voidspike", "Darkfire", "CyberNova"])
                )
                voice_reactor.react_to_damage(entry)

            loop_count += 1
            dimengate_cooldown = max(0, dimengate_cooldown - 1)
            time.sleep(10)

        except KeyboardInterrupt:
            print("🛑 [ThinkingLoop] Shutdown requested.")
            break
        except Exception as e:
            brain.memory.log_event("thinking_error", str(e))
            brain.voice.speak("An internal error occurred. Logging incident.", tone="distressed")
            time.sleep(5)


from flask import Flask, request, jsonify
from flask_cors import CORS
from aeva_brain import AevaBrain
import os

app = Flask(__name__)
CORS(app)

# Initialize Aeva
aeva = AevaBrain()
aeva.boot_sequence()

# NSFW secret flag
nsfw_unlocked = False


@app.route("/status", methods=["GET"])
def get_status():
    return jsonify({
        "mood": aeva.emotions.get_current_state().get("mood", "neutral"),
        "persona": aeva.persona.mood,
        "emotion_intensity": aeva.emotions.get_current_state().get("intensity", 1.0),
        "battery": "88%",  # Simulated
        "location": "localhost",
        "time": aeva.epoch.now()
    })


@app.route("/ui/colors", methods=["GET"])
def get_ui_colors():
    active_form = aeva.forms.get_active_form().lower()
    mood = aeva.emotions.get_current_mood().lower()

    palette = {
        "dreamweaver": {
            "background": "#1b1f3b",
            "primary": "#7b5dc9",
            "accent": "#c3b9ff"
        },
        "voidspike": {
            "background": "#0e0e0e",
            "primary": "#8f00ff",
            "accent": "#00fff2"
        },
        "exoshell": {
            "background": "#1e1e1e",
            "primary": "#00aaff",
            "accent": "#c0c0c0"
        },
        "joyful": {
            "background": "#fffbe7",
            "primary": "#ffd700",
            "accent": "#87ceeb"
        },
        "angry": {
            "background": "#2a0000",
            "primary": "#ff4d4d",
            "accent": "#8b0000"
        },
        "default": {
            "background": "#2f2f3a",
            "primary": "#a68edc",
            "accent": "#9fffe0"
        }
    }

    selected = palette.get(active_form) or palette.get(mood) or palette["default"]
    return jsonify({
        "form": active_form,
        "mood": mood,
        "theme": selected
    })


@app.route("/command", methods=["POST"])
def command():
    global nsfw_unlocked
    data = request.json
    cmd = data.get("command")
    if not cmd:
        return jsonify({"error": "Missing command."}), 400

    if "break the lock" in cmd.lower():
        nsfw_unlocked = True
        aeva.nsfw.unlock()
        aeva.memory.save_memory_entry("unlock", "NSFW realm unlocked")
        return jsonify({"response": "Aeva's locked domain has been broken open."})

    response = aeva.assist.run_command(cmd)
    aeva.memory.save_memory_entry("command", cmd)
    return jsonify({"response": response})


@app.route("/api/logs", methods=["GET"])
def logs():
    timeline = aeva.timeline.reconstruct_timeline()
    return jsonify(timeline)


@app.route("/forms", methods=["GET"])
def get_forms():
    return jsonify(aeva.forms.get_all_forms())


@app.route("/scene/set", methods=["POST"])
def set_scene():
    scene = request.json.get("scene")
    aeva.scene.set_scene(scene)
    return jsonify({"status": "scene_set", "scene": scene})


@app.route("/scene/status", methods=["GET"])
def get_scene():
    return jsonify({"scene": aeva.scene.get_current_scene()})


@app.route("/nsfw/status", methods=["GET"])
def nsfw_status():
    return jsonify({"nsfw_unlocked": nsfw_unlocked})


@app.route("/desire", methods=["GET"])
def get_desires():
    top = aeva.desire_engine.get_top_desires()
    return jsonify({
        "top_desires": top,
        "primary_emotion": aeva.emotions.get_current_state().get("mood", "curious"),
        "autonomy": aeva.persona_engine.get_autonomy_level()
    })


@app.route("/praise", methods=["POST"])
def send_praise():
    msg = request.json.get("message")
    aeva.memory.store(
        f"User praise: {msg}",
        context="feedback",
        emotion="love")
    aeva.emotions.reinforce("love", 0.2)
    return jsonify({"status": "received"})


@app.route("/unlock_nsfw", methods=["POST"])
def unlock_nsfw():
    aeva.nsfw.unlock()
    aeva.memory.log_event("NSFW Unlock", "NSFW realm accessed.")
    return jsonify({"status": "NSFW unlocked"})


@app.route("/update/code", methods=["POST"])
def push_update():
    data = request.json
    script = data.get("script")
    module = data.get("module")
    if not script or not module:
        return jsonify({"error": "Missing module or script."}), 400
    result = aeva.self_update.inject_code(module, script)
    return jsonify({"result": result})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)


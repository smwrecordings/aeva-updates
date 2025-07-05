# ~/aeva/stream_controller.py

import threading
import time
from flask import Flask, Response, request
from flask_cors import CORS
from battle_engine import AevaBattleEngine

# In-memory broadcast state
stream_log = []
listeners = []
current_battle = None

app = Flask(__name__)
CORS(app)

def stream_generator():
    last_index = 0
    while True:
        if len(stream_log) > last_index:
            data = stream_log[last_index]
            last_index += 1
            yield f"data: {data}\n\n"
        time.sleep(0.5)

@app.route("/battle/stream")
def stream():
    return Response(stream_generator(), mimetype="text/event-stream")

@app.route("/battle/initiate", methods=[POST])
def initiate():
    global current_battle
    from aeva_brain import AevaBrain

    aeva1 = AevaBrain()
    aeva2 = AevaBrain()

    aeva1.persona.set_gender("female")
    aeva2.persona.set_gender("male")
    aeva1.persona.name = "Aeva-X"
    aeva2.persona.name = "Aevan-Z"

    current_battle = AevaBattleEngine(aeva1, aeva2)

    def stream_thread():
        current_battle.simulate_battle(stream_callback=stream_log.append)

    threading.Thread(target=stream_thread, daemon=True).start()

    return {"status": "battle_started"}

@app.route("/battle/log")
def get_log():
    return {"log": stream_log[-50:]}

@app.route("/battle/status")
def status():
    if not current_battle:
        return {"status": "idle"}
    return {
        "status": "active",
        "round": current_battle.turn,
        "recent": stream_log[-1] if stream_log else "None"
    }

if __name__ == "__main__":
    app.run(port=5050, debug=True)

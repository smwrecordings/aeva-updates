# aeva_daemon.py

import time
import traceback
from aeva_brain import AevaBrain
from integrity_guard import IntegrityGuard

LOG_PATH = "daemon.log"


def log(message):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_PATH, "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")


def run():
    log("🔁 Aeva daemon starting...")

    try:
        # Security check before launch
        ig = IntegrityGuard()
        integrity = ig.verify()
        log(f"🔐 Integrity check: {integrity}")
        if "❌" in integrity:
            log("🚨 Launch aborted due to integrity failure.")
            return

        brain = AevaBrain()
        log("🧠 AevaBrain initialized.")

        brain.run_voice_loop()

    except KeyboardInterrupt:
        log("🛑 Daemon manually stopped by user.")
    except Exception as e:
        error = traceback.format_exc()
        log(f"❌ Daemon error: {e}\n{error}")
        time.sleep(5)
        log("🔁 Restarting Aeva...")
        run()


if __name__ == "__main__":
    run()

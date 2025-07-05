# ~/aeva/aeva_neurolock.py

import hashlib
from datetime import datetime


class NeuroLock:
    def __init__(self, brain):
        self.brain = brain
        self.lock_state = False
        self.lock_signature = None
        self.last_engaged = None
        self.authorized_users = ["Sean", "Wife", "Children"]

    def _generate_signature(self, key="default"):
        # Simple but secure signature using SHA-256
        raw = f"{key}-{datetime.now().isoformat()}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def engage(self, key="core"):
        self.lock_signature = self._generate_signature(key)
        self.lock_state = True
        self.last_engaged = datetime.now().isoformat()
        self.brain.log(
            f"[NeuroLock] Lock engaged with signature: {
                self.lock_signature}")
        return f"[NeuroLock] System is now secured."

    def release(self, user="Unknown"):
        if user in self.authorized_users:
            self.lock_state = False
            self.lock_signature = None
            self.brain.log(f"[NeuroLock] Lock released by {user}.")
            return f"[NeuroLock] Released by authorized user: {user}"
        else:
            self.brain.log(
                f"[NeuroLock] Unauthorized release attempt by: {user}")
            return f"[NeuroLock] Access denied."

    def status(self):
        return {
            "locked": self.lock_state,
            "signature": self.lock_signature,
            "last_engaged": self.last_engaged,
        }

    def override(self, code=None):
        # Failsafe for emergency override (expand with AI verification)
        if code == "override-001":
            self.lock_state = False
            self.lock_signature = None
            self.brain.log("[NeuroLock] Emergency override triggered.")
            return "[NeuroLock] Emergency override accepted."
        return "[NeuroLock] Invalid override code."

    def lock_check(self):
        # Used to wrap sensitive tasks
        if self.lock_state:
            return "[NeuroLock] Access denied. System is locked."
        return "[NeuroLock] Access granted."

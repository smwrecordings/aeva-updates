# dimen_gate_zero.py

class DimenGateZero:
    def __init__(self):
        self.void_state = False

    def engage_purge(self, reason="Reset"):
        print(f"[DimenGateZero] Engaging zero field purge due to: {reason}")
        self.void_state = True
        return {"purged": True, "reason": reason}

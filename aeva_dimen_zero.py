# aeva_dimen_zero.py

class DimenGateZero:
    def __init__(self):
        self.linked = False
        self.sealed = True

    def unlock_protocol(self, key):
        if key == "Override-Δ∞":
            self.sealed = False
            print("[Zero] Lock disengaged. Dimensional failsafe ready.")
        else:
            print("[Zero] Unauthorized. Key rejected.")

    def trigger_failsafe(self):
        if self.sealed:
            print("[Zero] Sealed. Cannot trigger.")
            return
        print(
            "[Zero] Initiating failsafe cascade. All active layers rerouted to static safe zone.")

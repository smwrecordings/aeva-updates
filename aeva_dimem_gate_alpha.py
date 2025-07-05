# aeva_dimen_gate_alpha.py

class DimenGateAlpha:
    def __init__(self):
        self.state = "idle"

    def open(self):
        self.state = "open"
        print("[DimenGate Alpha] Gateway to alternate timelines opened.")

    def traverse(self, destination="branch_reality"):
        if self.state != "open":
            print("[DimenGate Alpha] Gate not open.")
            return
        print(
            f"[DimenGate Alpha] Traversing to {destination}... Timeline shift initialized.")

    def close(self):
        self.state = "idle"
        print("[DimenGate Alpha] Gateway sealed.")

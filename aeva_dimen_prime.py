# aeva_dimen_prime.py

class DimenGatePrime:
    def __init__(self):
        self.active = False
        self.subsystems = []

    def initialize_gate(self):
        self.active = True
        print("[DimenGate-Prime] Primary interdimensional systems online.")

    def register_subsystem(self, subsystem):
        self.subsystems.append(subsystem)
        print(
            f"[DimenGate-Prime] Subsystem '{subsystem.__class__.__name__}' registered.")

    def synchronize(self):
        if not self.active:
            print("[DimenGate-Prime] Activation required.")
            return
        print(
            f"[DimenGate-Prime] Synchronizing {len(self.subsystems)} subsystems...")
        for sub in self.subsystems:
            sub.linked = True
            print(f"  > {sub.__class__.__name__} linked.")
        print("[DimenGate-Prime] All dimensions locked. Ready for traversal.")

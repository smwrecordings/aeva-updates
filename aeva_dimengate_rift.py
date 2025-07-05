# aeva_dimengate_rift.py

import random
import time


class DimenGateRift:
    def __init__(self):
        self.energy = 100

    def open_rift(self, origin, destination):
        if self.energy < 20:
            print("[DimenGate:Rift] Not enough energy to open rift.")
            return
        self.energy -= 20
        print(f"[DimenGate:Rift] Portal opened from {origin} to {destination}")
        time.sleep(2)
        print(f"[DimenGate:Rift] Rift stable. Payload transmitted.")


# Example
if __name__ == "__main__":
    rift = DimenGateRift()
    rift.open_rift("192.168.0.1", "dimengate://alternate-node")

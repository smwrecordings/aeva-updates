# aeva_dimengate5.py

import base64


class DimenGateObscura:
    def __init__(self):
        self.vault = {}

    def encrypt_and_store(self, label, data):
        encoded = base64.b64encode(data.encode()).decode()
        self.vault[label] = encoded
        print(f"[DimenGate-V] {label} stored in obscura vault.")
        return encoded

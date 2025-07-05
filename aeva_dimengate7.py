# aeva_dimengate7.py

import time


class DimenGatePortalframe:
    def __init__(self):
        self.portals_opened = []

    def open_gateway(self, target_realm):
        timestamp = datetime.utcnow().isoformat()
        print(
            f"[DimenGate-VII] Portal opened to {target_realm} at {timestamp}")
        self.portals_opened.append(
            {"realm": target_realm, "opened": timestamp})
        time.sleep(1)
        return f"↯ Gateway {target_realm} stabilized."

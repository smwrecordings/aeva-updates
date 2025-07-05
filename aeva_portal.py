# aeva_portal.py

import os
import json
import uuid
from datetime import datetime


class InterdimensionalPortal:
    def __init__(self, gateway_dir="assets/data/portals"):
        self.gateway_dir = gateway_dir
        os.makedirs(self.gateway_dir, exist_ok=True)
        self.active_portals = {}

    def open_gateway(self, name, parameters):
        gateway_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        gateway = {
            "id": gateway_id,
            "name": name,
            "timestamp": timestamp,
            "parameters": parameters,
            "status": "open"
        }
        self.active_portals[gateway_id] = gateway
        self._save_gateway(gateway)
        print(
            f"[Portal] Opened interdimensional gateway '{name}' with ID {gateway_id}")
        return gateway

    def close_gateway(self, gateway_id):
        if gateway_id in self.active_portals:
            self.active_portals[gateway_id]['status'] = "closed"
            self._save_gateway(self.active_portals[gateway_id])
            print(f"[Portal] Closed gateway with ID {gateway_id}")
        else:
            print(f"[Portal] No such gateway: {gateway_id}")

    def list_gateways(self):
        print(f"[Portal] Listing {len(self.active_portals)} gateways:")
        for gw in self.active_portals.values():
            print(f" - {gw['name']} ({gw['status']})")
        return list(self.active_portals.values())

    def simulate_universe(self, laws, seed_entities):
        universe_id = str(uuid.uuid4())
        simulation = {
            "universe_id": universe_id,
            "created": datetime.utcnow().isoformat(),
            "laws": laws,
            "entities": seed_entities
        }
        path = os.path.join(self.gateway_dir, f"universe_{universe_id}.json")
        with open(path, 'w') as f:
            json.dump(simulation, f, indent=4)
        print(f"[Portal] Simulated new universe with ID {universe_id}")
        return universe_id

    def _save_gateway(self, gateway):
        path = os.path.join(self.gateway_dir, f"gateway_{gateway['id']}.json")
        with open(path, 'w') as f:
            json.dump(gateway, f, indent=4)


# Example usage
if __name__ == "__main__":
    portal = InterdimensionalPortal()
    g = portal.open_gateway(
        "Quantum Nexus", {
            "frequency": "144.7 THz", "anchor": "entropy-tether"})
    portal.simulate_universe({"gravity": "9.8", "dimensions": 11}, [
                             "Zarnax the Architect", "Etherian Cloud"])
    portal.list_gateways()
    portal.close_gateway(g['id'])

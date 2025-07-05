# aeva_galaxyweave.py

import json
import os
from datetime import datetime
import requests


class GalaxyWeave:
    def __init__(self, data_path="assets/data/galaxy_logs.json"):
        self.data_path = data_path
        self.events = []
        os.makedirs(os.path.dirname(data_path), exist_ok=True)

    def fetch_cosmic_data(self):
        try:
            url = "https://services.swpc.noaa.gov/json/planetary_k_index_1m.json"
            r = requests.get(url)
            data = r.json()
            self._log_event("CosmicData", {"data": data[:5]})
            print("[GalaxyWeave] Fetched cosmic data.")
            return data
        except Exception as e:
            print(f"[GalaxyWeave] Error: {e}")
            return None

    def _log_event(self, label, metadata):
        event = {
            "timestamp": datetime.utcnow().isoformat(),
            "label": label,
            "metadata": metadata}
        self.events.append(event)
        with open(self.data_path, "w") as f:
            json.dump(self.events, f, indent=4)

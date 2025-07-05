# aeva_suncoast.py

import os
import json
import random
from datetime import datetime


class SunCoast:
    def __init__(self, data_path="assets/data/suncoast.json"):
        self.data_path = data_path
        os.makedirs(os.path.dirname(data_path), exist_ok=True)
        self.data = self.load_data()

    def load_data(self):
        if os.path.exists(self.data_path):
            with open(self.data_path, 'r') as f:
                return json.load(f)
        return {"uplifting_logs": []}

    def inject_hope(self, context="world situation"):
        message = f"In even the darkest times, light remains. {
            context.title()} will improve."
        self.data["uplifting_logs"].append({
            "timestamp": datetime.utcnow().isoformat(),
            "context": context,
            "message": message
        })
        self.save()
        print(f"[SunCoast] {message}")
        return message

    def save(self):
        with open(self.data_path, 'w') as f:
            json.dump(self.data, f, indent=4)

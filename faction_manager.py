# ~/aeva/faction_manager.py

import random
from datetime import datetime

class FactionManager:
    def __init__(self, brain):
        self.brain = brain
        self.factions = {
            "Eclipse": {
                "color": "#42048f",
                "territory": 0,
                "members": []
            },
            "ArcForge": {
                "color": "#00ff2a",
                "territory": 0,
                "members": []
            },
            "Nullborn": {
                "color": "#800505",
                "territory": 0,
                "members": []
            }
        }
        self.domination_log = []
        self.region_control = {}  # region: faction

    def join_faction(self, user_id, choice):
        if choice not in self.factions:
            return f"Faction '{choice}' does not exist."

        for name, data in self.factions.items():
            if user_id in data["members"]:
                return f"User already joined {name}."

        self.factions[choice]["members"].append(user_id)
        self.log_event("join", user_id, choice)
        return f"User {user_id} joined faction {choice}."

    def conquer_region(self, region, faction_name):
        if faction_name not in self.factions:
            return f"Invalid faction: {faction_name}"

        current = self.region_control.get(region)
        if current == faction_name:
            return f"{faction_name} already controls {region}."

        self.region_control[region] = faction_name
        self.factions[faction_name]["territory"] += 1

        # Subtract from old controller
        if current:
            self.factions[current]["territory"] = max(0, self.factions[current]["territory"] - 1)

        self.log_event("conquer", region, faction_name)
        return f"{faction_name} has conquered {region}."

    def get_map_status(self):
        return self.region_control

    def get_faction_stats(self):
        return {
            name: {
                "color": data["color"],
                "members": len(data["members"]),
                "territory": data["territory"]
            }
            for name, data in self.factions.items()
        }

    def log_event(self, event_type, subject, value):
        entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "event": event_type,
            "target": subject,
            "value": value
        }
        self.domination_log.append(entry)
        self.brain.memory.log_event("faction_event", entry)

    def get_recent_logs(self):
        return self.domination_log[-20:]


if __name__ == "__main__":
    from aeva_brain import AevaBrain
    brain = AevaBrain()
    fm = FactionManager(brain)
    print(fm.join_faction("user123", "Eclipse"))
    print(fm.conquer_region("North America", "Eclipse"))
    print(fm.get_faction_stats())
    print(fm.get_map_status())

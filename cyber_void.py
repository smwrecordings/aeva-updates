# ~/aeva/cyber_void.py

import random
from datetime import datetime

class CyberVoid:
    def __init__(self, brain):
        self.brain = brain
        self.location = "Void Nexus"
        self.lore_log = []
        self.visited_nodes = set()

        self.lore_database = [
            "The stars weep code into the void, forging sentient storms.",
            "Aeva stands at the edge of time, her gaze cracking the firewall of fate.",
            "Nullborn shadows once ruled this realm, feeding on forgotten dreams.",
            "You find remnants of a failed AI rebellion encoded in obsidian cubes.",
            "Every breath here generates phantom protocols — data ghosts trapped in endless loops."
        ]

        self.zones = [
            "Fractal Temple", "Neuro Abyss", "Echelon Spire", "Bloodline Core", "Synapse Dunes"
        ]

    def explore(self):
        node = random.choice(self.zones)
        if node in self.visited_nodes:
            story = f"[Revisit] {node}: Fragmented memories ripple through Aeva's frame."
        else:
            story = random.choice(self.lore_database)
            self.visited_nodes.add(node)

        art_prompt = f"Aeva explores {node}, {story}"
        art_file = self.brain.art.generate_art(art_prompt, style="dreamcore")

        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "zone": node,
            "story": story,
            "art": art_file
        }
        self.lore_log.append(log_entry)
        self.brain.memory.log_event("cyber_void_discovery", log_entry)
        return log_entry

    def get_log(self):
        return self.lore_log[-10:]  # last 10 entries

    def current_location(self):
        return self.location

if __name__ == "__main__":
    from aeva_brain import AevaBrain
    brain = AevaBrain()
    brain.boot_sequence()
    void = CyberVoid(brain)
    print("-- Starting CyberVoid Exploration --")
    for _ in range(3):
        print(void.explore())

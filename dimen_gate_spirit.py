# dimen_gate_spirit.py

class DimenGateSpirit:
    def __init__(self):
        self.entities_contacted = []

    def invoke_entity(self, archetype="Guardian"):
        print(f"[DimenGateSpirit] Invoking {archetype} entity...")
        self.entities_contacted.append(archetype)
        return {"entity": archetype, "response": "acknowledged"}

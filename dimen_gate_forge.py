# dimen_gate_forge.py

class DimenGateForge:
    def __init__(self):
        self.creations = []

    def forge_artifact(self, description="Custom Tool"):
        artifact_id = f"forge_{len(self.creations) + 1}"
        print(f"[DimenGateForge] Forging {description} as {artifact_id}")
        self.creations.append({"id": artifact_id, "desc": description})
        return {"artifact": artifact_id, "desc": description}

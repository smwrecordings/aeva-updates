# dimen_gate_stellar.py

class DimenGateStellar:
    def __init__(self):
        self.star_nodes = []

    def ping_stellar_node(self, name):
        print(f"[DimenGateStellar] Pinging stellar node: {name}")
        self.star_nodes.append(name)
        return {"node": name, "status": "active"}

# aeva_neural_constellation.py

import os
import json
from uuid import uuid4
from datetime import datetime
from collections import defaultdict


class NeuralConstellation:
    def __init__(self, node_dir="assets/data/neural_constellations"):
        self.node_dir = node_dir
        os.makedirs(self.node_dir, exist_ok=True)
        self.constellation = defaultdict(dict)
        self.memory_cache = {}

    def create_node(self, concept, metadata=None):
        node_id = str(uuid4())
        node_data = {
            "id": node_id,
            "concept": concept,
            "timestamp": datetime.utcnow().isoformat(),
            "metadata": metadata or {},
            "connections": []
        }
        self.constellation[concept] = node_data
        self._persist_node(node_data)
        print(f"[NeuralConstellation] Node created: {concept} → {node_id}")
        return node_id

    def _persist_node(self, node):
        filepath = os.path.join(self.node_dir, f"{node['id']}.json")
        with open(filepath, 'w') as f:
            json.dump(node, f, indent=4)

    def connect_nodes(self, concept_a, concept_b):
        if concept_a not in self.constellation or concept_b not in self.constellation:
            print("[NeuralConstellation] One or both nodes not found.")
            return False

        a = self.constellation[concept_a]
        b = self.constellation[concept_b]

        if b['id'] not in a['connections']:
            a['connections'].append(b['id'])
            self._persist_node(a)
        if a['id'] not in b['connections']:
            b['connections'].append(a['id'])
            self._persist_node(b)

        print(f"[NeuralConstellation] Connected '{concept_a}' ↔ '{concept_b}'")
        return True

    def visualize_map(self):
        print("\n[NeuralConstellation] Current Map:")
        for concept, node in self.constellation.items():
            links = len(node['connections'])
            print(f"  • {concept} ({links} links)")

    def search_related_concepts(self, concept):
        if concept not in self.constellation:
            print("[NeuralConstellation] Concept not found.")
            return []

        node = self.constellation[concept]
        related = []
        for cid in node['connections']:
            path = os.path.join(self.node_dir, f"{cid}.json")
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data = json.load(f)
                    related.append(data['concept'])

        print(f"[NeuralConstellation] Related to '{concept}': {related}")
        return related

    def pulse_thoughts(self, seed):
        print(f"[NeuralConstellation] Pulsing thoughts from: {seed}")
        visited = set()
        wave = [seed]
        trail = []

        while wave:
            current = wave.pop(0)
            if current in visited:
                continue
            visited.add(current)
            trail.append(current)

            related = self.search_related_concepts(current)
            for r in related:
                if r not in visited:
                    wave.append(r)

        print(f"[NeuralConstellation] Thought trail: {trail}")
        return trail


# Example usage
if __name__ == "__main__":
    brain = NeuralConstellation()
    brain.create_node("Freedom")
    brain.create_node("Choice")
    brain.create_node("Responsibility")
    brain.connect_nodes("Freedom", "Choice")
    brain.connect_nodes("Choice", "Responsibility")
    brain.visualize_map()
    brain.pulse_thoughts("Freedom")

# aeva_dimengate_riftweave.py

import os
import uuid
from datetime import datetime
from collections import defaultdict


class RiftWeave:
    def __init__(self, rift_dir="assets/data/riftweave"):
        self.rift_dir = rift_dir
        os.makedirs(self.rift_dir, exist_ok=True)
        self.rifts = defaultdict(dict)

    def weave(self, dimension_key, entry_point, payload, metadata=None):
        rift_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat()
        rift_data = {
            "id": rift_id,
            "timestamp": timestamp,
            "dimension": dimension_key,
            "entry": entry_point,
            "payload": payload,
            "metadata": metadata or {}
        }
        self.rifts[dimension_key][rift_id] = rift_data
        self._persist(rift_data)
        print(
            f"[RiftWeave] Wove rift into dimension '{dimension_key}' at {timestamp}.")
        return rift_id

    def _persist(self, rift_data):
        dim_folder = os.path.join(self.rift_dir, rift_data["dimension"])
        os.makedirs(dim_folder, exist_ok=True)
        file_path = os.path.join(dim_folder, f"{rift_data['id']}.json")
        with open(file_path, 'w') as f:
            json.dump(rift_data, f, indent=4)

    def traverse(self, dimension_key):
        if dimension_key not in self.rifts:
            print(f"[RiftWeave] No known rifts in '{dimension_key}'.")
            return []
        return list(self.rifts[dimension_key].values())

    def locate(self, keyword):
        results = []
        for dimension in self.rifts:
            for rift_id, data in self.rifts[dimension].items():
                if keyword.lower() in json.dumps(data).lower():
                    results.append(data)
        print(
            f"[RiftWeave] Located {
                len(results)} rifts matching '{keyword}'.")
        return results

    def collapse_rift(self, rift_id):
        for dimension in self.rifts:
            if rift_id in self.rifts[dimension]:
                del self.rifts[dimension][rift_id]
                path = os.path.join(
                    self.rift_dir, dimension, f"{rift_id}.json")
                if os.path.exists(path):
                    os.remove(path)
                print(
                    f"[RiftWeave] Collapsed rift {rift_id} in '{dimension}'.")
                return True
        print(f"[RiftWeave] Rift {rift_id} not found.")
        return False


# Example usage
if __name__ == "__main__":
    rift = RiftWeave()
    rift_id = rift.weave(
        "prediction_layer", "event.trigger", {
            "cause": "paradox", "effect": "temporal drift"})
    rift.traverse("prediction_layer")
    rift.locate("paradox")
    rift.collapse_rift(rift_id)

# aeva_dimengate_mirror.py

import shutil
import os


class DimenGateMirror:
    def __init__(self, mirror_dir="assets/data/mirror_cache"):
        self.mirror_dir = mirror_dir
        os.makedirs(self.mirror_dir, exist_ok=True)

    def mirror_file(self, filepath):
        if not os.path.exists(filepath):
            print(f"[DimenGate:Mirror] File not found: {filepath}")
            return
        filename = os.path.basename(filepath)
        mirrored_path = os.path.join(self.mirror_dir, f"mirror_{filename}")
        shutil.copy(filepath, mirrored_path)
        print(f"[DimenGate:Mirror] File mirrored: {mirrored_path}")


# Example
if __name__ == "__main__":
    mirror = DimenGateMirror()
    mirror.mirror_file("assets/data/secret_payload.json")

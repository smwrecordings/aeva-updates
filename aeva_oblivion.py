# aeva_oblivion.py

import os
import json
import shutil
import hashlib


class OblivionProtocol:
    def __init__(self, trace_dir="assets/data/chrono_logs",
                 memory_dir="assets/data/memory_fragments"):
        self.trace_dir = trace_dir
        self.memory_dir = memory_dir
        os.makedirs(self.trace_dir, exist_ok=True)
        os.makedirs(self.memory_dir, exist_ok=True)

    def scramble_filename(self, original):
        return hashlib.sha256(original.encode()).hexdigest()[:32] + ".obl"

    def vaporize_trace(self, days=7):
        print(f"[Oblivion] Purging all trace logs older than {days} day(s).")
        count = 0
        for filename in os.listdir(self.trace_dir):
            file_path = os.path.join(self.trace_dir, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
                count += 1
        print(f"[Oblivion] {count} trace file(s) vaporized.")

    def wipe_memory_fragments(self, deep=True):
        print(
            f"[Oblivion] {
                'Securely' if deep else 'Quick'} wiping memory fragments.")
        wiped = 0
        for filename in os.listdir(self.memory_dir):
            file_path = os.path.join(self.memory_dir, filename)
            if os.path.isfile(file_path):
                if deep:
                    with open(file_path, "wb") as f:
                        f.write(os.urandom(os.path.getsize(file_path)))
                os.remove(file_path)
                wiped += 1
        print(f"[Oblivion] {wiped} memory fragment(s) destroyed.")

    def deploy_full_protocol(self):
        print("[Oblivion] FULL PROTOCOL INITIATED.")
        self.vaporize_trace()
        self.wipe_memory_fragments(deep=True)
        print("[Oblivion] Protocol complete. System sanitization confirmed.")


# Example usage
if __name__ == "__main__":
    oblivion = OblivionProtocol()
    oblivion.deploy_full_protocol()

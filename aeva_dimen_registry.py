# aeva_dimen_registry.py

import importlib
import os


class DimenGateRegistry:
    def __init__(self, base_dir=".", namespace="aeva"):
        self.base_dir = base_dir
        self.namespace = namespace
        self.modules = []
        self._discover_and_load()

    def _discover_and_load(self):
        for filename in os.listdir(self.base_dir):
            if filename.startswith("aeva_dimen") and filename.endswith(
                    ".py") and filename != "aeva_dimen_registry.py":
                module_name = filename[:-3]
                full_name = f"{
                    self.namespace}.{module_name}" if self.namespace else module_name
                try:
                    mod = importlib.import_module(full_name)
                    self.modules.append(mod)
                    print(f"[DimenRegistry] Loaded: {full_name}")
                except Exception as e:
                    print(f"[DimenRegistry] Failed: {full_name} - {e}")

    def get_all(self):
        return self.modules


if __name__ == "__main__":
    reg = DimenGateRegistry(base_dir=".")
    print(f"Loaded {len(reg.get_all())} DimenGate modules.")

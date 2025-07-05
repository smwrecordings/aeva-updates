# integrity_guard.py
# Code Sovereignty & Security Layer for Aeva

import os
import hashlib
import json


class IntegrityGuard:
    def __init__(self, whitelist_path=".file_whitelist.json"):
        self.device_fingerprint = self._generate_fingerprint()
        self.whitelist_path = whitelist_path
        self.core_files = [
            "aeva.py",
            "aeva_brain.py",
            "plugin_handler.py",
            "memory.py",
            "persona.py",
            "sensors.py",
            "voice.py",
            "voice_input.py",
            "self_update.py",
            "explorer.py",
            "mission_guardian.py",
            "aeva_coreos.py",
            "wearable_bridge.py",
            "wearable_interface.py"]
        self.allowed_plugins = "plugins"

    def _generate_fingerprint(self):
        return hashlib.sha256(os.uname().nodename.encode()).hexdigest()

    def _hash_file(self, path):
        try:
            with open(path, "rb") as f:
                return hashlib.sha256(f.read()).hexdigest()
        except Exception as e:
            return None

    def create_whitelist(self):
        whitelist = {
            "fingerprint": self.device_fingerprint,
            "core": {},
            "plugins": {}}
        for f in self.core_files:
            hash_val = self._hash_file(f)
            if hash_val:
                whitelist["core"][f] = hash_val

        if os.path.isdir(self.allowed_plugins):
            for fname in os.listdir(self.allowed_plugins):
                if fname.endswith(".py"):
                    fpath = os.path.join(self.allowed_plugins, fname)
                    hash_val = self._hash_file(fpath)
                    if hash_val:
                        whitelist["plugins"][fname] = hash_val

        with open(self.whitelist_path, "w") as f:
            json.dump(whitelist, f, indent=2)
        print(f"✅ Whitelist created at {self.whitelist_path}")

    def verify(self):
        if not os.path.exists(self.whitelist_path):
            return "⚠️ No whitelist found."

        with open(self.whitelist_path, "r") as f:
            stored = json.load(f)

        current_fingerprint = self._generate_fingerprint()
        if stored.get("fingerprint") != current_fingerprint:
            return "🔐 Device fingerprint mismatch!"

        # Check core files
        for f, stored_hash in stored.get("core", {}).items():
            if self._hash_file(f) != stored_hash:
                return f"❌ Integrity failure: {f}"

        # Check plugins
        for fname, stored_hash in stored.get("plugins", {}).items():
            fpath = os.path.join(self.allowed_plugins, fname)
            if self._hash_file(fpath) != stored_hash:
                return f"❌ Plugin tampered: {fname}"

        return "✅ All core and plugin files verified."

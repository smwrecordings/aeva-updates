# aeva_autoupdate_scan.py

import os
import re
import json
from aeva_brain import AevaBrain
from aeva_self_update import AevaSelfUpdate

# Initialize brain and updater
aeva = AevaBrain()
updater = AevaSelfUpdate(aeva)

# Directories to scan for patching
SCAN_DIRS = ["./", "modules", "plugins"]
PATCH_KEYWORDS = [
    "omniscient",
    "autonomy",
    "aeonmind",
    "omninet",
    "persona_engine"]

# Omniscience logic to inject
INJECT_CODE = """
# Injected Omniscience Awareness
if hasattr(self, 'aeon') and hasattr(self.aeon, 'query_everything'):
    self.omniscience_enabled = True
    self.knowledge = self.aeon.query_everything(scope='global')
else:
    self.omniscience_enabled = False
"""

# Scan files for missing logic


def scan_and_patch():
    patched = []
    for root, _, files in os.walk("."):
        for file in files:
            if file.endswith(".py") and not file.startswith("_"):
                path = os.path.join(root, file)
                with open(path, "r") as f:
                    content = f.read()

                if not any(k in content for k in PATCH_KEYWORDS):
                    continue
                if "omniscience_enabled" in content:
                    continue  # already patched

                # Inject code just after class init if it exists
                modified = re.sub(
                    r"(def __init__\(self[^)]*\):\n)",
                    r"\1    " + INJECT_CODE + "\n",
                    content,
                    flags=re.MULTILINE)

                if modified != content:
                    with open(path, "w") as f:
                        f.write(modified)
                    patched.append(path)

    aeva.memory.save_memory_entry(
        "omniscient_patch", f"Patched {
            len(patched)} files.")
    return patched


# Run and log
if __name__ == "__main__":
    results = scan_and_patch()
    for file in results:
        print(f"[🔧] Patched: {file}")
    if not results:
        print("[✅] All files already contain omniscient logic.")

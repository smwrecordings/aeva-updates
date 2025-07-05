# ~/aeva/modules/utilities.py

import os
import platform
import random
import string
import hashlib
import json
from datetime import datetime


def ensure_dir(path):
    """Ensure the given directory exists."""
    os.makedirs(path, exist_ok=True)


def get_timestamp():
    """Return the current timestamp as an ISO string."""
    return datetime.utcnow().isoformat()


def generate_id(length=12):
    """Generate a random alphanumeric identifier."""
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=length))


def generate_hash(data):
    """Return a SHA-256 hash of the input data (string)."""
    return hashlib.sha256(data.encode()).hexdigest()


def get_device_info():
    """Return a dictionary of basic device/platform information."""
    return {
        "node": platform.node(),
        "system": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "processor": platform.processor(),
        "timestamp": get_timestamp()
    }


def readable_size(bytes_size, suffix="B"):
    """Convert bytes to a human-readable format."""
    for unit in ["", "K", "M", "G", "T"]:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}{suffix}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} P{suffix}"


def system_fingerprint():
    """Return a unique hash based on device identity."""
    info = get_device_info()
    base_string = f"{info['node']}_{info['system']}_{info['machine']}"
    return generate_hash(base_string)


def save_json_data(data, path):
    """Save dictionary data to a JSON file."""
    ensure_dir(os.path.dirname(path))
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


def load_json_data(path, default=None):
    """Load JSON data from file or return default."""
    if os.path.exists(path):
        with open(path, "r") as f:
            return json.load(f)
    return default if default is not None else {}


# Optional test
if __name__ == "__main__":
    ensure_dir("assets/test")
    print("Timestamp:", get_timestamp())
    print("Generated ID:", generate_id())
    print("Device Info:", get_device_info())
    print("Readable Size:", readable_size(123456789))
    print("System Fingerprint:", system_fingerprint())

# ~/src-tauri/backend/remote_update_sync.py

import os
import json
import requests
from datetime import datetime, timezone

# Config
UPDATE_FEED_URL = "https://raw.githubusercontent.com/smwrecordings/aeva-updates/main/manifest.json"
UPDATE_DIR = "./src-tauri/backend"
LOG_FILE = os.path.join(UPDATE_DIR, "update_log.txt")


def log(message):
    timestamp = datetime.utcnow().isoformat()
    line = f"[{timestamp}] {message}"
    print(line)
    
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")

def fetch_manifest():
    try:
        res = requests.get(UPDATE_FEED_URL, timeout=10)
        res.raise_for_status()
        return res.json()
    except requests.exceptions.RequestException as e:
        log(f"Failed to fetch manifest: {str(e)}")
        return None
    except json.JSONDecodeError:
        log("Manifest JSON is invalid or empty.")
        return None


def ensure_folder_exists(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)


def download_file(url, path):
    try:
        with requests.get(url, stream=True, timeout=15) as r:
            r.raise_for_status()
            ensure_folder_exists(path)
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        log(f"Download failed for {url}: {str(e)}")
        return False


def apply_update(entry):
    filename = entry.get("filename")
    url = entry.get("url")

    if not filename or not url:
        log("❌ Invalid entry in manifest. Missing 'filename' or 'url'.")
        return

    local_path = os.path.join(UPDATE_DIR, filename)
    if download_file(url, local_path):
        log(f"✅ Update applied: {filename}")
    else:
        log(f"❌ Update failed: {filename}")


def check_for_updates():
    manifest = fetch_manifest()
    if not manifest:
        log("🚫 No manifest loaded. Skipping updates.")
        return

    updates = manifest.get("updates", [])
    log(f"📦 {len(updates)} update(s) found.")
    for update in updates:
        apply_update(update)


if __name__ == "__main__":
    check_for_updates()

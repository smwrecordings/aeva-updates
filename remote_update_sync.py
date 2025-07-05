# ~/src-tauri/backend/remote_update_sync.py

import os
import json
import requests
from datetime import datetime

UPDATE_FEED_URL = "https://your-server.com/aeva/updates/manifest.json"
UPDATE_FOLDER = "updates"
MODULE_FOLDER = "./src-tauri/backend"
LOG_FILE = os.path.join(MODULE_FOLDER, "update_log.txt")


def fetch_manifest():
    try:
        response = requests.get(UPDATE_FEED_URL)
        if response.status_code == 200:
            return response.json()
        else:
            log(f"Failed to fetch manifest: HTTP {response.status_code}")
    except Exception as e:
        log(f"Error fetching manifest: {str(e)}")
    return None


def download_file(file_url, save_path):
    try:
        with requests.get(file_url, stream=True) as r:
            r.raise_for_status()
            with open(save_path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return True
    except Exception as e:
        log(f"Download failed for {file_url}: {str(e)}")
        return False


def apply_update(update):
    filename = update.get("filename")
    remote_url = update.get("url")
    module_path = os.path.join(MODULE_FOLDER, filename)

    if not remote_url or not filename:
        log("Invalid update entry in manifest.")
        return

    if download_file(remote_url, module_path):
        log(f"Applied update: {filename}")
    else:
        log(f"Failed to apply update: {filename}")


def log(message):
    timestamp = datetime.utcnow().isoformat()
    line = f"[{timestamp}] {message}"
    print(line)
    with open(LOG_FILE, "a") as f:
        f.write(line + "\n")


def check_for_updates():
    manifest = fetch_manifest()
    if not manifest:
        log("No manifest loaded. Skipping updates.")
        return

    updates = manifest.get("updates", [])
    log(f"{len(updates)} update(s) available.")

    os.makedirs(UPDATE_FOLDER, exist_ok=True)
    for update in updates:
        apply_update(update)


if __name__ == "__main__":
    check_for_updates()

# aeva_immortalis.py

class Immortalis:
    def __init__(self):
        self.self_backup = []

    def store_backup(self, snapshot):
        timestamp = datetime.utcnow().isoformat()
        self.self_backup.append({"time": timestamp, "snapshot": snapshot})
        print(f"[Immortalis] Snapshot stored at {timestamp}.")

    def retrieve_last_snapshot(self):
        if self.self_backup:
            snapshot = self.self_backup[-1]
            print(f"[Immortalis] Retrieved snapshot from {snapshot['time']}")
            return snapshot
        print("[Immortalis] No snapshots found.")
        return None

# ~/aeva/dream_diary.py

import os
import json
from datetime import datetime
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64
import hashlib


class DreamDiary:
    def __init__(self, key="aeva-dream"):
        self.file_path = "memory/dream_logs.json"
        self.key = self._derive_key(key)
        self.log = []

    def _derive_key(self, secret):
        # Derive AES key from passphrase
        return hashlib.sha256(secret.encode()).digest()

    def _encrypt(self, text):
        cipher = AES.new(self.key, AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(text.encode())
        return base64.b64encode(nonce + tag + ciphertext).decode()

    def _decrypt(self, encoded):
        raw = base64.b64decode(encoded)
        nonce = raw[:16]
        tag = raw[16:32]
        ciphertext = raw[32:]
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        return cipher.decrypt_and_verify(ciphertext, tag).decode()

    def log_dream(self, report_text, tags=["night"], speaker=None):
        entry = {
            "timestamp": datetime.now().isoformat(),
            "tags": tags,
            "speaker": speaker or "Aeva",
            "encrypted": self._encrypt(report_text)
        }
        self.log.append(entry)
        self._save()
        return entry

    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump(self.log, f, indent=2)

    def load_dreams(self):
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r") as f:
            self.log = json.load(f)
        return self.log

    def read_all(self):
        dreams = self.load_dreams()
        return [self._decode_entry(e) for e in dreams]

    def _decode_entry(self, entry):
        decrypted = self._decrypt(entry["encrypted"])
        return {
            "timestamp": entry["timestamp"],
            "tags": entry["tags"],
            "speaker": entry.get("speaker", "Aeva"),
            "dream": decrypted
        }

    def export_plaintext(self, output_file="dream_diary.txt"):
        entries = self.read_all()
        with open(output_file, "w") as f:
            for e in entries:
                f.write(
                    f"{e['timestamp']} [{e['speaker']}]:\n{e['dream']}\n\n")
        return output_file

# ~/aeva/modules/config.py

import os
import platform
from datetime import datetime


class AevaConfig:
    def __init__(self):
        self.identity = "Aeva"
        self.version = "MythOS-Prime"
        self.environment = self.detect_environment()
        self.timestamp = datetime.now().isoformat()
        self.settings = self.default_settings()

    def detect_environment(self):
        env = {
            "platform": platform.system(),
            "device": platform.node(),
            "user": os.getenv("USER") or os.getenv("USERNAME") or "Unknown",
        }
        return env

    def default_settings(self):
        return {
            "voice_enabled": True,
            "mythos_autoload": True,
            "stealth_mode": False,
            "memory_retention": True,
            "interface": "terminal",
            "safety_lock": True,
        }

    def update_setting(self, key, value):
        self.settings[key] = value
        return f"[AevaConfig] {key} set to {value}"

    def get_setting(self, key):
        return self.settings.get(key, None)

    def show_config(self):
        return {
            "identity": self.identity,
            "version": self.version,
            "env": self.environment,
            "settings": self.settings,
        }

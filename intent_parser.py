# intent_parser.py

import re
import datetime


class IntentParser:
    def __init__(self, memory):
        self.memory = memory

    def parse(self, text):
        text = text.lower().strip()

        if any(word in text for word in ["remember", "store", "save this"]):
            return "store_memory", {
                "memory": text.split("remember", 1)[-1].strip()}

        if "recall" in text or "what did i say" in text:
            return "recall_memory", {}

        if "what do you know about" in text:
            subject = text.split("about", 1)[-1].strip()
            return "recall_topic", {"topic": subject}

        if "what time is it" in text or "current time" in text:
            return "time_query", {}

        if "what day is it" in text or "current date" in text:
            return "date_query", {}

        if "status report" in text or "system status" in text:
            return "system_status", {}

        if "kill process" in text:
            pid = re.findall(r'\d+', text)
            return "kill_process", {
                "pid": int(
                    pid[0])} if pid else {
                "pid": None}

        if "run plugin" in text:
            name = text.split(
                "run plugin")[-1].strip().replace(" ", "_").lower()
            return "run_plugin", {"plugin": name}

        return "unknown", {"text": text}

    def handle(self, intent, data):
        if intent == "store_memory":
            self.memory.remember("note", data["memory"])
            return f"🧠 Got it: '{data['memory']}'"

        if intent == "recall_memory":
            return f"📦 Last note: {self.memory.recall('note')}"

        if intent == "recall_topic":
            return self.memory.search(data["topic"])

        if intent == "time_query":
            now = datetime.datetime.now().strftime("%H:%M:%S")
            return f"🕒 The time is {now}"

        if intent == "date_query":
            today = datetime.datetime.now().strftime("%A, %B %d, %Y")
            return f"📅 Today is {today}"

        if intent == "system_status":
            from aeva_coreos import AevaCoreOS
            return AevaCoreOS().to_json()

        if intent == "kill_process":
            from aeva_coreos import AevaCoreOS
            pid = data["pid"]
            if pid:
                return AevaCoreOS().kill_process(pid)
            return "⚠️ No process ID provided."

        if intent == "run_plugin":
            from plugin_handler import PluginHandler
            plugin = data["plugin"] + ".py"
            handler = PluginHandler()
            return handler.execute_plugin(plugin, "", {})

        return f"🤖 I'm not sure how to handle that: {data['text']}"

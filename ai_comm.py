# ai_comm.py

import json
import socket
import time
import requests


class AICommunicator:
    def __init__(self):
        self.history = []
        print("🌐 AI Communicator active.")

    def respond_to(self, prompt, tone="neutral", weight=1.0):
        """
        Simple AI placeholder response logic.
        Replace with LLM integration (like Ollama, LM Studio, or GPT API).
        """
        response = f"[Aeva Response] Based on tone '{tone}' and weight {weight:.2f}, I processed: '{prompt}'"
        self.history.append({
            "from": "user",
            "to": "aeva-core",
            "prompt": prompt,
            "response": response,
            "tone": tone,
            "weight": weight,
            "timestamp": time.time()
        })
        return response

    def search(self, query):
        return f"[SEARCH MODULE] Ready to handle query: '{query}'"

    def send_message(self, recipient, message):
        packet = {
            "from": "aeva-core",
            "to": recipient,
            "message": message,
            "timestamp": time.time()
        }
        self.history.append(packet)
        return f"[MSG] Sent to {recipient}: {message}"

    def receive_message(self, sender, message):
        response = f"[MSG] From {sender}: {message}"
        self.history.append({
            "from": sender,
            "to": "aeva-core",
            "message": message,
            "timestamp": time.time()
        })
        return response

    def connect_to_socket(self, host='127.0.0.1', port=5050):
        try:
            s = socket.socket()
            s.connect((host, port))
            s.send(b"Aeva connected.")
            data = s.recv(1024)
            s.close()
            return data.decode()
        except Exception as e:
            return f"Socket connection error: {e}"

    def ask_ai(self, question):
        return f"[INTERNAL AI] Awaiting module response to: '{question}'"

    def export_conversation_history(self, path="ai_comm_history.json"):
        try:
            with open(path, "w") as f:
                json.dump(self.history, f, indent=2)
            return f"[LOG] Exported to {path}"
        except Exception as e:
            return f"Export error: {e}"

    def handshake(self, system_id="unknown"):
        return f"[HANDSHAKE] Confirmed with: {system_id}"

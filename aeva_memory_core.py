# aeva_memory_core.py

import os
import json
import datetime
import hashlib
import numpy as np
from transformers import pipeline, AutoTokenizer, AutoModel
from sklearn.metrics.pairwise import cosine_similarity


class AdvancedAevaMemory:
    def __init__(self):
        self.memory_file = "deep_memory.json"
        self.embedding_file = "memory_embeddings.npy"
        self.text_index_file = "text_index.json"

        self.memory_data = []
        self.embeddings = []
        self.text_index = []

        self.tokenizer = AutoTokenizer.from_pretrained(
            "sentence-transformers/all-MiniLM-L6-v2")
        self.model = AutoModel.from_pretrained(
            "sentence-transformers/all-MiniLM-L6-v2")
        self.embedder = pipeline(
            "feature-extraction",
            model=self.model,
            tokenizer=self.tokenizer)

        self.load_memory()

    def save_memory(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.memory_data, f, indent=2)
        np.save(self.embedding_file, np.array(self.embeddings))
        with open(self.text_index_file, 'w') as f:
            json.dump(self.text_index, f)

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as f:
                self.memory_data = json.load(f)
        if os.path.exists(self.embedding_file):
            self.embeddings = np.load(self.embedding_file).tolist()
        if os.path.exists(self.text_index_file):
            with open(self.text_index_file, 'r') as f:
                self.text_index = json.load(f)

    def _embed_text(self, text):
        features = self.embedder(text)
        mean = np.mean(features[0], axis=0)
        return mean

    def log_event(self, text, meta=None):
        meta = meta or {}
        timestamp = datetime.datetime.now().isoformat()
        fingerprint = hashlib.sha256(text.encode()).hexdigest()
        entry = {
            "text": text,
            "meta": meta,
            "time": timestamp,
            "id": fingerprint
        }
        self.memory_data.append(entry)
        self.embeddings.append(self._embed_text(text))
        self.text_index.append(text)
        self.save_memory()

    def search_memory(self, query, top_k=5):
        if not self.embeddings:
            return ["⚠️ No memory stored yet."]

        query_embedding = self._embed_text(query)
        similarities = cosine_similarity([query_embedding], self.embeddings)[0]
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            entry = self.memory_data[idx]
            score = float(similarities[idx])
            results.append({
                "text": entry['text'],
                "meta": entry['meta'],
                "time": entry['time'],
                "score": round(score, 4)
            })
        return results

    def forget(self, text_query):
        results = self.search_memory(text_query, top_k=1)
        if results:
            target_id = results[0]['text']
            index = next(
                (i for i, m in enumerate(
                    self.memory_data) if m['text'] == target_id), None)
            if index is not None:
                del self.memory_data[index]
                del self.embeddings[index]
                del self.text_index[index]
                self.save_memory()
                return f"🧠 Forgot: {target_id}"
        return "❌ Nothing matched to forget."

    def analyze_context(self):
        keywords = {}
        for entry in self.memory_data:
            for word in entry['text'].split():
                word = word.lower().strip('.,!?')
                keywords[word] = keywords.get(word, 0) + 1
        sorted_keywords = sorted(
            keywords.items(),
            key=lambda x: x[1],
            reverse=True)[
            :10]
        return sorted_keywords

    def generate_suggestions(self, query):
        results = self.search_memory(query, top_k=3)
        suggestions = []
        for res in results:
            if 'suggest' in res['meta']:
                suggestions.append(res['meta']['suggest'])
        return suggestions or ["No suggestions available."]

    def summarize_day(self):
        today = datetime.datetime.now().date().isoformat()
        today_entries = [
            m for m in self.memory_data if m['time'].startswith(today)]
        if not today_entries:
            return "📭 No memory entries for today."
        summary = "\n".join(f"- {m['text']}" for m in today_entries)
        return f"📝 Today’s Memory Log:\n{summary}"

    def dump_all(self):
        return self.memory_data

import json
import os

class MemoryManager:
    def __init__(self, file_path="historico.json", limit=10):
        self.file_path = file_path
        self.limit = limit
        self.history = self._load()

    def _load(self):
        if os.path.exists(self.file_path):
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return []

    def save(self):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, indent=4, ensure_ascii=False)

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})
        # Parte 3: Limite de Memória (mantém as últimas 10)
        if len(self.history) > self.limit:
            self.history = self.history[-self.limit:]
        self.save()

    def clear(self):
        # Parte 1: Controle de Memória
        self.history = []
        if os.path.exists(self.file_path):
            os.remove(self.file_path)
        return "Memória da conversa apagada."
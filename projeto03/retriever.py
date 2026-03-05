import os
import numpy as np
from sentence_transformers import SentenceTransformer

class Retriever:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.knowledge_chunks = []
        self.embeddings = []
        # Carrega um modelo de embedding que roda localmente no seu PC
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self._prepare_knowledge()

    def _prepare_knowledge(self):
        if not os.path.exists(self.file_path):
            print(f"Erro: Arquivo {self.file_path} não encontrado.")
            return
        
        with open(self.file_path, "r", encoding="utf-8") as f:
            content = f.read()
            self.knowledge_chunks = [p.strip() for p in content.split('\n\n') if p.strip()]

        if self.knowledge_chunks:
            # Gera embeddings localmente
            self.embeddings = self.model.encode(self.knowledge_chunks)

    def get_relevant_context(self, query: str, top_k: int = 2):
        if not self.knowledge_chunks:
            return ""

        # Gera embedding da pergunta
        query_vec = self.model.encode([query])[0]

        # Cálculo de similaridade de cosseno com NumPy
        norm_query = np.linalg.norm(query_vec)
        norm_knowledge = np.linalg.norm(self.embeddings, axis=1)
        dot_product = np.dot(self.embeddings, query_vec)
        
        similarities = dot_product / (norm_knowledge * norm_query)

        top_indices = np.argsort(similarities)[-top_k:][::-1]
        return "\n".join([self.knowledge_chunks[i] for i in top_indices])
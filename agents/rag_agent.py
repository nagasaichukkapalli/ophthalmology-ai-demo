import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from utils.text_loader import TextLoader

class DiseaseRetrievalAgent:
    def __init__(self, data_path, embedding_dir):
        self.data_path = data_path
        self.embedding_dir = embedding_dir
        self.diseases = TextLoader.load_diseases(data_path)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self._build_index()

    def _build_index(self):
        if not self.diseases:
            return

        # Create corpus from disease descriptions and symptoms
        corpus = [f"{d['name']} {d['symptoms']} {d['description']}" for d in self.diseases]
        embeddings = self.model.encode(corpus)
        
        # Initialize FAISS
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(np.array(embeddings).astype('float32'))

    def retrieve(self, query, k=3):
        """
        Retrieves top-k relevant diseases based on query.
        """
        if not self.index:
            return []

        query_vec = self.model.encode([query])
        distances, indices = self.index.search(np.array(query_vec).astype('float32'), k)
        
        results = []
        for i, idx in enumerate(indices[0]):
            if idx < len(self.diseases):
                # Convert L2 distance to a similarity score (approximate)
                # 0 distance = 100% match.
                score = max(0, 100 - distances[0][i] * 10) 
                
                results.append({
                    "disease": self.diseases[idx],
                    "score": score
                })
        return results

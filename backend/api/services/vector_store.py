# Simple FAISS-based vector store wrapper (demo)
import os, json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, storage_dir, model_name='all-MiniLM-L6-v2'):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self.meta_file = os.path.join(self.storage_dir, 'metadata.json')
        self.index_file = os.path.join(self.storage_dir, 'faiss.index')
        self.model = SentenceTransformer(model_name)
        self.dim = self.model.get_sentence_embedding_dimension()
        self._load()

    def _load(self):
        if os.path.exists(self.meta_file):
            with open(self.meta_file, 'r', encoding='utf-8') as f:
                self.metadata = json.load(f)
        else:
            self.metadata = []
        if os.path.exists(self.index_file):
            try:
                self.index = faiss.read_index(self.index_file)
            except Exception:
                self.index = faiss.IndexFlatL2(self.dim)
        else:
            self.index = faiss.IndexFlatL2(self.dim)

    def save(self):
        with open(self.meta_file, 'w', encoding='utf-8') as f:
            json.dump(self.metadata, f, ensure_ascii=False, indent=2)
        try:
            faiss.write_index(self.index, self.index_file)
        except Exception:
            pass

    def upsert(self, docs):
        # docs: [{'id','file','chunk','text'}]
        texts = [d['text'] for d in docs]
        vecs = self.model.encode(texts, show_progress_bar=False)
        arr = np.array(vecs).astype('float32')
        self.index.add(arr)
        for i,d in enumerate(docs):
            meta = {'id': d['id'], 'file': d.get('file'), 'chunk': d.get('chunk',0), 'text': d['text']}
            # storing vectors in metadata avoided for brevity
            self.metadata.append(meta)
        self.save()

    def search(self, query, top_k=5):
        if self.index.ntotal == 0:
            return []
        vec = self.model.encode([query])
        q = np.array(vec).astype('float32')
        D,I = self.index.search(q, top_k)
        results = []
        for dist, idx in zip(D[0], I[0]):
            if idx<0 or idx>=len(self.metadata):
                continue
            m = self.metadata[idx]
            results.append({'score': float(dist), 'file': m['file'], 'chunk': m['chunk'], 'text': m['text']})
        return results

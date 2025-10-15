import os, uuid
from pathlib import Path
from pdfminer.high_level import extract_text as pdf_extract_text
import docx

CHUNK_SIZE = 500

class DocumentProcessor:
    def __init__(self, storage_dir, vector_store=None):
        self.storage_dir = storage_dir
        os.makedirs(self.storage_dir, exist_ok=True)
        self.vector_store = vector_store
        self.index = {}

    def _read_text(self, path):
        p = Path(path)
        if not p.exists():
            return ''
        suf = p.suffix.lower()
        try:
            if suf in ('.txt', '.csv'):
                return p.read_text(encoding='utf-8', errors='ignore')
            if suf == '.pdf':
                return pdf_extract_text(str(p))
            if suf == '.docx':
                doc = docx.Document(str(p))
                return '\n'.join([para.text for para in doc.paragraphs])
        except Exception:
            return ''
        return ''

    def _chunk_text(self, text):
        text = text.strip()
        if not text:
            return []
        chunks = []
        i=0
        while i<len(text):
            chunks.append(text[i:i+CHUNK_SIZE])
            i+=CHUNK_SIZE
        return chunks

    def process_documents(self, paths):
        to_upsert = []
        for p in paths:
            txt = self._read_text(p)
            self.index[os.path.basename(p)] = txt
            chunks = self._chunk_text(txt)
            for i,c in enumerate(chunks):
                to_upsert.append({'id': str(uuid.uuid4()), 'file': os.path.basename(p), 'chunk': i, 'text': c})
        if self.vector_store and to_upsert:
            self.vector_store.upsert(to_upsert)

    def search(self, query, top_k=5):
        if self.vector_store:
            return self.vector_store.search(query, top_k=top_k)
        # fallback naive search
        res = []
        q = query.lower()
        for f,t in self.index.items():
            if q in t.lower():
                res.append({'file': f, 'snippet': t[:400]})
        return res

import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="data/chroma_db")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection(name="documents")

    # MODIFIÉ: La fonction accepte maintenant une liste de dictionnaires
    def add_document_chunks(self, doc_id: int, chunks: List[Dict]):
        if not chunks:
            return

        texts = [chunk["text"] for chunk in chunks]
        embeddings = self.embedding_model.encode(texts)
        
        # MODIFIÉ: Les métadonnées incluent maintenant le numéro de page
        metadatas = []
        for i, chunk in enumerate(chunks):
            meta = chunk["metadata"]
            meta["document_id"] = doc_id
            meta["chunk_index"] = i
            metadatas.append(meta)
            
        ids = [f"doc_{doc_id}_chunk_{i}" for i, _ in enumerate(chunks)]

        self.collection.add(
            embeddings=embeddings,
            metadatas=metadatas,
            documents=texts,
            ids=ids
        )
        print(f"Ajout de {len(chunks)} chunks pour le document {doc_id} à ChromaDB.")

    # MODIFIÉ: La fonction retourne maintenant les documents ET leurs métadonnées
    def find_similar_chunks(self, question: str, n_results: int = 3) -> Dict:
        """Trouve les chunks pertinents et retourne leur contenu et métadonnées."""
        query_embedding = self.embedding_model.encode(question)
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results,
            include=["documents", "metadatas"] # On demande explicitement les métadonnées
        )
        
        return results
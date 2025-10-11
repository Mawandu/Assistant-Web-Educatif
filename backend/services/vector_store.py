import chromadb
from sentence_transformers import SentenceTransformer
from typing import List, Dict

class VectorStore:
    def __init__(self):
        self.client = chromadb.PersistentClient(path="data/chroma_db")
        
        self.embedding_model = SentenceTransformer('intfloat/multilingual-e5-large')
        
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"} 
        )

    def add_document_chunks(self, doc_id: int, chunks: List[Dict]):
        if not chunks:
            return

        texts = [chunk["text"] for chunk in chunks]
        prefixed_texts = [f"passage: {text}" for text in texts]
        embeddings = self.embedding_model.encode(prefixed_texts, normalize_embeddings=True)
        
        metadatas = []
        for i, chunk in enumerate(chunks):
            meta = chunk["metadata"].copy()
            meta["document_id"] = doc_id
            meta["chunk_index"] = i
            metadatas.append(meta)
            
        ids = [f"doc_{doc_id}_chunk_{i}" for i, _ in enumerate(chunks)]

        self.collection.add(
            embeddings=embeddings.tolist(),
            metadatas=metadatas,
            documents=texts,  
            ids=ids
        )
        print(f"✅ Ajout de {len(chunks)} chunks pour le document {doc_id} à ChromaDB.")

    def find_similar_chunks(self, question: str, n_results: int = 5) -> Dict:
        """Trouve les chunks pertinents et retourne leur contenu et métadonnées."""
        
        prefixed_question = f"query: {question}"
        query_embedding = self.embedding_model.encode(prefixed_question, normalize_embeddings=True)
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]  
        )
        
        if results.get("distances"):
            distances = results["distances"][0]
            print(f"\n📊 Scores de similarité pour '{question}':")
            for i, dist in enumerate(distances[:3]):
                similarity = 1 - dist  
                print(f"  Chunk {i+1}: {similarity:.3f}")
        
        return results
import chromadb
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self):
        # ... (le début de la classe ne change pas)
        self.client = chromadb.PersistentClient(path="data/chroma_db")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.collection = self.client.get_or_create_collection(name="documents")

    def add_document_chunks(self, doc_id: int, chunks: list[str]):
        # ... (cette fonction ne change pas)
        if not chunks:
            return

        embeddings = self.embedding_model.encode(chunks)
        metadatas = [{"document_id": doc_id, "chunk_index": i} for i, _ in enumerate(chunks)]
        ids = [f"doc_{doc_id}_chunk_{i}" for i, _ in enumerate(chunks)]

        self.collection.add(
            embeddings=embeddings,
            metadatas=metadatas,
            documents=chunks,
            ids=ids
        )
        print(f"Ajout de {len(chunks)} chunks pour le document {doc_id} à ChromaDB.")

    # === AJOUTEZ CETTE NOUVELLE FONCTION CI-DESSOUS ===
    def find_similar_chunks(self, question: str, n_results: int = 3) -> list[str]:
        """
        Trouve les morceaux de texte les plus pertinents pour une question donnée.
        """
        # Transforme la question en vecteur.
        query_embedding = self.embedding_model.encode(question)

        # Interroge la collection ChromaDB.
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=n_results
        )

        # Retourne uniquement le texte des documents trouvés.
        return results['documents'][0]

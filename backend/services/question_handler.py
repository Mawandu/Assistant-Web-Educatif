from backend.services.vector_store import VectorStore
from backend.services.ollama_client import generate_response

class QuestionHandler:
    def __init__(self):
        self.vector_store = VectorStore()

    def get_answer(self, question: str):
        # 1. Trouver les chunks pertinents avec leurs métadonnées
        search_results = self.vector_store.find_similar_chunks(question)

        # Extraire le contexte et les sources
        context_texts = search_results["documents"][0]
        sources_metadata = search_results["metadatas"][0]
        
        context = "\n---\n".join(context_texts)

        # 2. Générer une réponse en utilisant le contexte
        answer = generate_response(question, context)

        # 3. Formater les sources pour la réponse finale
        sources = []
        for meta in sources_metadata:
            sources.append({
                "document_id": meta.get("document_id"),
                "page": meta.get("page")
            })

        return {
            "question": question,
            "answer": answer,
            "sources": sources
        }
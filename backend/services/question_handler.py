# backend/services/question_handler.py

from backend.services.vector_store import VectorStore
from backend.services.ollama_client import generate_response
from backend.services.cache_manager import CacheManager 

class QuestionHandler:
    def __init__(self):
        self.vector_store = VectorStore()
        self.cache = CacheManager() 

    def get_answer(self, question: str):
        cached_answer = self.cache.get(question)
        if cached_answer:
            print(f"Réponse trouvée dans le cache pour : '{question}'")
            return {**cached_answer, "cached": True}
        print(f"Réponse non trouvée dans le cache pour : '{question}'. Génération en cours...")
        search_results = self.vector_store.find_similar_chunks(question)
        context_texts = search_results["documents"][0]
        sources_metadata = search_results["metadatas"][0]       
        context = "\n---\n".join(context_texts)
        answer = generate_response(question, context)
        sources = []
        for meta in sources_metadata:
            sources.append({
                "document_id": meta.get("document_id"),
                "page": meta.get("page")
            })
        final_response = {
            "question": question,
            "answer": answer,
            "sources": sources
        }
        self.cache.set(question, final_response)
        return {**final_response, "cached": False}
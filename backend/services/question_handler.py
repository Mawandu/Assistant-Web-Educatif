from sqlalchemy.orm import Session
from services.vector_store import VectorStore
from services.ollama_client import generate_response
from services.cache_manager import CacheManager
from models.document import Document 
class QuestionHandler:
    def __init__(self):
        self.vector_store = VectorStore()
        self.cache = CacheManager()

    def get_answer(self, question: str, db: Session):
        cached_answer = self.cache.get(question)
        if cached_answer:
            return {**cached_answer, "cached": True}

        search_results = self.vector_store.find_similar_chunks(question, n_results=5)
        
        if not search_results or not search_results.get("documents") or not search_results["documents"][0]:
             return {
                "question": question,
                "answer": "Désolé, je n'ai trouvé aucune information pertinente dans les documents fournis pour répondre à cette question.",
                "sources": [],
                "cached": False
            }

        context_texts = search_results["documents"][0]
        sources_metadata = search_results["metadatas"][0]
        context = "\n---\n".join(context_texts)
        
        answer = generate_response(question, context)

        doc_ids = {meta.get("document_id") for meta in sources_metadata if meta.get("document_id") is not None}
        documents = db.query(Document).filter(Document.id.in_(doc_ids)).all()
        doc_titles = {doc.id: doc.file_name for doc in documents}
        
        sources = []
        for meta in sources_metadata:
            doc_id = meta.get("document_id")
            sources.append({
                "document": doc_titles.get(doc_id, "Titre inconnu"), 
                "page": meta.get("page")
            })

        final_response = {
            "question": question,
            "answer": answer,
            "sources": sources
        }

        self.cache.set(question, final_response)
        return {**final_response, "cached": False}
from backend.services.vector_store import VectorStore
from backend.services.ollama_client import generate_response

class QuestionHandler:
    def __init__(self):
        self.vector_store = VectorStore()

    def get_answer(self, question: str):
        # 1. Find relevant context in the vector database
        context = self.vector_store.find_similar_chunks(question)

        # 2. Generate an answer using the context and the question
        answer = generate_response(question, context)

        return {
            "question": question,
            "answer": answer,
            "context": context
        }

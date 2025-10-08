# backend/services/ollama_client.py
import requests
import json
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def generate_response(question: str, context: str) -> str:
    """
    Génère une réponse en utilisant Ollama avec un contexte.
    """
    prompt = f"""
    En te basant uniquement sur le contexte suivant, réponds à la question.
    Contexte :
    ---
    {context}
    ---
    Question : {question}
    """
    
    try:
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": "mistral", 
                "prompt": prompt,
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()
        full_response = response.text.strip().split('\n')[-1]
        return json.loads(full_response).get("response", "Aucune réponse générée.")

    except requests.exceptions.RequestException as e:
        print(f"Error calling Ollama: {e}")
        return "Désolé, une erreur est survenue lors de la génération de la réponse."
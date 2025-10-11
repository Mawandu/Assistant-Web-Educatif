import requests
import json
import os

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

def generate_response(question: str, context: str) -> str:
    prompt = f"""Tu es un assistant éducatif spécialisé en Recherche Opérationnelle.

CONTEXTE DU DOCUMENT :
{context}

QUESTION DE L'ÉTUDIANT :
{question}

INSTRUCTIONS IMPORTANTES :
1. Réponds UNIQUEMENT en utilisant les informations du contexte ci-dessus
2. Si l'information n'existe PAS dans le contexte, réponds EXACTEMENT : "L'information n'est pas disponible dans le document fourni."
3. Sois précis, pédagogique et structuré
4. Utilise des exemples du contexte si disponibles
5. Ne cite JAMAIS d'informations externes au contexte

RÉPONSE :"""
    
    full_response_text = ""
    try:
        print(f"Envoi de la requête en streaming à Ollama sur l'hôte : {OLLAMA_HOST}")
        with requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": "mistral",  
                "prompt": prompt,
                "stream": True,
                "options": {
                    "temperature": 0.1,  
                    "num_predict": 500   
                }
            },
            stream=True,
            timeout=300
        ) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    try:
                        chunk = json.loads(line)
                        full_response_text += chunk.get("response", "")
                        if chunk.get("done"):
                            break
                    except json.JSONDecodeError:
                        print(f"Ligne JSON invalide reçue d'Ollama: {line}")
        
        print("Réponse complète reçue d'Ollama.")
        return full_response_text.strip()

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de l'appel à Ollama : {e}")
        return "Désolé, une erreur est survenue lors de la génération de la réponse."
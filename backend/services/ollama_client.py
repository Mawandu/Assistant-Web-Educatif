import requests
import json

def generate_response(question: str, context: list[str]):
    """
    Sends the question and context to the Ollama model and gets a response.
    """
    prompt = f"""
    En te basant uniquement sur le contexte suivant, réponds à la question.
    Si la réponse ne se trouve pas dans le contexte, dis "Je ne sais pas".

    Contexte:
    {" ".join(context)}

    Question: {question}
    """

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": prompt,
                "stream": False
            }
        )
        response.raise_for_status()
        return json.loads(response.text).get("response", "")
    except requests.RequestException as e:
        print(f"Error calling Ollama: {e}")
        return "Désolé, une erreur est survenue lors de la génération de la réponse."

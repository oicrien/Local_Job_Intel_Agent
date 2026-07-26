import requests
import json

def ollama_generate(model: str, prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt}
    )
    data = response.json()
    return data.get("response", "")

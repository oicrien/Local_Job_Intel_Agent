import requests
import json

def ollama_generate(model: str, prompt: str) -> str:
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt},
        stream=True
    )

    full_text = ""

    for line in response.iter_lines():
        if not line:
            continue
        try:
            obj = json.loads(line.decode("utf-8"))
            full_text += obj.get("response", "")
        except json.JSONDecodeError:
            # Ignore malformed lines
            continue

    return full_text

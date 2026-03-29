from config.env import (
    MODEL_PROVIDER,
    MODEL,
    GEMINI_API_KEY,
    OLLAMA_BASE_URL,
)
from config.prompt import prompt


def _get_gemini_client():
    """Returns the Gemini client for model interactions."""
    from google import genai
    return genai.Client(api_key=GEMINI_API_KEY)


def _get_ollama_client():
    """Returns the Ollama client for model interactions."""
    from ollama import Client
    return Client(host=OLLAMA_BASE_URL)


async def ask_ai(message: str):
    """
    Generate a response from the configured AI model.
    
    Supports:
    - 'ollama': Local or remote Ollama (e.g., qwen3, qwen3-vl, llama3.2)
    - 'gemini': Google Gemini API
    """
    provider = MODEL_PROVIDER.lower()
    
    if provider == 'ollama':
        return _ask_ollama(message)
    elif provider == 'gemini':
        return _ask_gemini(message)
    else:
        raise ValueError(f"Unknown MODEL_PROVIDER: {provider}. Must be 'ollama' or 'gemini'.")


def _ask_gemini(message: str):
    """Generate response using Google Gemini API."""
    client = _get_gemini_client()
    
    class GeminiChunk:
        def __init__(self, text):
            self.text = text
    
    response_stream = client.models.generate_content_stream(
        model=MODEL,
        contents=message,
        config={
            'system_instruction': prompt,
        }
    )
    
    def gemini_generator():
        for chunk in response_stream:
            if chunk.text:
                yield GeminiChunk(chunk.text)
    
    return gemini_generator()


def _ask_ollama(message: str):
    """Generate response using Ollama API."""
    client = _get_ollama_client()
    
    class OllamaChunk:
        def __init__(self, text):
            self.text = text
    
    response = client.chat(
        model=MODEL,
        messages=[
            {'role': 'system', 'content': prompt},
            {'role': 'user', 'content': message},
        ],
        stream=True,
    )
    
    def ollama_generator():
        for chunk in response:
            content = chunk.get('message', {}).get('content', '')
            if content:
                yield OllamaChunk(content)
    
    return ollama_generator()

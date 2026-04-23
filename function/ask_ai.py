from config.env import (
    MODEL_PROVIDER,
    MODEL,
    GEMINI_API_KEY,
    OLLAMA_BASE_URL,
    OPENAI_API_KEY,
    OPENAI_BASE_URL,
)
from config.prompt import prompt
import base64


def _get_openai_client():
    """Returns the OpenAI-compatible client for model interactions."""
    from openai import AsyncOpenAI
    return AsyncOpenAI(
        base_url=OPENAI_BASE_URL,
        api_key=OPENAI_API_KEY,
    )


def _get_gemini_client():
    """Returns the Gemini client for model interactions."""
    from google import genai
    return genai.Client(api_key=GEMINI_API_KEY)


def _get_ollama_client():
    """Returns the Ollama client for model interactions."""
    from ollama import Client
    return Client(host=OLLAMA_BASE_URL)


def _get_ollama_async_client():
    """Returns the Ollama async client for model interactions."""
    from ollama import AsyncClient
    return AsyncClient(host=OLLAMA_BASE_URL)


async def ask_ai(message: str, image: bytes = None):
    """
    Generate a response from the configured AI model.

    Supports:
    - 'ollama': Local or remote Ollama (e.g., qwen3, qwen3-vl, llama3.2)
    - 'gemini': Google Gemini API
    - 'openai': OpenAI-compatible API (e.g., OpenRouter, DeepSeek)
    
    Yields chunks asynchronously as they arrive.
    """
    provider = MODEL_PROVIDER.lower()

    if provider == 'ollama':
        async for chunk in _ask_ollama(message, image):
            yield chunk
    elif provider == 'gemini':
        async for chunk in _ask_gemini(message, image):
            yield chunk
    elif provider == 'openai' or provider == 'openrouter':
        async for chunk in _ask_openai(message, image):
            yield chunk
    else:
        raise ValueError(f"Unknown MODEL_PROVIDER: {provider}. Must be 'ollama', 'gemini', or 'openai'.")


async def _ask_openai(message: str, image: bytes = None):
    """Generate response using OpenAI-compatible API."""
    client = _get_openai_client()

    class OpenAIChunk:
        def __init__(self, text):
            self.text = text

    messages = [
        {"role": "system", "content": prompt},
    ]

    if image:
        base64_image = base64.b64encode(image).decode('utf-8')
        user_content = [
            {"type": "text", "text": message},
            {
                "type": "image_url",
                "image_url": {
                    "url": f"data:image/jpeg;base64,{base64_image}"
                }
            }
        ]
        messages.append({"role": "user", "content": user_content})
    else:
        messages.append({"role": "user", "content": message})

    response = await client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
    )

    async for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            yield OpenAIChunk(chunk.choices[0].delta.content)


async def _ask_gemini(message: str, image: bytes = None):
    """Generate response using Google Gemini API."""
    from google.genai import types
    client = _get_gemini_client()

    class GeminiChunk:
        def __init__(self, text):
            self.text = text

    contents = [message]
    if image:
        contents.append(types.Part.from_bytes(data=image, mime_type="image/jpeg"))

    response_stream = client.models.generate_content_stream(
        model=MODEL,
        contents=contents,
        config={
            'system_instruction': prompt,
        }
    )

    for chunk in response_stream:
        if chunk.text:
            yield GeminiChunk(chunk.text)


async def _ask_ollama(message: str, image: bytes = None):
    """Generate response using Ollama API (async streaming)."""
    client = _get_ollama_async_client()

    class OllamaChunk:
        def __init__(self, text):
            self.text = text

    user_message = {'role': 'user', 'content': message}
    if image:
        user_message['images'] = [image]

    stream = await client.chat(
        model=MODEL,
        messages=[
            {'role': 'system', 'content': prompt},
            user_message,
        ],
        stream=True,
    )

    async for response in stream:
        content = response.get('message', {}).get('content', '')
        if content:
            yield OllamaChunk(content)

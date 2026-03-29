from google import genai
from config.env import BRIAN_CORE_API_KEY, MODEL
from config.prompt import prompt

client = genai.Client(api_key=BRIAN_CORE_API_KEY)

async def ask_ai(message: str):
    # Using the new google-genai client
    response = client.models.generate_content(
        model=MODEL,
        contents=message,
        config={
            'system_instruction': prompt,
        }
    )
    # The new client doesn't return a stream by default in this simple call, 
    # but we can simulate the iteration if needed. 
    # For a simple response, we can just return a list with one item or use generate_content_stream.
    
    # Let's use stream for compatibility with main.py logic:
    response_stream = client.models.generate_content_stream(
        model=MODEL,
        contents=message,
        config={
            'system_instruction': prompt,
        }
    )
    return response_stream

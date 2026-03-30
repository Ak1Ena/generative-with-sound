import io
from PIL import ImageGrab

def capture_screen():
    """
    Capture the current screen and return the image data as bytes.
    """
    try:
        # Capture the entire primary monitor
        screenshot = ImageGrab.grab()
        
        # Save to bytes buffer
        buffer = io.BytesIO()
        # Save as JPEG to reduce data size (Gemini and Ollama support it)
        screenshot.save(buffer, format="JPEG", quality=80)
        
        return buffer.getvalue()
    except Exception as e:
        print(f"Error capturing screen: {e}")
        return None

async def see_action(args, callback):
    """
    Action handler for 'see'.
    Args:
        args (dict): Parsed arguments from the AI, e.g., {'prompt': '...'}
        callback (function): The interaction function to call with the result.
    """
    prompt = args.get('prompt', "This is my current screen. Please tell me what you see.")
    print(f"--- Action: see, Prompt: {prompt} ---")
    
    img_bytes = capture_screen()
    if img_bytes:
        # Call the callback (process_interaction) with the follow-up prompt and image
        await callback(prompt, img_bytes)
    else:
        print("Failed to capture screen.")

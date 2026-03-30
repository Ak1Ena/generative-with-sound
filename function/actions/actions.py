import importlib
from function.actions.capture_screen import capture_screen

async def handle_see(args, callback):
    """
    Action: see
    Args: {'prompt': '...'}
    """
    prompt = args.get('prompt', "This is my current screen. Please tell me what you see.")
    print(f"--- Action: see, Prompt: {prompt} ---")
    img_bytes = capture_screen()
    if img_bytes:
        # We call the callback (process_interaction) with the result
        await callback(prompt, img_bytes)
    else:
        print("Failed to capture screen.")

async def handle_click(args, callback):
    """
    Action: click
    Args: {'x': number, 'y': number}
    """
    x = args.get('x')
    y = args.get('y')
    print(f"--- Action: click at ({x}, {y}) ---")
    # Here you would use something like pyautogui or similar to click
    # For now, we'll just acknowledge it
    await callback(f"I've clicked at coordinates {x}, {y}.", None)

def get_handler(location, function_name):
    """Dynamically import and return the handler function."""
    try:
        module = importlib.import_module(location)
        return getattr(module, function_name)
    except Exception as e:
        print(f"Error loading handler {function_name} from {location}: {e}")
        return None

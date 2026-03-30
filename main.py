import asyncio
import time
import re
import json
import os
import importlib
from function.ask_ai import ask_ai
from function.speak import speak, preload_models
import config.env as env

# Load action map for internal use
ACTION_MAP = {}
action_path = os.path.join(os.path.dirname(__file__), "action.json")
if os.path.exists(action_path):
    with open(action_path, "r") as f:
        action_data = json.load(f)
        for act in action_data:
            ACTION_MAP[act["name"]] = act

# Regex to find complete sentences (ends with punctuation + space or end)
SENTENCE_PATTERN = re.compile(r'(.+?[.!?]\s+)|(.+?[.!?]$)', re.DOTALL)
# Regex to find actions like [**action_name<arg1=val1,arg2=val2>**]
ACTION_EXTRACTOR = re.compile(r'\[\*\*(?P<name>\w+)(?:<(?P<args>.*?)>)?\*\*\]')
# Regex to remove actions from text
ACTION_CLEANER = re.compile(r'\[\*\*.*?\*\*\]')

def parse_args(args_str):
    """Parse string like 'x=4,y=1' into {'x': '4', 'y': '1'}."""
    if not args_str:
        return {}
    
    args = {}
    pairs = args_str.split(',')
    for pair in pairs:
        if '=' in pair:
            key, val = pair.split('=', 1)
            args[key.strip()] = val.strip()
    return args

def get_action_handler(location, function_name):
    """Dynamically import and return the handler function."""
    try:
        module = importlib.import_module(location)
        return getattr(module, function_name)
    except Exception as e:
        return None

async def speak_worker(queue):
    """Background task that speaks text from the queue."""
    while True:
        text = await queue.get()
        if text is None:
            break
        await speak(text)
        queue.task_done()

async def process_interaction(message, image=None, is_follow_up=False):
    """
    Handle a single interaction with the AI.
    is_follow_up: set to True if this call is the result of an action.
    """
    if not is_follow_up:
        print(f"AI: ", end="", flush=True)
    
    full_response = ""
    text_queue = asyncio.Queue()
    speak_task = asyncio.create_task(speak_worker(text_queue))

    try:
        chunk_buffer = ""
        async for chunk in ask_ai(message, image):
            if chunk.text:
                chunk_buffer += chunk.text
                full_response += chunk.text

                # Find complete sentences in buffer
                matches = list(SENTENCE_PATTERN.finditer(chunk_buffer))
                if len(matches) > 1:
                    for match in matches[:-1]:
                        sentence = match.group().strip()
                        if sentence:
                            # Clean sentence (remove tags) for both printing and speaking
                            clean_sentence = ACTION_CLEANER.sub("", sentence).strip()
                            
                            # 1. Handle terminal printing (only for top-level interaction)
                            if not is_follow_up and clean_sentence:
                                print(clean_sentence, end=" ", flush=True)

                            # 2. Handle TTS speaking: Speak the cleaned version of the sentence
                            # only if there is actual text left after removing the action.
                            if clean_sentence:
                                text_queue.put_nowait(clean_sentence)
                    
                    last_end = matches[-1].end()
                    chunk_buffer = chunk_buffer[last_end:]

        # Handle remaining buffer
        if chunk_buffer.strip():
            clean_sentence = ACTION_CLEANER.sub("", chunk_buffer).strip()
            if not is_follow_up and clean_sentence:
                print(clean_sentence, end="", flush=True)
            
            if clean_sentence:
                text_queue.put_nowait(clean_sentence)

        if not is_follow_up:
            print() 
        
        await text_queue.join()
        
    finally:
        text_queue.put_nowait(None)
        await speak_task

    # Only process actions from the TOP-LEVEL response to avoid loops
    if not is_follow_up:
        found_actions = list(ACTION_EXTRACTOR.finditer(full_response))
        for match in found_actions:
            name = match.group('name')
            args = parse_args(match.group('args'))
            
            if name in ACTION_MAP:
                action_config = ACTION_MAP[name]
                handler = get_action_handler(action_config["location"], action_config["function"])
                if handler:
                    async def follow_up_callback(msg, img):
                        await process_interaction(msg, img, is_follow_up=True)
                    
                    await handler(args, follow_up_callback)

async def main():
    print("RinneAI (Python Only)")
    preload_models()

    print("\n" + "="*30)
    print(f"System ready using {env.TTS_PROVIDER}. Type something:")
    print("="*30)

    while True:
        try:
            user_input = input("User: ").strip()
            if user_input.lower() == "exit":
                break
            if not user_input:
                continue

            start_time = time.perf_counter()
            try:
                await process_interaction(user_input)
            except Exception as e:
                print(f"Error: {e}")
            finally:
                end_time = time.perf_counter()
                print(f"Time: {end_time - start_time:.2f}s")

        except (EOFError, KeyboardInterrupt):
            break

if __name__ == "__main__":
    asyncio.run(main())

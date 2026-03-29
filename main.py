import asyncio
import time
import re
from function.ask_ai import ask_ai
from function.speak import speak, preload_models
import config.env as env

# Regex to find complete sentences (ends with punctuation + space or end)
SENTENCE_PATTERN = re.compile(r'(.+?[.!?]\s+)|(.+?[.!?]$)', re.DOTALL)

async def speak_worker(queue):
    """Background task that speaks text from the queue."""
    while True:
        text = await queue.get()
        if text is None:  # Poison pill to stop
            break
        await speak(text)
        queue.task_done()

async def main():
    print("RinneAI (Python Only)")

    # Pre-download and load models based on .env
    preload_models()

    print("\n" + "="*30)
    print(f"System ready using {env.TTS_PROVIDER}. Type something (or 'exit'):")
    print("="*30)

    while True:
        try:
            user_input = input("User: ").strip()

            if user_input.lower() == "exit":
                print("Bye!")
                break

            if not user_input:
                continue

            start_time = time.perf_counter()
            try:
                # Create a queue for non-blocking TTS
                text_queue = asyncio.Queue()
                speak_task = asyncio.create_task(speak_worker(text_queue))

                # Stream chunks with smart buffering for natural speech
                chunk_buffer = ""
                async for chunk in ask_ai(user_input):
                    if chunk.text:
                        chunk_buffer += chunk.text

                        # Find complete sentences in buffer
                        matches = list(SENTENCE_PATTERN.finditer(chunk_buffer))
                        if len(matches) > 1:
                            # Speak all complete sentences except the last (potentially incomplete) part
                            for match in matches[:-1]:
                                sentence = match.group().strip()
                                if sentence:
                                    text_queue.put_nowait(sentence)
                            # Keep remaining text in buffer
                            last_end = matches[-1].end()
                            chunk_buffer = chunk_buffer[last_end:]

                # Speak remaining buffer
                if chunk_buffer.strip():
                    text_queue.put_nowait(chunk_buffer.strip())

                # Wait for all text to be spoken
                await text_queue.join()

                # Stop the worker
                text_queue.put_nowait(None)
                await speak_task

            except Exception as e:
                print(f"Error during AI interaction: {e}")
            finally:
                end_time = time.perf_counter()
                print(f"Conversation took {end_time - start_time:.2f}s")

        except EOFError:
            break
        except KeyboardInterrupt:
            print("\nExiting...")
            break

if __name__ == "__main__":
    asyncio.run(main())

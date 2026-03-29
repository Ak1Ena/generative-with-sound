import asyncio
import time
import re
from function.ask_ai import ask_ai
from function.speak import speak, preload_models
import config.env as env

def split_into_sentences(text):
    """Splits text into sentences based on punctuation (., !, ?)."""
    # This regex looks for sentence-ending punctuation followed by a space or end of string
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

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
                response_stream = await ask_ai(user_input)
                
                full_response = ""
                sentence_buffer = ""
                
                for chunk in response_stream:
                    if chunk.text:
                        chunk_text = chunk.text
                        full_response += chunk_text
                        sentence_buffer += chunk_text
                        
                        # Check if we have a complete sentence in the buffer
                        # (Ending with . ! or ?)
                        if any(char in sentence_buffer for char in ".!?"):
                            # Extract complete sentences from the buffer
                            parts = re.split(r'(?<=[.!?])\s+', sentence_buffer)
                            
                            # If we have more than one part, the first parts are definitely complete
                            if len(parts) > 1:
                                for i in range(len(parts) - 1):
                                    sentence = parts[i].strip()
                                    if sentence:
                                        await speak(sentence)
                                
                                # The last part remains in the buffer (might be incomplete)
                                sentence_buffer = parts[-1]
                
                # Speak any remaining text in the buffer after stream ends
                if sentence_buffer.strip():
                    await speak(sentence_buffer.strip())
                
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

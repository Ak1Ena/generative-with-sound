import os
import subprocess
import asyncio
import io
from elevenlabs import ElevenLabs
import config.env as env

# Global instances
elevenlabs_instance = None
local_tts_instance = None

def get_elevenlabs_client():
    global elevenlabs_instance
    if elevenlabs_instance is None:
        if env.VOICE_CORE_API_KEY:
            elevenlabs_instance = ElevenLabs(api_key=env.VOICE_CORE_API_KEY)
        else:
            print("Warning: ElevenLabs API Key is missing.")
    return elevenlabs_instance

def get_local_tts_model():
    """Only imports AI libraries when Qwen is actually used."""
    global local_tts_instance
    if local_tts_instance is None:
        try:
            import torch
            from huggingface_hub import snapshot_download
            from qwen_tts import Qwen3TTSModel

            print(f"Checking/Downloading model from Hugging Face ({env.LOCAL_TTS_MODEL_ID})...")
            model_dir = snapshot_download(repo_id=env.LOCAL_TTS_MODEL_ID)
            
            print(f"Loading Qwen3-TTS (1.7B) onto CPU...")
            local_tts_instance = Qwen3TTSModel.from_pretrained(
                model_dir, 
                device_map=None,
                dtype=torch.float32
            )
            print("Qwen3-TTS model loaded and ready.")
                
        except ImportError as e:
            print(f"Error: {e}")
            print("Hint: Make sure 'huggingface_hub', 'qwen-tts', 'torch' are installed.")
        except Exception as e:
            print(f"Error loading local TTS: {e}")
    return local_tts_instance

def play_audio_with_ffplay(audio_data):
    """Plays audio data (bytes) by piping it to ffplay via stdin."""
    try:
        ffplay_command = ["ffplay", "-nodisp", "-autoexit", "-hide_banner", "-i", "pipe:0"]
        process = subprocess.Popen(
            ffplay_command,
            stdin=subprocess.PIPE,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        process.communicate(input=audio_data)
    except FileNotFoundError:
        print("Error: 'ffplay' not found. Please install ffmpeg.")
    except Exception as e:
        print(f"Error playing audio with ffplay: {e}")

def preload_models():
    """Only preloads if selected in env."""
    if env.TTS_PROVIDER == 'qwen-tts' or env.TTS_PROVIDER == 'local':
        get_local_tts_model()
    elif env.TTS_PROVIDER == 'elevenlabs':
        get_elevenlabs_client()

async def speak(message: str):
    if not message.strip():
        return
        
    print(f"Speaking ({env.TTS_PROVIDER}): {message}")
    
    if env.TTS_PROVIDER == 'elevenlabs':
        client = get_elevenlabs_client()
        if client:
            try:
                audio_stream = client.text_to_speech.convert(
                    voice_id=env.VOICE_ID,
                    text=message,
                    model_id=env.VOICE_MODEL,
                    output_format="mp3_44100_128",
                )
                audio_data = b"".join(audio_stream)
                play_audio_with_ffplay(audio_data)
            except Exception as e:
                print(f"ElevenLabs Error: {e}")
                
    elif env.TTS_PROVIDER == 'qwen-tts' or env.TTS_PROVIDER == 'local':
        model = get_local_tts_model()
        if model:
            try:
                import torch
                import soundfile as sf
                # Use Qwen3 VoiceDesign logic
                print(f"Generating audio for: '{message}'...")
                wavs, sr = model.generate_voice_design(
                    text=message,
                    language=env.TTS_LANGUAGE,
                    instruct=env.TTS_VOICE_INSTRUCT
                )
                # Convert wav array to bytes
                buffer = io.BytesIO()
                sf.write(buffer, wavs[0], sr, format='WAV')
                audio_data = buffer.getvalue()
                play_audio_with_ffplay(audio_data)
            except Exception as e:
                print(f"Local TTS Error: {e}")
        else:
            print("Local TTS model not available.")
    else:
        print(f"Unknown TTS Provider: {env.TTS_PROVIDER}. Just printing message.")
        print(message)

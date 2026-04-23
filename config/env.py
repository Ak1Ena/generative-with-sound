import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ===========================================
# Model Provider Configuration
# ===========================================

# Model Provider: 'ollama', 'gemini', or 'openai'
MODEL_PROVIDER = os.getenv('MODEL_PROVIDER', 'ollama')

# Model name based on provider
# - Ollama: qwen3, qwen3-vl:235b-cloud, llama3.2, mistral, etc.
# - Gemini: gemini-2.0-flash, gemini-1.5-pro, etc.
# - OpenAI Compatible: google/gemini-2.0-flash-exp:free, openai/gpt-4o, etc.
MODEL = os.getenv('MODEL', 'qwen3')

# ===========================================
# Gemini API Configuration
# ===========================================
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# Legacy support for BRIAN_CORE_API_KEY
if not GEMINI_API_KEY:
    GEMINI_API_KEY = os.getenv('BRIAN_CORE_API_KEY', '')

# ===========================================
# OpenAI Compatible Configuration (OpenRouter, DeepSeek, etc.)
# ===========================================
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
OPENAI_BASE_URL = os.getenv('OPENAI_BASE_URL', 'https://openrouter.ai/api/v1')

# ===========================================
# Ollama Configuration
# ===========================================
# Default: http://localhost:11434 (only change if Ollama runs elsewhere)
OLLAMA_BASE_URL = os.getenv('OLLAMA_BASE_URL', 'http://localhost:11434')

# ===========================================
# TTS Configuration
# ===========================================

# TTS Provider Selection ('elevenlabs' or 'qwen-tts')
TTS_PROVIDER = os.getenv('TTS_PROVIDER', 'qwen-tts')

# Local TTS Configuration
LOCAL_TTS_MODEL_ID = os.getenv('LOCAL_TTS_MODEL_ID', 'Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign')
TTS_LANGUAGE = os.getenv('TTS_LANGUAGE', 'English')
TTS_VOICE_INSTRUCT = os.getenv('TTS_VOICE_INSTRUCT', 'A deep, resonant male voice speaking with a calm and authoritative tone.')

# ===========================================
# ElevenLabs Configuration
# ===========================================
VOICE_CORE_API_KEY = os.getenv('VOICE_CORE_API_KEY', '')
VOICE_ID = os.getenv('VOICE_ID', 'TxGi1N29NQoCaYD4fcU5')
VOICE_MODEL = os.getenv('VOICE_MODEL', 'eleven_v3')

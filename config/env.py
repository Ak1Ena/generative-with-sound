import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 1. AI Configuration (Gemini)
BRIAN_CORE_API_KEY = os.getenv('BRIAN_CORE_API_KEY', '')
MODEL = os.getenv('MODEL', 'gemini-2.0-flash')

# 2. TTS Provider Selection ('elevenlabs' or 'qwen-tts')
TTS_PROVIDER = os.getenv('TTS_PROVIDER', 'qwen-tts')

# 3. Local TTS Configuration (Qwen3-1.7B for Instructions)
LOCAL_TTS_MODEL_ID = os.getenv('LOCAL_TTS_MODEL_ID', 'Qwen/Qwen3-TTS-12Hz-1.7B-VoiceDesign')
TTS_LANGUAGE = os.getenv('TTS_LANGUAGE', 'English')
# Describe the voice here!
TTS_VOICE_INSTRUCT = os.getenv('TTS_VOICE_INSTRUCT', 'A deep, resonant male voice speaking with a calm and authoritative tone.')

# 4. ElevenLabs Configuration
VOICE_CORE_API_KEY = os.getenv('VOICE_CORE_API_KEY', '')
VOICE_ID = os.getenv('VOICE_ID', 'TxGi1N29NQoCaYD4fcU5')
VOICE_MODEL = os.getenv('VOICE_MODEL', 'eleven_v3')

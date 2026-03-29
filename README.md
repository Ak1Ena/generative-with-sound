# RinneAI (Python Only)

This is a Python-only project for AI Chat with Text-to-Speech.

## Features
- AI Chat using Google GenAI (Gemini)
- Text-to-Speech (TTS) with support for:
  - **ElevenLabs** (Cloud-based)
  - **Qwen-TTS / Sambert** (**Local-based** via ModelScope)
- User-selectable TTS provider via `.env`.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *Note: Local TTS requires `torch` and `modelscope`, which are included in requirements.txt.*

2. Configure environment variables in `.env`:
   - Copy `.env.example` to `.env`.
   - Fill in your API keys for Google GenAI and ElevenLabs (if using it).
   - Set `TTS_PROVIDER` to `elevenlabs` or `qwen-tts`.

3. **Mandatory Requirement: FFmpeg**
   Ensure `ffplay` is installed and available in your PATH. Audio is piped directly to `ffplay` for playback.

## Running

```bash
python main.py
```
*Note: The first time you run with `qwen-tts`, it will download the model files (~GBs).*

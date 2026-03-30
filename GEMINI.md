# RinneAI - Project Context

RinneAI is a Python-based AI chat application featuring streaming Text-to-Speech (TTS). It supports both cloud-based and local AI/TTS providers.

## Project Overview

- **Purpose**: Interactive AI chat with natural voice feedback.
- **Core Technologies**: 
  - **Languages**: Python
  - **AI Models**: Google Gemini API, Ollama (Local)
  - **TTS Providers**: ElevenLabs (Cloud), Qwen-TTS (Local via ModelScope)
  - **Audio Engine**: FFmpeg (`ffplay`) for real-time audio playback.
- **Architecture**: Asynchronous streaming. The chat loop uses `asyncio` to stream AI responses chunk by chunk, buffering them into sentences, and passing them to a background worker for sequential TTS generation and playback.

## Directory Structure

- `main.py`: The primary entry point. Orchestrates the chat loop, AI streaming, and background TTS processing.
- `run.py`: Simple wrapper to execute `main.py`.
- `config/`:
    - `env.py`: Manages environment variables and application settings.
    - `prompt.py`: Contains the system instructions/persona for the AI.
- `function/`:
    - `ask_ai.py`: Handles communication with Gemini and Ollama.
    - `speak.py`: Manages TTS generation (ElevenLabs or Qwen) and playback via `ffplay`.
- `kokoro_models/`: Local storage for downloaded TTS models (if applicable).
- `.env.example`: Template for required API keys and configuration.

## Setup and Commands

### Prerequisites
- **Python 3.10+**
- **FFmpeg**: Must have `ffplay` installed and available in the system PATH.

### Installation
```bash
pip install -r requirements.txt
```
*Note: The requirements include a specific index for CPU-only PyTorch to ensure stability on Windows systems.*

### Configuration
1. Copy `.env.example` to `.env`.
2. Configure `MODEL_PROVIDER` (`gemini` or `ollama`) and `TTS_PROVIDER` (`elevenlabs` or `qwen-tts`).
3. Provide necessary API keys (`GEMINI_API_KEY`, `VOICE_CORE_API_KEY`).

### Running
```bash
python main.py
```

## Development Conventions

- **Asynchronous Execution**: The project relies heavily on `asyncio` for non-blocking I/O (streaming AI text and background TTS).
- **Environment Driven**: Feature toggles (Provider selection) are controlled strictly via environment variables in `config/env.py`.
- **Modular Functions**: AI logic is separated into `ask_ai.py` and speech logic into `speak.py` to allow for easy extension of new providers.
- **Dependency Management**: Uses a flat `requirements.txt` with specific versioning for torch to avoid common installation issues on Windows.

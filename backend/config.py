# config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Configurations
    FLASK_ENV = os.getenv('FLASK_ENV', 'production')
    FLASK_DEBUG = os.getenv('FLASK_DEBUG', 'False') == 'True'
    PORT = int(os.getenv('PORT', 5000))
    
    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///diario.db')
    
    # Hugging Face API
    HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
    HUGGINGFACE_MODEL = os.getenv('HUGGINGFACE_MODEL', 'meta-llama/Llama-3.1-8B-Instruct')
    HUGGINGFACE_API_URL = f"https://api-inference.huggingface.co/models/{HUGGINGFACE_MODEL}"
    
    # ElevenLabs API (Opcional)
    ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
    ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID')
    ELEVENLABS_TTS_URL = f'https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}/stream' if os.getenv('ELEVENLABS_VOICE_ID') else None

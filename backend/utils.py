# utils.py

import requests
import base64
from config import Config
from models import DiarioEntry
from sqlalchemy.orm import Session
from datetime import datetime

def generate_diary_content():
    """
    Interactúa con la API de Hugging Face para generar el contenido de la entrada del diario.
    """
    try:
        headers = {
            "Authorization": f"Bearer {Config.HUGGINGFACE_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": {
                "role": "user",
                "content": "Genera una entrada de diario para el día de hoy. La entrada debe ser reflexiva, positiva y describir las actividades realizadas durante el día."
            },
            "parameters": {
                "max_new_tokens": 300,
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        response = requests.post(Config.HUGGINGFACE_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            # Ajusta esto según la estructura de la respuesta de Hugging Face
            return result.get('choices')[0].get('text').strip()
        else:
            print(f"Error en generación de diario: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Excepción en generación de diario: {e}")
        return None

def text_to_audio(texto):
    """
    Convierte el texto proporcionado en audio utilizando la API de ElevenLabs.
    """
    try:
        if not Config.ELEVENLABS_API_KEY or not Config.ELEVENLABS_VOICE_ID:
            print("ElevenLabs API Key o Voice ID no están configurados.")
            return None

        headers = {
            'xi-api-key': Config.ELEVENLABS_API_KEY,
            'Content-Type': 'application/json'
        }
        payload = {
            "text": texto,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.33,
                "similarity_boost": 0.75,
                "style": 0.48,
                "use_speaker_boost": "true"
            }
        }
        response = requests.post(Config.ELEVENLABS_TTS_URL, headers=headers, json=payload)
        if response.status_code == 200:
            # Leer el contenido binario del audio
            audio_content = response.content

            # Codificar el audio en base64
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')
            return audio_base64
        else:
            print(f"Error al generar el audio: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Excepción en conversión a audio: {e}")
        return None

def generate_and_store_diary(session: Session = None):
    """
    Genera contenido para el diario utilizando Hugging Face y opcionalmente convierte el texto en audio.
    Luego, almacena la entrada en la base de datos.
    """
    today = datetime.utcnow().date()

    # Crear una sesión si no se proporciona una
    close_session = False
    if not session:
        session = Session()
        close_session = True

    try:
        # Verificar si ya existe una entrada para hoy
        existing_entry = session.query(DiarioEntry).filter_by(date=today).first()
        if existing_entry:
            print("Ya existe una entrada para hoy.")
            return existing_entry

        # Generar contenido
        content = generate_diary_content()
        if not content:
            print("Error al generar el contenido de la entrada del diario.")
            return None

        # Crear descripción breve
        description = content.split('.')[0] + '.' if '.' in content else content

        # Convertir a audio (opcional)
        audio = text_to_audio(content) if Config.ELEVENLABS_API_KEY and Config.ELEVENLABS_VOICE_ID else None

        # Crear y almacenar la entrada
        new_entry = DiarioEntry(
            date=today,
            description=description,
            content=content,
            audio=audio
        )
        session.add(new_entry)
        session.commit()
        print("Entrada de diario generada y almacenada exitosamente.")
        return new_entry
    except Exception as e:
        if session:
            session.rollback()
        print(f"Error al generar y almacenar la entrada del diario: {e}")
        return None
    finally:
        if close_session:
            session.close()

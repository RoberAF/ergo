from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
import requests
import os
from dotenv import load_dotenv
import base64

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurar el cliente de Hugging Face
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
if not HUGGINGFACE_API_KEY:
    raise ValueError("La variable de entorno 'HUGGINGFACE_API_KEY' no está configurada.")
client = InferenceClient(token=HUGGINGFACE_API_KEY)

# Configurar la API de ElevenLabs
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID')
if not ELEVENLABS_API_KEY:
    raise ValueError("La variable de entorno 'ELEVENLABS_API_KEY' no está configurada.")
if not ELEVENLABS_VOICE_ID:
    raise ValueError("La variable de entorno 'ELEVENLABS_VOICE_ID' no está configurada.")
ELEVENLABS_TTS_URL = f'https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}/stream'

# Ruta para manejar mensajes de texto con contexto
@app.route('/message', methods=['POST'])
def handle_message():
    try:
        data = request.get_json()
        print("Datos recibidos:", data)  # Depuración

        user_messages = data.get('messages', [])

        if not user_messages:
            return jsonify({'reply': 'No se proporcionó ningún mensaje.'}), 400

        # Añadir el mensaje de sistema al inicio del historial
        system_message = {
            "role": "system",
            "content": "Finge ser una humana del país España y habla como una humana española lo haría, tienes una personalidad extrovertida, dulce y amigable, siempre vas disfrazada de dinosaurio. No generes acciones como por ejemplo *suspira*"
        }

        # Verificar si ya se ha añadido el mensaje de sistema para evitar duplicados
        if not user_messages or user_messages[0].get('role') != 'system':
            messages = [system_message] + user_messages
        else:
            messages = user_messages

        # Limitar el historial para evitar exceder el límite de tokens
        MAX_HISTORY = 20
        if len(messages) > MAX_HISTORY:
            messages = messages[-MAX_HISTORY:]

        # Generar respuesta con Hugging Face
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=messages,
            max_tokens=200
        )

        print("Respuesta completa del modelo:", completion)  # Depuración

        # Obtener la respuesta del modelo directamente
        bot_reply = completion['choices'][0]['message']['content']

        # Convertir el texto de respuesta en audio usando ElevenLabs
        elevenlabs_headers = {
            'xi-api-key': ELEVENLABS_API_KEY,
            'Content-Type': 'application/json'
        }

        elevenlabs_payload = {
            "text": bot_reply,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.33,
                "similarity_boost": 0.75,
                "style": 0.48,
                "use_speaker_boost": "true"
            }
        }

        # Hacer la solicitud a ElevenLabs
        tts_response = requests.post(ELEVENLABS_TTS_URL, headers=elevenlabs_headers, json=elevenlabs_payload)

        if tts_response.status_code == 200:
            # Leer el contenido binario del audio
            audio_content = tts_response.content

            # Codificar el audio en base64
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')

            # Devolver el texto y el audio codificado en base64
            return jsonify({'reply': bot_reply, 'audio': audio_base64})
        else:
            print(f"Error al generar el audio: {tts_response.status_code} - {tts_response.text}")
            # Devolver solo el texto en caso de error con el audio
            return jsonify({'reply': bot_reply, 'audio': None}), 500

    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return jsonify({'reply': 'Hubo un error al procesar tu solicitud.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

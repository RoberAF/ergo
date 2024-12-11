# app.py

from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
import requests
import os
from dotenv import load_dotenv
import base64
from PIL import Image
from io import BytesIO
from sqlalchemy import create_engine, Column, Integer, String, Date, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import atexit

# Configurar el logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s',
                    handlers=[
                        logging.FileHandler("diario_backend.log"),
                        logging.StreamHandler()
                    ])

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurar el cliente de Hugging Face para Chat
HUGGINGFACE_API_KEY = os.getenv('HUGGINGFACE_API_KEY')
if not HUGGINGFACE_API_KEY:
    raise ValueError("La variable de entorno 'HUGGINGFACE_API_KEY' no está configurada.")
client_chat = InferenceClient(token=HUGGINGFACE_API_KEY)

# Configurar el cliente de Hugging Face para Generación de Imágenes
IMAGE_GENERATION_API_KEY = HUGGINGFACE_API_KEY
if not IMAGE_GENERATION_API_KEY:
    raise ValueError("La variable de entorno 'IMAGE_GENERATION_API_KEY' no está configurada.")
client_image = InferenceClient(token=IMAGE_GENERATION_API_KEY)

# Configurar la API de ElevenLabs
ELEVENLABS_API_KEY = os.getenv('ELEVENLABS_API_KEY')
ELEVENLABS_VOICE_ID = os.getenv('ELEVENLABS_VOICE_ID')
if not ELEVENLABS_API_KEY:
    raise ValueError("La variable de entorno 'ELEVENLABS_API_KEY' no está configurada.")
if not ELEVENLABS_VOICE_ID:
    raise ValueError("La variable de entorno 'ELEVENLABS_VOICE_ID' no está configurada.")
ELEVENLABS_TTS_URL = f'https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}/stream'

# Configurar la base de datos
DATABASE_URL = 'sqlite:///diario.db'
engine = create_engine(DATABASE_URL)
Base = declarative_base()

class DiarioEntry(Base):
    __tablename__ = 'diario_entries'
    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    description = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    audio = Column(Text, nullable=True)  # Almacena audio en base64

    def to_dict(self):
        return {
            "id": self.id,
            "date": self.date.isoformat(),
            "description": self.description,
            "content": self.content,
            "audio": self.audio
        }

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Ruta para manejar mensajes de texto con contexto
@app.route('/message', methods=['POST'])
def handle_message():
    try:
        data = request.get_json()
        logging.info(f"Datos recibidos: {data}")  # Depuración

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
        completion = client_chat.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=messages,
            max_tokens=200
        )

        logging.info(f"Respuesta completa del modelo: {completion}")  # Depuración

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
            logging.error(f"Error al generar el audio: {tts_response.status_code} - {tts_response.text}")
            # Devolver solo el texto en caso de error con el audio
            return jsonify({'reply': bot_reply, 'audio': None}), 500

    except Exception as e:
        logging.error(f"Error al procesar la solicitud: {e}")
        return jsonify({'reply': 'Hubo un error al procesar tu solicitud.'}), 500

# Ruta para generar imágenes a partir de un prompt
@app.route('/generate-image', methods=['POST'])
def generate_image():
    try:
        prompt = request.form.get('prompt', '')
        # aspectRatio, style y referenceImage si las envías
        aspect_ratio = request.form.get('aspectRatio', 'portrait')
        style = request.form.get('style', 'No style')
        # Si envías la imagen como archivo:
        # reference_image = request.files.get('referenceImage')

        if not prompt:
            return jsonify({'error': 'No se proporcionó ningún prompt.'}), 400

        image = client_image.text_to_image(prompt)

        if isinstance(image, Image.Image):
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_bytes = buffered.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            return jsonify({'image': img_base64}), 200
        else:
            return jsonify({'error': 'Error al generar la imagen.'}), 500

    except Exception as e:
        logging.error(f"Error al generar la imagen: {e}")
        return jsonify({'error': 'Hubo un error al generar la imagen.'}), 500


# Ruta para obtener todas las entradas del diario
@app.route('/diarios', methods=['GET'])
def get_diarios():
    session = Session()
    try:
        entries = session.query(DiarioEntry).order_by(DiarioEntry.date.desc()).all()
        return jsonify([entry.to_dict() for entry in entries]), 200
    except Exception as e:
        logging.error(f"Error al obtener las entradas del diario: {e}")
        return jsonify({"error": "Error al obtener las entradas del diario."}), 500
    finally:
        session.close()

# Ruta para crear una nueva entrada en el diario
@app.route('/diarios', methods=['POST'])
def create_diario():
    session = Session()
    try:
        data = request.get_json()
        if data:
            # Crear entrada manualmente
            date_str = data.get('date')
            description = data.get('description')
            content = data.get('content')
            audio = data.get('audio')  # Opcional

            # Validar campos obligatorios
            if not date_str or not description or not content:
                return jsonify({"error": "Los campos 'date', 'description' y 'content' son obligatorios."}), 400

            # Convertir date_str a objeto datetime.date
            try:
                date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({"error": "El campo 'date' debe tener el formato 'YYYY-MM-DD'."}), 400

            # Crear y almacenar la nueva entrada
            new_entry = DiarioEntry(
                date=date_obj,
                description=description,
                content=content,
                audio=audio
            )
            session.add(new_entry)
            session.commit()
            return jsonify({"message": "Entrada de diario creada exitosamente.", "entry": new_entry.to_dict()}), 201
        else:
            # Generar entrada automáticamente
            new_entry = generate_and_store_diary(session)
            if new_entry:
                return jsonify({"message": "Entrada de diario generada exitosamente.", "entry": new_entry.to_dict()}), 201
            else:
                return jsonify({"error": "Error al generar la entrada del diario."}), 500
    except Exception as e:
        session.rollback()
        logging.error(f"Error al crear la entrada del diario: {e}")
        return jsonify({"error": "Error al crear la entrada del diario."}), 500
    finally:
        session.close()

def generate_and_store_diary(session):
    try:
        # Obtener la fecha actual
        now = datetime.utcnow()
        today = now.date()

        # Generar contenido con Hugging Face
        completion = client_chat.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=[
                {
                    "role": "system",
                    "content": "Genera una entrada de diario reflexiva, positiva y que describa las actividades realizadas durante el momento actual."
                }
            ],
            max_tokens=100
        )

        bot_reply = completion['choices'][0]['message']['content'].strip()

        # Crear una descripción breve
        description = bot_reply.split('.')[0] + '.' if '.' in bot_reply else bot_reply

        # Convertir el texto a audio usando ElevenLabs
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

        elevenlabs_headers = {
            'xi-api-key': ELEVENLABS_API_KEY,
            'Content-Type': 'application/json'
        }

        # Hacer la solicitud a ElevenLabs
        tts_response = requests.post(ELEVENLABS_TTS_URL, headers=elevenlabs_headers, json=elevenlabs_payload)

        if tts_response.status_code == 200:
            # Leer el contenido binario del audio
            audio_content = tts_response.content

            # Codificar el audio en base64
            audio_base64 = base64.b64encode(audio_content).decode('utf-8')
        else:
            logging.error(f"Error al generar el audio: {tts_response.status_code} - {tts_response.text}")
            audio_base64 = None

        # Crear y almacenar la nueva entrada
        new_entry = DiarioEntry(
            date=today,
            description=description,
            content=bot_reply,
            audio=audio_base64
        )
        session.add(new_entry)
        session.commit()
        logging.info("Entrada de diario generada y almacenada exitosamente.")
        return new_entry
    except Exception as e:
        session.rollback()
        logging.error(f"Error al generar y almacenar la entrada del diario: {e}")
        return None

# Ruta para eliminar una entrada del diario
@app.route('/diarios/<int:entry_id>', methods=['DELETE'])
def delete_diario(entry_id):
    session = Session()
    try:
        entry = session.query(DiarioEntry).filter_by(id=entry_id).first()
        if not entry:
            return jsonify({"error": "Entrada no encontrada."}), 404

        session.delete(entry)
        session.commit()
        logging.info(f"Entrada con id {entry_id} eliminada exitosamente.")
        return jsonify({"message": "Entrada eliminada exitosamente."}), 200
    except Exception as e:
        session.rollback()
        logging.error(f"Error al eliminar la entrada del diario: {e}")
        return jsonify({"error": "Error al eliminar la entrada del diario."}), 500
    finally:
        session.close()

# Configurar el scheduler
scheduler = BackgroundScheduler()

def scheduled_task():
    """
    Tarea programada para generar una nueva entrada en el diario automáticamente.
    """
    session = Session()
    try:
        generate_and_store_diary(session)
        logging.info("Entrada de diario generada automáticamente.")
    except Exception as e:
        logging.error(f"Error al generar la entrada del diario: {e}")
    finally:
        session.close()

scheduler.add_job(scheduled_task, 'cron', hour=0, id='generate_diary')

# Iniciar el scheduler
scheduler.start()
logging.info("Scheduler iniciado para generar entradas cada 5 minutos.")

# Detener el scheduler al salir
atexit.register(lambda: scheduler.shutdown())
logging.info("Scheduler shutdown registrado.")

if __name__ == '__main__':
    logging.info("Servidor Flask iniciado.")
    app.run(debug=True)

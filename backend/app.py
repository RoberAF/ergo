from flask import Flask, request, jsonify
from flask_cors import CORS
from huggingface_hub import InferenceClient
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Configurar el cliente de Hugging Face
API_KEY = os.getenv('HUGGINGFACE_API_KEY')  # Asegúrate de configurar esta variable de entorno
client = InferenceClient(token=API_KEY)

# Ruta para manejar mensajes de texto con contexto
@app.route('/message', methods=['POST'])
def handle_message():
    try:
        data = request.get_json()
        print("Datos recibidos:", data)  # Depuración

        messages = data.get('messages', [])

        if not messages:
            return jsonify({'reply': 'No se proporcionó ningún mensaje.'}), 400

        # Limitar el historial para evitar exceder el límite de tokens
        MAX_HISTORY = 20
        if len(messages) > MAX_HISTORY:
            messages = messages[-MAX_HISTORY:]

        # Generar respuesta
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=messages,
            max_tokens=200
        )

        print("Respuesta completa del modelo:", completion)  # Depuración

        # Obtener la respuesta del modelo directamente
        bot_reply = completion['choices'][0]['message']['content']

        return jsonify({'reply': bot_reply})

    except Exception as e:
        print(f"Error al procesar la solicitud: {e}")
        return jsonify({'reply': 'Hubo un error al procesar tu solicitud.'}), 500

if __name__ == '__main__':
    app.run(debug=True)

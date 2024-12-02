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

# Ruta para manejar mensajes de texto
@app.route('/message', methods=['POST'])
def handle_message():
    data = request.get_json()
    user_message = data.get('message')

    # Añadir instrucciones al modelo
    messages = [
        {"role": "system", "content": "Imita ser un humano y mantener conversaciones naturales, responde de manera clara y concisa en español. Por favor, evita incluir código o formatos innecesarios en tus respuestas."},
        {"role": "user", "content": user_message}
    ]
    try:
        completion = client.chat.completions.create(
            model="meta-llama/Llama-3.1-8B-Instruct",
            messages=messages,
            max_tokens=200  # Ajustar según sea necesario
        )
        # Imprimir la respuesta completa para depuración
        print("Respuesta completa del modelo:")
        print(completion)

        # Obtener la respuesta del modelo directamente
        bot_reply = completion['choices'][0]['message']['content']

    except Exception as e:
        print(f"Error al generar respuesta: {e}")
        bot_reply = "Lo siento, ha ocurrido un error al generar la respuesta."

    return jsonify({'reply': bot_reply})

if __name__ == '__main__':
    app.run(debug=True)

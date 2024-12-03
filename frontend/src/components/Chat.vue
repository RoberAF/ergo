<!-- src/components/Chat.vue -->
<template>
  <div>
    <Navbar/>
  </div>
  <div class="flex flex-col flex-1">
    <!-- Área de mensajes -->
    <div class="flex-1 overflow-y-auto p-4 custom-scrollbar">
      <div v-for="(message, index) in messages" :key="index" :class="[
        'flex mb-2',
        message.role === 'user' ? 'justify-end' : 'justify-start',
      ]">
        <p class="break-words w-auto max-w-xs p-3 rounded-3xl" :class="[
          message.role === 'user'
            ? 'bg-blue-500 text-white rounded-br-md'
            : 'bg-gray-600 text-gray-100 rounded-bl-md',
        ]">
          {{ message.content }}
        </p>
      </div>
    </div>

    <!-- Área de entrada -->
    <div class="flex-none p-4 w-full">
      <div class="flex w-full rounded-xl">
        <!-- Campo de entrada -->
        <input v-model="userInput" @keyup.enter="sendMessage" type="text"
          class="flex-1 p-2 rounded-xl  bg-white bg-opacity-10 backdrop-blur-xl	 shadow-xl focus:outline-none"
          placeholder="Escribe tu mensaje..." />
        <!-- Botón Enviar -->
        <button @click="sendMessage"
          class="-ml-px px-4 bg-blue-500 text-white border border-gray-600 rounded-xl focus:outline-none">
          Enviar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import axios from 'axios';
import { ref } from 'vue';

export default {
  components: {
    Navbar
  },
  name: 'Chat',
  setup() {
    // Inicializar el historial de mensajes sin el mensaje de sistema
    const messages = ref([]);
    const userInput = ref('');
    const isLoading = ref(false);

    const sendMessage = async () => {
      if (userInput.value.trim() === '') return;

      // Agregar el mensaje del usuario al historial
      messages.value.push({
        role: 'user',
        content: userInput.value,
      });

      const currentMessage = userInput.value;
      userInput.value = '';
      isLoading.value = true;

      try {
        const response = await axios.post('http://localhost:5000/message', {
          messages: messages.value,
        });

        // Agregar la respuesta del bot al historial
        messages.value.push({
          role: 'bot',
          content: response.data.reply,
        });
      } catch (error) {
        console.error('Error al enviar el mensaje:', error);
        if (error.response) {
          // El servidor respondió con un código de estado fuera del rango 2xx
          messages.value.push({
            role: 'bot',
            content:
              error.response.data.reply ||
              'Hubo un error al enviar tu mensaje. Por favor, intenta de nuevo.',
          });
        } else if (error.request) {
          // La solicitud fue hecha pero no se recibió respuesta
          messages.value.push({
            role: 'bot',
            content:
              'No se recibió respuesta del servidor. Por favor, intenta de nuevo.',
          });
        } else {
          // Algo sucedió al configurar la solicitud que desencadenó un Error
          messages.value.push({
            role: 'bot',
            content:
              'Hubo un error al enviar tu mensaje. Por favor, intenta de nuevo.',
          });
        }
      } finally {
        isLoading.value = false;
      }
    };

    return {
      messages,
      userInput,
      sendMessage,
      isLoading,
    };
  },
};
</script>

<style scoped>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #4a5568 #2d3748;
}

.custom-scrollbar::-webkit-scrollbar {
  width: 8px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: #2d3748;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #4a5568;
  border-radius: 4px;
  border: 2px solid #2d3748;
}
</style>

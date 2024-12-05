<template>
  <div class="flex flex-col flex-1">
    <!-- Área de mensajes -->
    <div class="flex-1 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-slate-900/20 scrollbar-track-transparent">
      <div v-for="(message, index) in messages" :key="index" :class="[
        'flex mb-2',
        message.role === 'user' ? 'justify-end' : 'justify-start',
      ]">
        <p class="break-words w-auto max-w-xs p-3 rounded-3xl" :class="[
          message.role === 'user'
            ? 'bg-slate-600 text-white rounded-br-md'
            : 'bg-slate-600 text-gray-100 rounded-bl-md',
        ]">
          {{ message.content }}
        </p>
      </div>
      <!-- Indicador de Carga -->
      <div v-if="isLoading" class="flex justify-start mb-2">
        <p class="bg-gray-600 text-gray-100 p-3 rounded-bl-md rounded-tl-md">
          ...
        </p>
      </div>
    </div>

    <!-- Área de entrada -->
    <div class="flex-none p-4 w-full">
      <div class="flex w-full rounded-xl bg-slate-900 bg-opacity-30 backdrop-blur-lg shadow-md ">
        <!-- Campo de entrada -->
        <input v-model="userInput" @keyup.enter="sendMessage" type="text"
          class="h-14 flex-1 p-2 bg-transparent text-white placeholder-slate-200 focus:outline-none"
          placeholder="Escribe algo..." />
        <!-- Botón Enviar -->
        <button @click="sendMessage"
          class="flex items-center justify-center px-4 bg-transparent text-white hover:bg-slate-700 hover:bg-opacity-30 transition-colors rounded-r-xl"
          aria-label="Enviar mensaje">
          Enviar
        </button>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import { ref } from 'vue';

export default {
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
        const botMessage = {
          role: 'bot',
          content: response.data.reply,
        };

        // Verificar si se recibió audio
        if (response.data.audio) {
          botMessage.audio = response.data.audio;
        }

        messages.value.push(botMessage);

        // Reproducir el audio si está disponible
        if (response.data.audio) {
          const audio = new Audio(`data:audio/mpeg;base64,${response.data.audio}`);
          audio.play().catch((error) => {
            console.error('Error al reproducir el audio:', error);
          });
        }
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

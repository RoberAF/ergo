<template>
  <div class="flex flex-col flex-1">
    <div class="flex-1 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-slate-900/20 scrollbar-track-transparent">
      <div v-for="(message, index) in messages" :key="index"
        :class="['flex mb-2', message.role === 'user' ? 'justify-end' : 'justify-start']">
        <template v-if="message.image">
          <div
            :class="message.role === 'user' ? 'bg-slate-600 text-white rounded-br-md' : 'bg-slate-600 text-gray-100 rounded-bl-md'"
            class="p-3 rounded-3xl">
            <img :src="'data:image/png;base64,' + message.image" alt="Mensaje con imagen" class="w-32 h-auto rounded" />
          </div>
        </template>
        <template v-else>
          <p class="break-words w-auto max-w-xs p-3 rounded-3xl"
            :class="[message.role === 'user' ? 'bg-slate-600 text-white rounded-br-md' : 'bg-slate-600 text-gray-100 rounded-bl-md']">
            {{ message.content }}
          </p>
        </template>
      </div>

      <div v-if="isLoading" class="flex justify-start mb-2">
        <p class="bg-gray-600 text-gray-100 p-3 rounded-bl-md rounded-tl-md">...</p>
      </div>
    </div>

    <div class="flex-none p-4 w-full">
      <div class="flex w-full rounded-xl bg-slate-900 bg-opacity-30 backdrop-blur-lg shadow-md">
        <input v-model="userInput" @keyup.enter="sendMessage" type="text"
          class="h-14 flex-1 p-2 bg-transparent text-white placeholder-slate-200 focus:outline-none"
          placeholder="Escribe algo..." />
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
import { globalState } from '../store.js'; // Importa el estado global

export default {
  name: 'Chat',
  setup() {
    const userInput = ref('');
    const isLoading = ref(false);
    // messages se obtienen del estado global
    const messages = globalState.messages;

    const sendMessage = async () => {
      if (userInput.value.trim() === '') return;

      messages.push({
        role: 'user',
        content: userInput.value,
      });

      userInput.value = '';
      isLoading.value = true;

      try {
        const response = await axios.post('http://90.164.240.100:5000/message', {
          messages: messages,
        });

        const botMessage = {
          role: 'bot',
          content: response.data.reply || '',
        };

        if (response.data.audio) {
          botMessage.audio = response.data.audio;
        }

        messages.push(botMessage);

        if (response.data.audio) {
          const audio = new Audio(`data:audio/mpeg;base64,${response.data.audio}`);
          audio.play().catch((error) => {
            console.error('Error al reproducir el audio:', error);
          });
        }
      } catch (error) {
        console.error('Error al enviar el mensaje:', error);
        if (error.response) {
          messages.push({
            role: 'bot',
            content: error.response.data.reply || 'Hubo un error al enviar tu mensaje. Por favor, intenta de nuevo.',
          });
        } else if (error.request) {
          messages.push({
            role: 'bot',
            content: 'No se recibió respuesta del servidor. Por favor, intenta de nuevo.',
          });
        } else {
          messages.push({
            role: 'bot',
            content: 'Hubo un error al enviar tu mensaje. Por favor, intenta de nuevo.',
          });
        }
      } finally {
        isLoading.value = false;
      }
    };

    return {
      userInput,
      sendMessage,
      isLoading,
      messages
    };
  }
};
</script>

<style scoped>
.scrollbar-thin::-webkit-scrollbar {
  width: 8px;
}

.scrollbar-thin::-webkit-scrollbar-track {
  background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
  background-color: rgba(15, 23, 42, 0.2);
  border-radius: 4px;
  border: 2px solid transparent;
  background-clip: padding-box;
}

.scrollbar-thin::-webkit-scrollbar-thumb:hover {
  background-color: rgba(15, 23, 42, 0.3);
}

.scrollbar-thin {
  scrollbar-width: thin;
  scrollbar-color: rgba(15, 23, 42, 0.2) transparent;
}
</style>

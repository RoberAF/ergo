<template>
  <div class=" w-1/3 fixed top-0">
    <Navbar />
  </div>
  <div class="flex flex-col w-1/3 z-10 mb-4">
    
    <!-- Área de mensajes -->
    <div class="flex-1 overflow-y-auto p-4 custom-scrollbar" :style="{ maxHeight: maxMessagesHeight }">
      <div v-for="(message, index) in messages" :key="index" :class="[
        'flex mb-2',
        message.sender === 'user' ? 'justify-end' : 'justify-start',
      ]">
        <p class="break-words w-auto max-w-xs p-3 rounded-3xl" :class="[
          message.sender === 'user'
            ? 'bg-blue-500 text-white rounded-br-md'
            : 'bg-gray-600 text-gray-100 rounded-bl-md',
        ]">
          {{ message.text }}
        </p>
      </div>
    </div>
    <!-- Área de entrada -->
    <div class="flex-none p-4 w-full">
      <div class="flex w-full">
        <!-- Campo de entrada -->
        <input v-model="userInput" @keyup.enter="sendMessage" type="text"
          class="flex-1 p-2 bg-gray-800 text-white border border-gray-600 rounded-l focus:outline-none"
          placeholder="Escribe tu mensaje..." />
        <!-- Botón Enviar -->
        <button @click="sendMessage"
          class="-ml-px px-4 bg-blue-500 text-white border border-gray-600 rounded-r focus:outline-none">
          Enviar
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import Navbar from './Navbar.vue';
import axios from 'axios';

export default {
  components: {
    Navbar,
  },
  data() {
    return {
      messages: [],
      userInput: '',
    };
  },
  methods: {
    async sendMessage() {
      if (this.userInput.trim() === '') return;

      // Agregar el mensaje del usuario al array de mensajes
      this.messages.push({ sender: 'user', text: this.userInput });
      const message = this.userInput;
      this.userInput = '';

      try {
        // Enviar el mensaje al backend
        const response = await axios.post('http://localhost:5000/message', {
          message,
        });

        // Agregar la respuesta del bot al array de mensajes
        this.messages.push({ sender: 'bot', text: response.data.reply });
      } catch (error) {
        console.error('Error al enviar el mensaje:', error);
        this.messages.push({
          sender: 'bot',
          text: 'Hubo un error al enviar tu mensaje. Por favor, intenta de nuevo.',
        });
      }
    },
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
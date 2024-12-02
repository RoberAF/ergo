<template>
  <div class="flex flex-col h-full w-full">
    <!-- Área de mensajes -->
    <div class="flex-1 overflow-y-auto">
      <!-- Aquí irían los mensajes -->
    </div>
    <!-- Área de entrada -->
    <div class="flex-none p-4">
      <div class="flex w-full">
        <!-- Campo de entrada -->
        <input v-model="userInput" @keyup.enter="sendMessage" type="text"
          class="flex-1 p-2 bg-gray-800 text-white border border-gray-600 rounded-l focus:outline-none"
          placeholder="Escribe tu mensaje..." />
        <!-- Botón Enviar -->
        <button @click="sendMessage"
          class="-ml-px px-4 text-white border border-gray-600 focus:outline-none">
          Enviar
        </button>
        <!-- Botón de grabación -->
        <button @click="toggleRecording"
          class="-ml-px px-4 text-white border border-gray-600 rounded-r focus:outline-none">
          {{ isRecording ? '⏹️' : '🎤' }}
        </button>
      </div>
    </div>
  </div>
</template>


<script>
export default {
  // Tu código existente
};
</script>

<style scoped>
/* Estilos adicionales si es necesario */
</style>

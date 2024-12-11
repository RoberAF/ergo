<template>
  <div
    class="relative bg-slate-900 bg-opacity-40 backdrop-filter backdrop-blur-lg rounded-xl shadow-lg flex flex-col w-full max-w-4xl mx-auto h-full overflow-hidden">

    <!-- Contenedor Scrollable -->
    <div
      class="flex-1 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-slate-900/20 scrollbar-track-transparent relative z-10">

      <!-- Grid de 2 Columnas para Tarjetas -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

        <!-- Tarjeta Selfie -->
        <div @click="navigateTo('Selfie')"
          class="relative flex items-center bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg rounded-lg shadow-md p-6 cursor-pointer hover:bg-white/30 transition-colors duration-300">
          <div>
            <h3 class="text-lg font-semibold text-gray-200">Selfie</h3>
            <p class="text-sm text-gray-300 mt-2">Obtén un selfie de tu Ergo en el estilo que quieras!</p>
          </div>
          <img src="https://1464501529.rsc.cdn77.org/assistant/Replika_selfies_recommended.png" alt="Selfie"
            class="w-16 h-16 object-contain ml-4" />
        </div>

        <!-- Tarjeta Imágenes IA -->
        <div @click="navigateTo('ImagenesIA')"
          class="relative flex items-center bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg rounded-lg shadow-md p-6 cursor-pointer hover:bg-white/30 transition-colors duration-300">
          <div>
            <h3 class="text-lg font-semibold text-gray-200">Imágenes IA</h3>
            <p class="text-sm text-gray-300 mt-2">Genera imágenes usando IA</p>
          </div>
          <img src="https://1464501529.rsc.cdn77.org/assistant/AI_images.png" alt="Imágenes IA"
            class="w-16 h-16 object-contain ml-4" />
        </div>

      </div>

      <ImagenesIA @confirm-image="handleConfirmImage" />

    </div>
  </div>
</template>

<script>
import Chat from './Chat.vue';
import ImagenesIA from './ImagenesIA.vue';
export default {
  name: 'Actividades',
  data() {
    return {
      messages: []
    };
  },
  methods: {
    navigateTo(componentName) {
      this.$router.push({ name: componentName });
    },
    handleConfirmImage(imageData) {
      this.messages.push({
        role: 'bot',
        content: '',
        image: imageData
      });
    }
  },
};
</script>

<style scoped></style>

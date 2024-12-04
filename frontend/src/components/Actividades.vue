<template>
  <div class="relative bg-white bg-opacity-70 backdrop-filter backdrop-blur-lg rounded-lg shadow-lg flex flex-col w-full max-w-4xl mx-auto h-full overflow-hidden">
    
    <!-- Fondo translúcido -->
    <div class="absolute inset-0 bg-black opacity-20 rounded-lg"></div>
    
    <!-- Contenedor Scrollable -->
    <div class="flex-1 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-slate-900/20 scrollbar-track-transparent relative z-10">
      
      <!-- Grid de 2 Columnas para Tarjetas -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        
        <!-- Tarjeta Principal: Selfie -->
        <div
          @click="navigateTo('Selfie')"
          class="relative flex items-center bg-slate-800 bg-opacity-25 backdrop-filter backdrop-blur-lg rounded-lg shadow-md p-6 cursor-pointer hover:bg-slate-700 transition-colors duration-300"
        >
          <div>
            <h3 class="text-lg font-semibold text-gray-200">Selfie</h3>
            <p class="text-sm text-gray-300 mt-2">Obtén un selfie de tu Ergo en el estilo que quieras!</p>
          </div>
          <!-- Imagen a la derecha -->
          <img
            src="https://1464501529.rsc.cdn77.org/assistant/Replika_selfies_recommended.png"
            alt="Selfie"
            class="w-16 h-16 object-contain ml-4"
          />
        </div>

        <!-- Tarjeta Principal: Imágenes IA -->
        <div
          @click="navigateTo('ImagenesIA')"
          class="relative flex items-center bg-slate-800 bg-opacity-25 backdrop-filter backdrop-blur-lg rounded-lg shadow-md p-6 cursor-pointer hover:bg-slate-700 transition-colors duration-300"
        >
          <div>
            <h3 class="text-lg font-semibold text-gray-200">Imágenes IA</h3>
            <p class="text-sm text-gray-300 mt-2">Genera imágenes usando IA</p>
          </div>
          <!-- Imagen a la derecha -->
          <img
            src="https://1464501529.rsc.cdn77.org/assistant/AI_images.png"
            alt="Imágenes IA"
            class="w-16 h-16 object-contain ml-4"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Actividades',
  methods: {
    navigateTo(componentName) {
      this.$router.push({ name: componentName });
    },
  },
};
</script>

<style scoped>
/* Añade estilos específicos para Actividades aquí si es necesario */
</style>

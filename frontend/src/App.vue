<template>
  <div class="flex h-screen bg-gray-900">
    <!-- Modelo 3D a la izquierda -->
    <Model3D class="w-1/3 h-full" />
    <!-- Chat a la derecha -->
    <Chat class="w-1/3 h-full" />
  </div>
</template>

<script>
import Chat from './components/Chat.vue';
import Model3D from './components/Model3D.vue';

export default {
  components: {
    Chat,
    Model3D,
  },
};
</script>

<style scoped>
/* Estilos adicionales si es necesario */
</style>

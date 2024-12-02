<template>
  <div class="relative h-screen overflow-hidden bg-gray-900">
    <!-- Modelo 3D en el fondo -->
    <Model3D class="absolute inset-0 z-0" />
    <!-- Contenedor para alinear el chat -->
    <div class="absolute inset-0 flex flex-col justify-end items-center">
      <Chat class="w-1/3"/>
    </div>
  </div>
</template>

<script>
import Chat from './components/Chat.vue';
import Model3D from './components/Model3D.vue';
import Navbar from './components/Navbar.vue';

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

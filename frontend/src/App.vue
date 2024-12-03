<template>
  <div class="relative h-screen overflow-hidden">
    <!-- Modelo de Fondo -->
    <BackgroundModel />

    <!-- Contenedor Principal para las 3 Columnas -->
    <div class="relative z-10 flex h-full">
      <!-- Primera columna: Modelo 3D -->
      <div class="w-1/3 flex justify-center items-center">
        <Model3D class="w-full h-full" />
      </div>

      <!-- Segunda columna: Chat -->
      <div class="w-1/3 flex flex-col justify-end p-4">
        <Chat class="w-full" />
      </div>

      <!-- Tercera columna: Actividades / RouterView -->
      <div class="w-1/3 flex flex-col justify-end p-4">
        <RouterView class="w-full" />
      </div>
    </div>
  </div>
</template>

<script>
import BackgroundModel from './components/BackgroundModel.vue';
import Model3D from './components/Model3D.vue';
import Chat from './components/Chat.vue';

export default {
  name: 'App',
  components: {
    BackgroundModel,
    Model3D,
    Chat,
  },
};
</script>

<style>
/* Estilos globales si es necesario */
</style>

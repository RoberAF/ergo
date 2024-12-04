<template>
  <div class="relative h-screen overflow-hidden">
    <!-- Modelo de Fondo -->
    <!-- <BackgroundModel /> -->
    <div id="bg" class="w-full h-full absolute inset-0 z-0"></div>

    <!-- Contenedor Principal para las 3 Columnas -->
    <div class="relative z-10 flex h-full">
      <!-- Primera columna: Modelo 3D -->
      <div class="w-1/3 flex justify-center items-center">
        <Model3D class="w-full h-full" />
      </div>

      <!-- Segunda columna: Chat -->
      <div class="w-1/3 flex flex-col justify-between p-4">
        <!-- Navbar -->
        <div class="w-full">
          <Navbar class="w-full" />
        </div>
        <!-- Chat -->
        <div class="w-full flex-grow overflow-y-auto relative fade-top">
          <Chat class="w-full h-full" />
        </div>
      </div>

      <!-- Tercera columna: Actividades / RouterView -->
      <div class="w-1/3 flex flex-col justify-end p-4">
        <RouterView class="w-full my-16" />
      </div>
    </div>
  </div>
</template>

<style>
#bg {
  background-color: #4158D0;
  background-image: linear-gradient(43deg, #4158D0 0%, #C850C0 46%, #FFCC70 100%);
}
</style>




<script>
import BackgroundModel from './components/BackgroundModel.vue';
import Model3D from './components/Model3D.vue';
import Chat from './components/Chat.vue';
import Navbar from './components/Navbar.vue';

export default {
  name: 'App',
  components: {
    BackgroundModel,
    Model3D,
    Chat,
    Navbar
  },
};
</script>

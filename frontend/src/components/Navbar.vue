<!-- src/components/Navbar.vue -->

<template>
  <div class="w-full max-w-fit-content mx-auto rounded-xl bg-slate-900 bg-opacity-30 shadow-md">
    <nav class="flex justify-around text-white py-2">
      <!-- Item de Navegación: Chat -->
      <router-link
        to="/"
        class="flex flex-col items-center cursor-pointer px-4 py-2 bg-opacity-0 backdrop-blur-lg rounded-xl hover:bg-white/30 transition-colors duration-200"
        :class="{ 'bg-slate-500': isActive('/') }"
      >
        <span class="text-sm font-bold">Chat</span>
      </router-link>

      <!-- Item de Navegación: Actividades -->
      <router-link
        to="/actividades"
        class="flex flex-col items-center cursor-pointer px-4 py-2 bg-opacity-0 backdrop-blur-lg rounded-xl hover:bg-white/30 transition-colors duration-200"
        :class="{ 'bg-slate-500': isActive('/actividades') }"
      >
        <span class="text-sm font-bold">Actividades</span>
      </router-link>

      <!-- Item de Navegación: Consciencia -->
      <router-link
        to="/consciencia"
        class="flex flex-col items-center cursor-pointer px-4 py-2 bg-opacity-0 backdrop-blur-lg rounded-xl hover:bg-white/30 transition-colors duration-200"
        :class="{ 'bg-slate-500': isActive('/consciencia') }"
      >
        <span class="text-sm font-bold">Consciencia</span>
      </router-link>

      <!-- Item de Navegación: Diario -->
      <router-link
        to="/diario"
        class="flex flex-col items-center cursor-pointer px-4 py-2 bg-opacity-0 backdrop-blur-lg rounded-xl hover:bg-white/30 transition-colors duration-200"
        :class="{ 'bg-slate-500': isActive('/diario') }"
      >
        <span class="text-sm font-bold">Diario</span>
      </router-link>

      <!-- Item de Navegación: Perfil -->
      <router-link
        to="/perfil"
        class="flex flex-col items-center cursor-pointer px-4 py-2 bg-opacity-0 backdrop-blur-lg rounded-xl hover:bg-white/30 transition-colors duration-200"
        :class="{ 'bg-slate-500': isActive('/perfil') }"
      >
        <span class="text-sm font-bold">Perfil</span>
      </router-link>
    </nav>
  </div>
</template>

<script>
import { useRoute } from 'vue-router';
import { computed } from 'vue';

export default {
  name: 'Navbar',
  setup() {
    const route = useRoute();

    const isActive = (path) => computed(() => route.path === path);

    return {
      isActive,
    };
  },
};
</script>

<style scoped>
/* Puedes agregar estilos personalizados aquí si es necesario */
</style>

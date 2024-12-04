// src/router/index.js

import { createRouter, createWebHistory } from 'vue-router';
import Chat from '../components/Chat.vue';
import Actividades from '../components/Actividades.vue';
import Selfie from '../components/Selfie.vue';
import ImagenesIA from '../components/ImagenesIA.vue';
// import Memoria from '../components/Memoria.vue';
// import Diario from '../components/Diario.vue';
// import Perfil from '../components/Perfil.vue';
// import NotFound from '../components/NotFound.vue'; // Componente para rutas no encontradas

const routes = [
  {
    path: '/',
    name: 'home',
  },
  {
    path: '/actividades',
    name: 'actividades',
    component: Actividades
  },
  {
    path: '/selfie',
    name: 'Selfie',
    component: Selfie,
  },
  {
    path: '/imagenes-ia',
    name: 'ImagenesIA',
    component: ImagenesIA,
  },
  // {
  //   path: '/memoria',
  //   name: 'memoria',
  //   component: Memoria
  // },
  // {
  //   path: '/diario',
  //   name: 'diario',
  //   component: Diario
  // },
  // {
  //   path: '/perfil',
  //   name: 'perfil',
  //   component: Perfil
  // },
  // // Ruta 404 para manejar rutas no definidas
  // {
  //   path: '/:pathMatch(.*)*',
  //   name: 'NotFound',
  //   component: NotFound
  // }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL), // Corrección del typo aquí
  routes
});

export default router;

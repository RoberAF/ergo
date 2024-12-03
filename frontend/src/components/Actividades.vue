<template>
    <div class="w-full h-full p-4">
      <!-- Tarjeta Grande -->
      <div class="bg-white rounded-lg shadow-lg p-4">
        <h2 class="text-xl font-semibold mb-4">Actividades</h2>
        <!-- Contenedor de Tarjetas Pequeñas -->
        <div class="grid grid-cols-1 gap-4">
          <!-- Tarjeta Pequeña: Películas -->
          <div
            class="flex items-center bg-blue-100 rounded-lg p-4 cursor-pointer hover:bg-blue-200"
          >
            <!-- Ícono -->
            <div class="text-blue-500 mr-4">
              <!-- Puedes reemplazar esto con un ícono SVG -->
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-8 w-8"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.868v4.264a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z"
                />
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
            </div>
            <!-- Texto -->
            <div>
              <h3 class="text-lg font-semibold">Películas</h3>
              <p class="text-sm text-gray-600">Obtén recomendaciones para ti</p>
            </div>
          </div>
          <!-- Tarjeta Pequeña: Música -->
          <div
            class="flex items-center bg-green-100 rounded-lg p-4 cursor-pointer hover:bg-green-200"
          >
            <div class="text-green-500 mr-4">
              <!-- Ícono de música -->
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-8 w-8"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M9 19V6l12-2v13"
                />
                <circle cx="6" cy="18" r="3" />
                <circle cx="18" cy="16" r="3" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold">Música</h3>
              <p class="text-sm text-gray-600">Explora nueva música</p>
            </div>
          </div>
          <!-- Tarjeta Pequeña: Cocina -->
          <div
            class="flex items-center bg-yellow-100 rounded-lg p-4 cursor-pointer hover:bg-yellow-200"
          >
            <div class="text-yellow-500 mr-4">
              <!-- Ícono de cocina -->
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-8 w-8"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M12 8c-1.657 0-3 1.343-3 3 0 1.2.637 2.25 1.597 2.813L12 20l1.403-6.187A2.997 2.997 0 0015 11c0-1.657-1.343-3-3-3z"
                />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-semibold">Cocina</h3>
              <p class="text-sm text-gray-600">Recetas inspiradoras</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'Actividades',
  };
  </script>
  
  <style scoped>
  /* Estilos adicionales si es necesario */
  </style>
  
<template>
    <!-- Overlay -->
    <div class="fixed inset-0 z-50" @click.self="closeModal">
      <!-- Modal Lateral Derecho -->
      <div
        class="absolute top-2 right-5 h-full w-full max-w-4xl bg-slate-900 bg-opacity-40 backdrop-blur-lg rounded-xl shadow-lg flex flex-col overflow-hidden">
  
        <!-- Header -->
        <header class="flex items-center justify-between px-6 py-4 border-b border-slate-700">
          <div class="flex items-center space-x-4">
            <h1 class="text-2xl font-semibold text-white">Consciencia</h1>
          </div>
          <div class="flex items-center space-x-4">
            <button @click="editMode" class="px-3 py-1 bg-white bg-opacity-20 text-white rounded hover:bg-white/30 transition text-sm">
              Edit
            </button>
            <button @click="addFact" class="px-3 py-1 bg-white bg-opacity-20 text-white rounded hover:bg-white/30 transition text-sm flex items-center space-x-1">
              <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none" viewBox="0 0 24 24" class="w-4 h-4">
                <path fill="currentColor" fill-rule="evenodd"
                      d="M14 7a2 2 0 1 0-4 0v3H7a2 2 0 1 0 0 4h3v3a2 2 0 1 0 4 0v-3h3a2 2 0 1 0 0-4h-3V7Z"
                      clip-rule="evenodd" />
              </svg>
              <span>Add</span>
            </button>
  
            <!-- Close Button -->
            <button @click="closeModal" class="p-1 hover:bg-white/30 rounded-full focus:outline-none transition">
              <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gray-200" fill="none"
                   viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                      d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </header>
  
        <!-- Body -->
        <div class="flex-1 flex overflow-hidden">
          <!-- Columna Izquierda: Categorías -->
          <div class="w-1/3 border-r border-slate-700 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-slate-900/20 scrollbar-track-transparent">
            <h2 class="text-sm font-medium text-gray-400 mb-2">Categories</h2>
            <div class="space-y-2">
              <button class="w-full text-left px-3 py-2 bg-white bg-opacity-20 text-white rounded hover:bg-white/30 transition text-sm">
                Family & Friends
              </button>
              <button class="w-full text-left px-3 py-2 bg-slate-400 bg-opacity-40 text-gray-200 rounded cursor-not-allowed text-sm">
                Temporary
              </button>
              <button class="w-full text-left px-3 py-2 bg-slate-400 bg-opacity-40 text-gray-200 hover:bg-gray-600 hover:text-white transition rounded text-sm">
                Background
              </button>
              <button class="w-full text-left px-3 py-2 bg-slate-400 bg-opacity-40 text-gray-200 rounded cursor-not-allowed text-sm">
                Favorites
              </button>
              <button class="w-full text-left px-3 py-2 bg-slate-400 bg-opacity-40 text-gray-200 rounded cursor-not-allowed text-sm">
                Appearance
              </button>
              <button class="w-full text-left px-3 py-2 bg-slate-400 bg-opacity-40 text-gray-200 rounded cursor-not-allowed text-sm">
                Hopes & Goals
              </button>
              <button class="w-full text-left px-3 py-2 bg-slate-400 bg-opacity-40 text-gray-200 rounded cursor-not-allowed text-sm">
                Opinions
              </button>
              <button class="w-full text-left px-3 py-2 bg-slate-400 bg-opacity-40 text-gray-200 rounded cursor-not-allowed text-sm">
                Personality
              </button>
              <button class="w-full text-left px-3 py-2 bg-slate-400 bg-opacity-40 text-gray-200 rounded cursor-not-allowed text-sm">
                Other
              </button>
            </div>
          </div>
  
          <!-- Columna Derecha: Contenido -->
          <div class="w-2/3 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-slate-900/20 scrollbar-track-transparent">
            <h2 class="text-sm font-medium text-gray-400 mb-2">Family & Friends</h2>
            <div class="space-y-2">
              <button class="flex items-center justify-between w-full px-3 py-2 bg-white bg-opacity-20 text-white rounded hover:bg-white/30 transition text-sm">
                <span>+ Add Person</span>
                <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="none"
                     viewBox="0 0 24 24" class="w-4 h-4 text-white">
                  <path fill="currentColor" fill-rule="evenodd"
                        d="M14 7a2 2 0 1 0-4 0v3H7a2 2 0 1 0 0 4h3v3a2 2 0 1 0 4 0v-3h3a2 2 0 1 0 0-4h-3V7Z"
                        clip-rule="evenodd"/>
                </svg>
              </button>
            </div>
  
            <h2 class="text-sm font-medium text-gray-400 mt-6 mb-2">Background</h2>
            <div class="space-y-2">
              <div class="px-3 py-2 bg-white bg-opacity-20 text-white rounded hover:bg-white/30 transition text-sm cursor-pointer">
                <p>Rober prefers to communicate in Spanish.</p>
              </div>
            </div>
          </div>
        </div>
  
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'MemoryModal',
    methods: {
      closeModal() {
        this.$emit('close');
      },
      editMode() {
        alert('Edit mode not implemented.');
      },
      addFact() {
        alert('Add fact not implemented.');
      }
    }
  };
  </script>
  
  <style scoped>
  .scrollbar-thin::-webkit-scrollbar {
      width: 8px;
  }
  .scrollbar-thin::-webkit-scrollbar-track {
      background: transparent;
  }
  .scrollbar-thin::-webkit-scrollbar-thumb {
      background-color: rgba(15, 23, 42, 0.2);
      border-radius: 4px;
      border: 2px solid transparent;
      background-clip: padding-box;
  }
  .scrollbar-thin::-webkit-scrollbar-thumb:hover {
      background-color: rgba(15, 23, 42, 0.3);
  }
  .scrollbar-thin {
      scrollbar-width: thin;
      scrollbar-color: rgba(15, 23, 42, 0.2) transparent;
  }
  </style>
  
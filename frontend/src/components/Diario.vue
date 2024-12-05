<!-- src/components/Diario.vue -->

<template>
    <div class="fixed inset-0 z-50 flex justify-end">

        <!-- Panel Diario Lateral Derecho -->
        <div
            class="m-8 relative flex flex-col bg-slate-900 bg-opacity-40 backdrop-filter backdrop-blur-lg rounded-xl shadow-lg w-3/5 h-full overflow-hidden transition-transform duration-300 ease-in-out">
            <!-- Cabecera del Panel -->
            <div class="flex items-center justify-between px-6 py-4 border-b border-slate-700">
                <h1 class="text-2xl font-semibold text-white">Diario</h1>
                <button @click="closeDiary" class="text-white hover:text-white focus:outline-none"
                    aria-label="Cerrar Diario">
                    <!-- Icono de Cerrar (X) -->
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-6 w-6" fill="none" viewBox="0 0 24 24"
                        stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <!-- Contenido del Panel con 2 Columnas -->
            <div class="flex flex-1 overflow-hidden">
                <!-- Columna Izquierda: Lista de Entradas del Diario -->
                <div
                    class="w-1/3 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-slate-900/20 scrollbar-track-transparent">
                    <ul class="space-y-4">
                        <li v-for="entry in diaryEntries" :key="entry.id"
                            class="bg-white bg-opacity-20 backdrop-filter backdrop-blur-lg rounded-lg shadow-md p-4 cursor-pointer hover:bg-white/30 transition-colors duration-300"
                            @click="selectEntry(entry)">
                            <div class="flex justify-between items-center">
                                <h3 class="text-lg font-semibold text-white">
                                    {{ formatDate(entry.date) }}
                                </h3>
                            </div>
                            <p class="text-sm text-gray-300 mt-2">{{ entry.description }}</p>
                        </li>
                    </ul>
                </div>

                <!-- Columna Derecha: Contenido de la Entrada Seleccionada -->
                <div
                    class="w-2/3 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-slate-900/20 scrollbar-track-transparent">
                    <div v-if="selectedEntry">
                        <h2 class="text-xl font-semibold text-white">
                            {{ formatFullDate(selectedEntry.date) }}
                        </h2>
                        <p class="text-white mt-2">{{ selectedEntry.content }}</p>
                        <!-- Acciones de la Entrada -->
                        <div class="mt-4 flex space-x-4">
                            <button @click="upvoteEntry"
                                class="flex items-center px-3 py-2 rounded-full bg-white bg-opacity-20 hover:bg-white/30 focus:outline-none">
                                <!-- Icono de Upvote -->
                                <!-- (Mantén tu SVG o usa otro icono según prefieras) -->
                                👍
                            </button>
                            <button @click="downvoteEntry"
                                class="flex items-center px-3 py-2 rounded-full bg-white bg-opacity-20 hover:bg-white/30 focus:outline-none">
                                <!-- Icono de Downvote -->
                                👎
                            </button>
                            <button @click="deleteEntry"
                                class="flex items-center px-3 py-2 rounded-full bg-white bg-opacity-20 hover:bg-white/30 focus:outline-none">
                                <!-- Icono de Delete -->
                                🗑️
                            </button>
                        </div>
                    </div>
                    <div v-else class="flex items-center justify-center h-full">
                        <p class="text-gray-400">Selecciona una entrada para ver su contenido</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';

export default {
    name: 'Diario',
    data() {
        return {
            diaryEntries: [],
            selectedEntry: null,
        };
    },
    methods: {
        closeDiary() {
            this.$emit('close');
        },
        selectEntry(entry) {
            this.selectedEntry = entry;
        },
        formatDate(dateStr) {
            const options = { month: 'short', day: 'numeric' };
            const date = new Date(dateStr);
            return date.toLocaleDateString('es-ES', options); // Ajusta el locale según sea necesario
        },
        formatFullDate(dateStr) {
            const options = { year: 'numeric', month: 'long', day: 'numeric' };
            const date = new Date(dateStr);
            return date.toLocaleDateString('es-ES', options); // Ajusta el locale según sea necesario
        },
        editDiary() {
            // Implementa la funcionalidad de edición aquí
            alert('La funcionalidad de edición del diario aún no está implementada.');
        },
        upvoteEntry() {
            // Implementa la funcionalidad de upvote aquí
            alert('¡Entrada votada positivamente!');
        },
        downvoteEntry() {
            // Implementa la funcionalidad de downvote aquí
            alert('¡Entrada votada negativamente!');
        },
        async deleteEntry() {
            if (this.selectedEntry) {
                const confirmDelete = confirm('¿Estás seguro de que deseas eliminar esta entrada?');
                if (!confirmDelete) return;

                try {
                    // Asumiendo que tu backend tiene una ruta DELETE /diarios/<id>
                    // Si no la tienes, esta parte no funcionará y deberías manejar la eliminación localmente
                    await axios.delete(`http://localhost:5000/diarios/${this.selectedEntry.id}`);
                    
                    // Filtrar la entrada eliminada de la lista
                    this.diaryEntries = this.diaryEntries.filter(entry => entry.id !== this.selectedEntry.id);
                    this.selectedEntry = null;
                    alert('Entrada del diario eliminada.');
                } catch (error) {
                    console.error('Error al eliminar la entrada del diario:', error);
                    alert('Hubo un error al eliminar la entrada del diario.');
                }
            }
        },
        async fetchDiaryEntries() {
            try {
                const response = await axios.get('http://localhost:5000/diarios');
                this.diaryEntries = response.data;
            } catch (error) {
                console.error('Error al obtener las entradas del diario:', error);
                alert('Hubo un error al obtener las entradas del diario.');
            }
        },
    },
    mounted() {
        this.fetchDiaryEntries();
    },
};
</script>

<style scoped>
/* Scrollbar personalizada */
.scrollbar-thin::-webkit-scrollbar {
    width: 4px;
}

.scrollbar-thumb-slate-900\/20::-webkit-scrollbar-thumb {
    background-color: rgba(15, 23, 42, 0.2);
    /* slate-900/20 */
    border-radius: 9999px;
}

.scrollbar-track-transparent::-webkit-scrollbar-track {
    background: transparent;
}

/* Añade estilos adicionales si es necesario */
</style>

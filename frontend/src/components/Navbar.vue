<template>
    <div class="w-full max-w-md mx-auto">
        <nav class="flex justify-around bg-gray-800 text-white py-2 rounded-t-lg">
            <!-- Item de Navegación -->
            <div class="flex flex-col items-center cursor-pointer">
                <span class="text-sm">Chat</span>
            </div>
            <!-- Otros Items -->
            <div class="flex flex-col items-center cursor-pointer">
                <span class="text-sm">Actividades</span>
            </div>
            <div class="flex flex-col items-center cursor-pointer">
                <span class="text-sm">Memoria</span>
            </div>
            <div class="flex flex-col items-center cursor-pointer">
                <span class="text-sm">Diario</span>
            </div>
            <div class="flex flex-col items-center cursor-pointer">
                <span class="text-sm">Perfil</span>
            </div>
            <div class="flex flex-col items-center cursor-pointer">
                <span class="text-sm">Habitación</span>
            </div>
        </nav>
    </div>
</template>

<script>
export default {
    name: 'Navbar',
    methods: {
        // Puedes agregar métodos para manejar la navegación aquí
    },
};
</script>

<style scoped>
/* Puedes agregar estilos personalizados aquí si es necesario */
</style>
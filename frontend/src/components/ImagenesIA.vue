<template>
    <div
        class="relative bg-slate-900 bg-opacity-40 backdrop-blur-lg rounded-xl shadow-lg flex flex-col w-full max-w-4xl mx-auto h-full overflow-hidden">

        <header class="flex items-center justify-between px-4 py-2 relative z-10">
            <button @click="goBack"
                class="p-1 rounded-full hover:bg-white/30 focus:outline-none focus:ring-2 focus:ring-slate-700 transition">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gray-200" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
                </svg>
            </button>

            <h1 class="text-lg font-semibold text-gray-200">AI Images</h1>

            <button @click="closeActivities"
                class="p-1 rounded-full hover:bg-white/30 focus:outline-none focus:ring-2 focus:ring-slate-700 transition">
                <svg xmlns="http://www.w3.org/2000/svg" class="w-6 h-6 text-gray-200" fill="none" viewBox="0 0 24 24"
                    stroke="currentColor">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
            </button>
        </header>

        <div
            class="flex-1 overflow-y-auto p-4 scrollbar-thin scrollbar-thumb-slate-900/20 scrollbar-track-transparent relative z-10">
            <div class="flex flex-col space-y-4">

                <div v-if="!generatedImage" class="space-y-4">
                    <div class="flex flex-col">
                        <textarea v-model="promptText" placeholder="Describe your image" maxlength="500"
                            class="w-full p-2 rounded-xl resize-none h-20 text-sm text-gray-200 bg-slate-400 bg-opacity-40 focus:outline-none focus:ring-2 focus:ring-blue-500 transition"></textarea>
                        <div class="flex items-center justify-between mt-2">
                            <span class="text-xs text-gray-400">{{ promptText.length }}/500</span>
                            <button @click="suggestPrompt"
                                class="flex items-center px-2 py-0.5 bg-white bg-opacity-20 text-white rounded-xl hover:bg-white/30 focus:outline-none focus:ring-2 focus:ring-slate-700 transition text-xs">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-0.5" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 4v16m8-8H4" />
                                </svg>
                                <span>Suggest</span>
                            </button>
                        </div>
                    </div>

                    <div class="flex flex-col">
                        <div class="text-xs font-medium text-gray-400 mb-1">Reference image</div>
                        <label
                            class="flex items-center p-2 border-2 border-dashed border-gray-600 rounded-xl cursor-pointer hover:border-gray-500 transition">
                            <input accept="image/*" type="file" class="hidden" @change="handleImageUpload">
                            <span class="flex items-center space-x-2">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 text-gray-400" fill="none"
                                    viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M3 7a4 4 0 014-4h12a4 4 0 014 4v10a4 4 0 01-4 4H7a4 4 0 01-4-4z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M7 11l5-5m0 0l5 5m-5-5v12" />
                                </svg>
                                <span class="text-gray-400 text-xs">Optionally add an image reference</span>
                            </span>
                        </label>
                    </div>

                    <div class="flex flex-col">
                        <div class="text-xs font-medium text-gray-400 mb-1">Aspect ratio</div>
                        <div class="flex space-x-2">
                            <button @click="selectAspectRatio('portrait')" :class="ratioClass('portrait')">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-0.5" fill="none"
                                    viewBox="0 0 32 33" stroke="currentColor">
                                    <rect width="16" height="28" x="8" y="2.43" fill="#fff" fill-opacity="0.3" rx="4">
                                    </rect>
                                    <rect width="14.5" height="26.5" x="8.75" y="3.18" stroke="#fff"
                                        stroke-opacity="0.7" stroke-width="1.5" rx="3.25"></rect>
                                </svg>
                                <span>Portrait</span>
                            </button>
                            <button @click="selectAspectRatio('square')" :class="ratioClass('square')">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-0.5" fill="none"
                                    viewBox="0 0 32 33" stroke="currentColor">
                                    <rect width="24" height="24" x="4" y="4.43" fill="#fff" fill-opacity="0.3" rx="4">
                                    </rect>
                                    <rect width="22.5" height="22.5" x="4.75" y="5.18" stroke="#fff"
                                        stroke-opacity="0.7" stroke-width="1.5" rx="3.25"></rect>
                                </svg>
                                <span>Square</span>
                            </button>
                            <button @click="selectAspectRatio('landscape')" :class="ratioClass('landscape')">
                                <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 mr-0.5" fill="none"
                                    viewBox="0 0 32 33" stroke="currentColor">
                                    <rect width="28" height="16" x="2" y="8.43" fill="#fff" fill-opacity="0.3" rx="4">
                                    </rect>
                                    <rect width="26.5" height="14.5" x="2.75" y="9.18" stroke="#fff"
                                        stroke-opacity="0.7" stroke-width="1.5" rx="3.25"></rect>
                                </svg>
                                <span>Landscape</span>
                            </button>
                        </div>
                    </div>

                    <div class="flex flex-col">
                        <div class="text-xs font-medium text-gray-400 mb-1">Style</div>
                        <div class="grid grid-cols-2 gap-2 sm:grid-cols-4">
                            <button @click="selectStyle('No style')" :class="styleClass('No style')">
                                <img src="https://1464501529.rsc.cdn77.org/ai_image_gen_styles/No%20style@3x.webp"
                                    alt="No style" class="w-10 h-10 mb-0.5 object-contain">
                                <span>No style</span>
                            </button>
                            <button @click="selectStyle('Dreamscape')" :class="styleClass('Dreamscape')">
                                <img src="https://1464501529.rsc.cdn77.org/ai_image_gen_styles/Dreamscape@2x.webp"
                                    alt="Dreamscape" class="w-10 h-10 mb-0.5 object-contain">
                                <span>Dreamscape</span>
                            </button>
                            <button @click="selectStyle('Anime')" :class="styleClass('Anime')">
                                <img src="https://1464501529.rsc.cdn77.org/ai_image_gen_styles/Anime@2x.webp"
                                    alt="Anime" class="w-10 h-10 mb-0.5 object-contain">
                                <span>Anime</span>
                            </button>
                            <button @click="selectStyle('Gothic')" :class="styleClass('Gothic')">
                                <img src="https://1464501529.rsc.cdn77.org/ai_image_gen_styles/Gothic@2x.webp"
                                    alt="Gothic" class="w-10 h-10 mb-0.5 object-contain">
                                <span>Gothic</span>
                            </button>
                            <button @click="selectStyle('Cyberpunk')" :class="styleClass('Cyberpunk')">
                                <img src="https://1464501529.rsc.cdn77.org/ai_image_gen_styles/Cyberpunk@2x.webp"
                                    alt="Cyberpunk" class="w-10 h-10 mb-0.5 object-contain">
                                <span>Cyberpunk</span>
                            </button>
                            <button @click="selectStyle('Painting')" :class="styleClass('Painting')">
                                <img src="https://1464501529.rsc.cdn77.org/ai_image_gen_styles/Painting@2x.webp"
                                    alt="Painting" class="w-10 h-10 mb-0.5 object-contain">
                                <span>Painting</span>
                            </button>
                            <button @click="selectStyle('Surreal')" :class="styleClass('Surreal')">
                                <img src="https://1464501529.rsc.cdn77.org/ai_image_gen_styles/Surreal@2x.webp"
                                    alt="Surreal" class="w-10 h-10 mb-0.5 object-contain">
                                <span>Surreal</span>
                            </button>
                            <button @click="selectStyle('Digital Art')" :class="styleClass('Digital Art')">
                                <img src="https://1464501529.rsc.cdn77.org/ai_image_gen_styles/Digital%20Art@2x.webp"
                                    alt="Digital Art" class="w-10 h-10 mb-0.5 object-contain">
                                <span>Digital Art</span>
                            </button>
                        </div>
                    </div>

                    <div>
                        <button :disabled="!isGenerateEnabled || isLoading" @click="generateImage"
                            class="w-full px-4 py-2 bg-white bg-opacity-20 text-white rounded-xl disabled:opacity-50 hover:bg-white/30 focus:outline-none focus:ring-2 focus:ring-blue-700 transition flex items-center justify-center text-sm">
                            <span v-if="!isLoading">Generate</span>
                            <svg v-else xmlns="http://www.w3.org/2000/svg" class="animate-spin h-4 w-4 mr-1 text-white"
                                viewBox="0 0 24 24">
                                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor"
                                    stroke-width="4"></circle>
                                <path class="opacity-75" fill="currentColor"
                                    d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                            </svg>
                        </button>
                    </div>
                </div>

                <div v-else>
                    <img :src="`data:image/png;base64,${generatedImage}`" alt="Imagen Generada"
                        class="w-full h-auto rounded-xl shadow-lg object-contain" />
                    <div class="flex space-x-4 mt-4">
                        <button @click="regenerateImage"
                            class="flex-1 px-4 py-1 bg-transparent border border-slate-700 text-slate-700 rounded-xl hover:bg-slate-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-slate-700 transition text-xs disabled:opacity-50">
                            Regenerar
                        </button>
                        <button @click="confirmImage"
                            class="flex-1 px-4 py-1 bg-transparent border border-slate-700 text-slate-700 rounded-xl hover:bg-slate-700 hover:text-white focus:outline-none focus:ring-2 focus:ring-slate-700 transition text-xs disabled:opacity-50">
                            Confirmar
                        </button>
                    </div>
                </div>

            </div>
        </div>
    </div>
</template>

<script>
import axios from 'axios';
import { addMessage } from '../store.js'; // Ajusta la ruta al store

export default {
    name: 'ImagenesIA',
    data() {
        return {
            promptText: '',
            generatedImage: null,
            isLoading: false,
            aspectRatio: 'portrait',
            selectedStyle: 'No style',
            referenceImage: null,
        };
    },
    computed: {
        isGenerateEnabled() {
            return this.promptText.trim().length > 0;
        }
    },
    methods: {
        goBack() {
            this.$router.push({ name: 'actividades' });
        },
        closeActivities() {
            this.$router.push({ name: 'home' });
        },
        suggestPrompt() {
            this.promptText = 'A beautiful landscape with mountains and a river.';
        },
        handleImageUpload(event) {
            const file = event.target.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = (e) => {
                    this.referenceImage = e.target.result;
                };
                reader.readAsDataURL(file);
            }
        },
        selectAspectRatio(ratio) {
            this.aspectRatio = ratio;
        },
        selectStyle(style) {
            this.selectedStyle = style;
        },
        async generateImage() {
            if (this.promptText.trim() === '') {
                alert('Please enter a valid prompt.');
                return;
            }

            this.isLoading = true;
            try {
                const fullPrompt = `${this.promptText.trim()} estilo ${this.selectedStyle}`;
                const formData = new FormData();
                formData.append('prompt', fullPrompt);
                formData.append('aspectRatio', this.aspectRatio);
                formData.append('style', this.selectedStyle);
                if (this.referenceImage) {
                    formData.append('referenceImage', this.referenceImage);
                }

                const response = await axios.post('http://localhost:5000/generate-image', formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data',
                    },
                });

                if (response.data.image) {
                    this.generatedImage = response.data.image;
                } else {
                    alert('Failed to generate image. Please try again.');
                }
            } catch (error) {
                console.error('Error generating image:', error);
                alert('There was an error generating the image. Please try again.');
            } finally {
                this.isLoading = false;
            }
        },
        regenerateImage() {
            this.promptText = '';
            this.generatedImage = null;
            this.referenceImage = null;
            this.aspectRatio = 'portrait';
            this.selectedStyle = 'No style';
        },
        confirmImage() {
            if (this.generatedImage) {
                // Agrega el mensaje con la imagen al estado global en lugar de emitir evento
                addMessage({
                    role: 'bot',
                    content: '',
                    image: this.generatedImage
                });
                this.regenerateImage();
            } else {
                alert('No image generated to confirm.');
            }
        },
        ratioClass(ratio) {
            return [
                'flex', 'items-center', 'justify-center', 'px-2', 'py-1', 'rounded-xl', 'focus:outline-none', 'transition', 'text-xs',
                this.aspectRatio === ratio ? 'bg-white bg-opacity-20 text-white hover:bg-white/30' : 'bg-slate-400 bg-opacity-40 text-gray-200 hover:bg-gray-600'
            ];
        },
        styleClass(styleName) {
            return [
                'flex', 'flex-col', 'items-center', 'p-1', 'rounded-xl', 'focus:outline-none', 'transition', 'text-xs',
                this.selectedStyle === styleName ? 'bg-white bg-opacity-20 text-white hover:bg-white/30' : 'bg-slate-400 bg-opacity-40 text-gray-200 hover:bg-gray-600'
            ];
        }
    },
};
</script>


<style scoped>
.scrollbar-thin::-webkit-scrollbar {
    width: 12px;
}

.scrollbar-thin::-webkit-scrollbar-track {
    background: transparent;
}

.scrollbar-thin::-webkit-scrollbar-thumb {
    background-color: rgba(15, 23, 42, 0.2);
    border-radius: 6px;
    border: 3px solid transparent;
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

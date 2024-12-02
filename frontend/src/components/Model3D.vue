<template>
    <div ref="canvasContainer" class="w-full h-full"></div>
  </template>
  
  <script>
  import * as THREE from 'three';
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';

  
  export default {
    mounted() {
      this.initThreeJS();
    },
    methods: {
      initThreeJS() {
        // Escena
        const scene = new THREE.Scene();
  
        // Cámara
        const camera = new THREE.PerspectiveCamera(
          75,
          this.$el.clientWidth / this.$el.clientHeight,
          0.1,
          1000
        );

        // Posición de la camara

        camera.position.z = 1;
        camera.position.y = 1.5;
        camera.position.x = 0;
  
        // Renderizador
        const renderer = new THREE.WebGLRenderer({ antialias: true });
        renderer.setSize(this.$el.clientWidth, this.$el.clientHeight);
        renderer.setClearColor(0x111827); // Fondo oscuro
        this.$refs.canvasContainer.appendChild(renderer.domElement);
  
        // Luz
        const light = new THREE.AmbientLight(0xffffff, 1);
        scene.add(light);
  
        // Cargar modelo 3D
        const loader = new GLTFLoader();
        loader.load('/src/assets/models/674aeeae8dc7c6e19d387ee0.glb', (gltf) => {
          scene.add(gltf.scene);
          animate();
        });
  
        // Animación
        const animate = () => {
          requestAnimationFrame(animate);
          renderer.render(scene, camera);
        };
      },
    },
  };
  </script>
  
  <style scoped>
  /* Estilos personalizados si es necesario */
  </style>
  
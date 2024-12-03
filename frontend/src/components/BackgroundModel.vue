
<template>
    <div ref="backgroundContainer" class="absolute inset-0 z-0"></div>
  </template>
  
  <script>
  import * as THREE from 'three';
  import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
  import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';
  
  export default {
    name: 'BackgroundModel',
    mounted() {
      this.initThreeJS();
    },
    methods: {
      initThreeJS() {
        // Crear la escena
        const scene = new THREE.Scene();
  
        // Configuración de la cámara
        const fov = 75; // Campo de visión
        const aspect = window.innerWidth / window.innerHeight; // Proporción de aspecto
        const near = 0.1; // Plano cercano
        const far = 1000; // Plano lejano
        const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);
  
        // Posición inicial de la cámara
        camera.position.set(-10, 10, 50); // (x, y, z)
        camera.lookAt(0, 0, 0); // La cámara mira al origen de la escena
  
        // Crear el renderizador
        const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
        renderer.setSize(window.innerWidth, window.innerHeight);
        renderer.setPixelRatio(window.devicePixelRatio);
        renderer.setClearColor(0x000000, 0); // Fondo transparente
        this.$refs.backgroundContainer.appendChild(renderer.domElement);
  
        // Configurar controles de órbita (opcional)
        const controls = new OrbitControls(camera, renderer.domElement);
        controls.enableDamping = true; // Habilitar amortiguación
        controls.dampingFactor = 0.05;
        controls.enablePan = false; // Deshabilitar paneo
        controls.enableZoom = false; // Deshabilitar zoom
  
        // Añadir luz ambiental
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.1); // Luz blanca suave
        scene.add(ambientLight);
  
        // Opcional: Añadir luz direccional para resaltar el modelo
        const directionalLight = new THREE.DirectionalLight(0xffffff, 0.1);
        directionalLight.position.set(10, 10, 10);
        scene.add(directionalLight);
  
        // Cargar el modelo 3D de fondo
        const loader = new GLTFLoader();
        loader.load(
          '/src/assets/models/cozy_room.glb', // Ruta al modelo de fondo
          (gltf) => {
            const model = gltf.scene;
  
            // Posición del modelo
            model.position.set(-10, -15, 0); // Centrar el modelo en la escena
  
            // Escala del modelo
            model.scale.set(30, 30, 30); // Ajusta según sea necesario
  
            // Rotación del modelo (opcional)
            // model.rotation.y = THREE.MathUtils.degToRad(0); // Rotar si es necesario
  
            // Añadir el modelo a la escena
            scene.add(model);
  
            // Iniciar la animación después de cargar el modelo
            animate();
          },
          undefined,
          (error) => {
            console.error('Error al cargar el modelo de fondo:', error);
          }
        );
  
        // Función de animación
        const animate = () => {
          requestAnimationFrame(animate);
          controls.update(); // Actualizar controles de órbita
          renderer.render(scene, camera);
        };
  
        // Manejar el redimensionamiento de la ventana
        window.addEventListener('resize', () => {
          const width = window.innerWidth;
          const height = window.innerHeight;
          camera.aspect = width / height;
          camera.updateProjectionMatrix();
          renderer.setSize(width, height);
        });
      },
    },
  };
  </script>
  
  <style scoped>
  /* Asegurar que el contenedor ocupe toda la pantalla */
  .absolute.inset-0 {
    pointer-events: none; /* Permitir interacción con elementos superpuestos */
  }
  </style>
  
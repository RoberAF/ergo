<!-- src/components/Model3D.vue -->
<template>
  <div ref="canvasContainer" class="w-full h-full z-0"></div>
</template>

<script>
import * as THREE from 'three';
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/examples/jsm/controls/OrbitControls.js';

export default {
  mounted() {
    this.initThreeJS();
  },
  methods: {
    initThreeJS() {
      // Crear la escena
      const scene = new THREE.Scene();

      // Configuración de la cámara
      const fov = 60;
      const aspect = this.$el.clientWidth / this.$el.clientHeight;
      const near = 0.1;
      const far = 1000;
      const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);

      // Posición inicial de la cámara
      camera.position.set(0, 1.0, 5);
      camera.lookAt(0, 0, 0);

      // Crear el renderizador
      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(this.$el.clientWidth, this.$el.clientHeight);
      renderer.setPixelRatio(window.devicePixelRatio);
      renderer.setClearColor(0x000000, 0);
      this.$refs.canvasContainer.appendChild(renderer.domElement);

      // Configurar controles de órbita
      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.05;
      controls.target.set(0, 0, 0);
      controls.update();

      // Añadir luz ambiental
      const ambientLight = new THREE.AmbientLight(0xffffff, 1);
      scene.add(ambientLight);

      // Añadir luz direccional (opcional)
      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
      directionalLight.position.set(5, 10, 7.5);
      scene.add(directionalLight);

      // Variables para animación
      let mixer = null;
      const clock = new THREE.Clock();

      // Cargar el modelo 3D
      const loader = new GLTFLoader();
      loader.load(
        '/models/ana_idle.glb/', // Ruta correcta desde la carpeta public
        (gltf) => {
          const model = gltf.scene;

          // Posición del modelo
          model.position.set(0, -5.5, 1);

          // Escala del modelo
          model.scale.set(4, 4, 4);

          // Añadir el modelo a la escena
          scene.add(model);

          // Configurar el AnimationMixer
          mixer = new THREE.AnimationMixer(model);
          if (gltf.animations && gltf.animations.length) {
            gltf.animations.forEach((clip) => {
              const action = mixer.clipAction(clip);
              action.play();
            });
          }

          // Iniciar la animación después de cargar el modelo
          animate();
        },
        undefined,
        (error) => {
          console.error('Error al cargar el modelo:', error);
        }
      );

      // Función de animación
      const animate = () => {
        requestAnimationFrame(animate);
        const delta = clock.getDelta();
        if (mixer) mixer.update(delta);
        controls.update();
        renderer.render(scene, camera);
      };

      // Manejar el redimensionamiento de la ventana
      window.addEventListener('resize', () => {
        const width = this.$el.clientWidth;
        const height = this.$el.clientHeight;
        camera.aspect = width / height;
        camera.updateProjectionMatrix();
        renderer.setSize(width, height);
      });
    },
  },
};
</script>

<style scoped>
/* Estilos personalizados si es necesario */
</style>

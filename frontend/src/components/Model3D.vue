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
      // Escena
      const scene = new THREE.Scene();

      // Cámara
      const camera = new THREE.PerspectiveCamera(
        20,
        this.$el.clientWidth / this.$el.clientHeight,
        0.1,
        1000
      );

      // Posición de la cámara
      camera.position.set(0, 0, 0);
      camera.lookAt(0, 0, -5); // Asegurar que la cámara mira hacia el modelo

      // Renderizador
      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(this.$el.clientWidth, this.$el.clientHeight);
      renderer.setPixelRatio(window.devicePixelRatio);
      renderer.setClearColor(0x111827); // Fondo oscuro
      this.$refs.canvasContainer.appendChild(renderer.domElement);

      // Controles de órbita (opcional)
      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true; // Habilitar amortiguación
      controls.dampingFactor = 0.05;

      // Luz ambiental
      const ambientLight = new THREE.AmbientLight(0xffffff, 1);
      scene.add(ambientLight);

      // Cargar modelo 3D
      const loader = new GLTFLoader();
      loader.load(
        '/src/assets/models/674aeeae8dc7c6e19d387ee0.glb',
        (gltf) => {
          // Posicionar el modelo enfrente de la cámara
          gltf.scene.position.set(-1.2, -1.2, -5);

          // Opcional: ajustar escala y rotación si es necesario
          // gltf.scene.scale.set(1, 1, 1);
          // gltf.scene.rotation.y = THREE.MathUtils.degToRad(0);

          // Añadir el modelo a la escena
          scene.add(gltf.scene);

          // Iniciar la animación después de cargar el modelo
          animate();
        },
        undefined,
        (error) => {
          console.error('Error al cargar el modelo:', error);
        }
      );

      // Animación
      const animate = () => {
        requestAnimationFrame(animate);
        controls.update(); // Actualizar controles si los estás utilizando
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

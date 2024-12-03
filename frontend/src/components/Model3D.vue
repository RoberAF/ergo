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
      const fov = 60; // Campo de visión (puedes ajustarlo para cambiar la perspectiva)
      const aspect = this.$el.clientWidth / this.$el.clientHeight; // Proporción de aspecto
      const near = 0.1; // Plano cercano
      const far = 1000; // Plano lejano
      const camera = new THREE.PerspectiveCamera(fov, aspect, near, far);

      // Posición inicial de la cámara
      // Ajusta estos valores para mover la cámara más cerca/lejos o en diferentes direcciones
      camera.position.set(0, 1., 5); // (x, y, z)
      camera.lookAt(0, 0, 0); // La cámara mira al origen de la escena

      // Crear el renderizador
      const renderer = new THREE.WebGLRenderer({ antialias: true });
      renderer.setSize(this.$el.clientWidth, this.$el.clientHeight);
      renderer.setPixelRatio(window.devicePixelRatio);
      renderer.setClearColor(0x000000, 0);
      this.$refs.canvasContainer.appendChild(renderer.domElement);

      // Configurar controles de órbita (opcional)
      const controls = new OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true; // Habilitar amortiguación para una mejor experiencia
      controls.dampingFactor = 0.05;
      controls.target.set(0, 0, 0); // Punto al que la cámara está mirando
      controls.update();

      // Añadir luz ambiental
      const ambientLight = new THREE.AmbientLight(0xffffff, 1); // Luz blanca suave
      scene.add(ambientLight);

      // Opcional: Añadir luz direccional para resaltar el modelo
      const directionalLight = new THREE.DirectionalLight(0xffffff, 0.5);
      directionalLight.position.set(5, 10, 7.5);
      scene.add(directionalLight);

      // Cargar el modelo 3D
      const loader = new GLTFLoader();
      loader.load(
        '/src/assets/models/674aeeae8dc7c6e19d387ee0.glb',
        (gltf) => {
          const model = gltf.scene;

          // Posición del modelo
          // Ajusta estos valores para mover el modelo en el espacio (izquierda/derecha, arriba/abajo, adelante/atrás)
          model.position.set(0, -5.5, 1); // Centrar el modelo en la escena

          // Escala del modelo
          // Ajusta estos valores para aumentar o reducir el tamaño del modelo
          model.scale.set(4, 4, 4); // Duplicar el tamaño del modelo

          // Rotación del modelo
          // Descomenta y ajusta si necesitas rotar el modelo
          // model.rotation.y = THREE.MathUtils.degToRad(45); // Rotar 45 grados en el eje Y

          // Añadir el modelo a la escena
          scene.add(model);

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
        controls.update(); // Actualizar los controles de órbita
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

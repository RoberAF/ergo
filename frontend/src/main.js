import { createApp } from 'vue'
import './index.css'
import App from './App.vue'
import router from './router';

createApp(App)
  .use(router) // Integrar el router
  .mount('#app');

import './assets/main.css'
import 'bootstrap/dist/css/bootstrap.css';

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'
import piniaPluginPersistedstate from 'pinia-plugin-persistedstate'

import { library } from '@fortawesome/fontawesome-svg-core';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { Pie, Bar } from 'vue-chartjs';

library.add(fas);
const app = createApp(App)
const pinia = createPinia()
pinia.use(piniaPluginPersistedstate)
app.use(pinia)
app.use(router)
app.component('pie-chart', Pie);
app.component('bar-chart', Bar)
app.component('font-awesome-icon', FontAwesomeIcon)
app.mount('#app')

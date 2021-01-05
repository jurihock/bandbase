import { createApp } from 'vue';
import axios from 'axios';

import 'bootstrap';
import 'flatpickr/dist/flatpickr.min.css'; // import before tabler
import '@tabler/core/dist/css/tabler.min.css';
import '@tabler/core/dist/css/tabler-vendors.min.css';
import 'feather-icons/dist/feather.min.js';

import App from '@/App.vue';
import config from '@/config.js';
import router from '@/router.js';

// TODO: axios.interceptors.response.use
//       https://blog.sqreen.com/authentication-best-practices-vue

axios.defaults.baseURL = config.backend;
axios.defaults.timeout = config.timeout;
axios.defaults.withCredentials = config.cors;

createApp(App).use(router).mount('#app');

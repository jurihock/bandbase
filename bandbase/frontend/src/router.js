import { createWebHistory, createRouter } from 'vue-router';
import axios from 'axios';

import DashboardPage from '@/components/pages/DashboardPage.vue';
import AboutPage from '@/components/pages/AboutPage.vue';

import LoginScreen from '@/components/screens/LoginScreen.vue';
import LogoutScreen from '@/components/screens/LogoutScreen.vue';

const auth = (to, from, next) => {
  axios.get('/session/check')
       .then(response => next())
       .catch(error => next('/login'));
};

const routes = [
  {
    path: '/login',
    name: 'LoginScreen',
    component: LoginScreen,
  },
  {
    path: '/logout',
    name: 'LogoutScreen',
    component: LogoutScreen,
  },
  {
    path: '/',
    name: 'DashboardPage',
    component: DashboardPage,
    beforeEnter: auth,
  },
  {
    path: '/about',
    name: 'AboutPage',
    component: AboutPage,
    beforeEnter: auth,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;

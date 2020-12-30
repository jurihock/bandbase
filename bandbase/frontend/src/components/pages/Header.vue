<template>

  <header class="navbar navbar-expand-md navbar-light d-print-none">
    <div class="container-xl">

      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-menu">
        <span class="navbar-toggler-icon"></span>
      </button>

      <h1 class="navbar-brand navbar-brand-autodark d-none-navbar-horizontal pe-0 pe-md-3">
        <router-link :to="{ name: 'DashboardPage'}">{{ title }}</router-link>
      </h1>

      <div class="navbar-nav flex-row order-md-last">
        <div class="nav-item d-none d-md-flex me-3">
          <router-link :to="{ name: 'LogoutScreen'}" class="nav-link px-0">Abmelden</router-link>
        </div>
      </div>

      <!--<span class="nav-link-icon d-md-none d-lg-inline-block"></span>-->
      <!--<span class="nav-link-title"></span>-->

      <!--
      TODO
      https://github.com/vuejs/vue-router-next/issues/148
      <router-link :to="{ name: 'AboutPage'}" v-slot="{ href, route, navigate, isActive, isExactActive }">
        <li :class="[isActive && 'active']" class="nav-item">
          <a @click="navigate" :href="href" :class="[isActive && 'active']" class="nav-link">Gigs</a>
        </li>
      </router-link>
      -->

      <div class="collapse navbar-collapse" id="navbar-menu">
        <div class="d-flex flex-column flex-md-row flex-fill align-items-stretch align-items-md-center">
          <ul class="navbar-nav">
            <li class="nav-item">
              <router-link :to="{ name: 'AboutPage'}" active-class="active" class="nav-link">Gigs</router-link>
            </li>
            <li class="nav-item">
              <a href="#" active-class="active" class="nav-link">Notenlager</a>
            </li>
            <li class="nav-item">
              <a href="#" active-class="active" class="nav-link">Notenmappen</a>
            </li>
            <li class="nav-item">
              <a href="#" active-class="active" class="nav-link">Kontakte</a>
            </li>
            <li class="nav-item">
              <a href="#" active-class="active" class="nav-link">Statistik</a>
            </li>
          </ul>
        </div>
      </div>

    </div>
  </header>

</template>

<script>
import config from '@/config.js';

export default {
  name: 'Header',
  components: {},
  data: function() {
    return {
      title: ''
    }
  },
  props: {},
  methods: {},
  created: function() {
    this.title = config.band.name;
  }
}
</script>

<style scoped>
</style>

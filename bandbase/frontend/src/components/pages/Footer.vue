<template>

  <footer class="footer footer-transparent d-print-none">
    <div class="container">
      <div class="row text-center align-items-center flex-row-reverse">
        <div class="col-lg-auto ms-lg-auto">
          <ul class="list-inline list-inline-dots mb-0">
            <li class="list-inline-item">
              <router-link :to="{ name: 'LoginScreen'}" class="link-secondary">Anmelden</router-link>
            </li>
            <li class="list-inline-item">
              <router-link :to="{ name: 'LogoutScreen'}" class="link-secondary">Abmelden</router-link>
            </li>
          </ul>
        </div>
        <div class="col-12 col-lg-auto mt-3 mt-lg-0">
          <ul class="list-inline list-inline-dots mb-0">
            <li class="list-inline-item">
              <span v-html="version"></span>
            </li>
            <li class="list-inline-item">
              <span v-html="copyright"></span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </footer>

</template>

<script>
import config from '@/config.js';

export default {
  name: 'Pages',
  components: {},
  data: function() {
    return {
      version: '',
      copyright: ''
    }
  },
  props: {},
  methods: {},
  created: function() {
    this.version = config.bandbase.name + ' v' + config.bandbase.version;
    this.copyright = config.bandbase.copyright;
  }
}
</script>

<style scoped>
</style>

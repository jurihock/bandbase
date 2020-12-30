<template>
  <Screen>
    <template v-slot:content>
      <div v-if="ready">
        <div v-if="error" class="empty">
          <p class="empty-title">{{ title }}</p>
          <p class="empty-subtitle text-muted">
            Die Abmeldung ist leider fehlgeschlagen.<br>
            Bitte versuche es erneut...
          </p>
          <div class="empty-action">
            <a href="/logout" class="btn btn-warning">Abmelden</a>
          </div>
        </div>
        <div v-else class="empty">
          <p class="empty-title">{{ title }}</p>
          <p class="empty-subtitle text-muted">
            Du bist nun abgemeldet.<br>
            Tschüß bis zum nächsten Mal!
          </p>
          <div class="empty-action">
            <a href="/login" class="btn btn-primary">Anmelden</a>
          </div>
        </div>
      </div>
      <div v-else>
        <div class="empty">
          <p class="empty-title">{{ title }}</p>
          <p class="empty-action">
            <div class="spinner-border" role="status"></div>
          </p>
        </div>
      </div>
    </template>
  </Screen>
</template>

<script>
import Screen from '@/components/screens/Screen.vue';
import config from '@/config.js';
import axios from 'axios';

export default {
  name: 'LoginScreen',
  components: { Screen },
  data: function() {
    return {
      title: '',
      ready: false,
      error: false
    }
  },
  props: {},
  methods: {},
  created: function()
  {
    this.title = config.band.name;
  },
  mounted: function()
  {
    axios.get('/session/logout')
         .then(response => this.error = false)
         .catch(error => this.error = true)
         .then(() => setTimeout(() => this.ready = true, 500));
  }
}
</script>

<style scoped>
</style>

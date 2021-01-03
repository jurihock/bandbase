<template>
  <Screen>
    <template v-slot:content>
      <form class="card card-md" autocomplete="off" v-on:submit.prevent="on_form_submit">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">{{ title }}</h2>
          <div class="mb-2">
            <input required
                   class="form-control" v-bind:class="{ 'is-invalid': error }"
                   type="password" autocomplete="off" placeholder="Passwort"
                   ref="secret"
                   v-model="secret"
                   v-on:click="on_secret_click">
          </div>
          <div class="form-footer">
            <button class="btn w-100" v-bind:class="[ error ? 'btn-danger' : 'btn-primary' ]" type="submit">Anmelden</button>
          </div>
        </div>
      </form>
    </template>
  </Screen>
</template>

<script>
import Screen from '@/components/parts/Screen.vue';
import config from '@/config.js';
import axios from 'axios';

export default {
  name: 'LoginScreen',
  components: { Screen },
  data: function() {
    return {
      title: config.band.name,
      secret: '',
      error: false
    }
  },
  props: {},
  mounted: function()
  {
    this.focus();
  },
  methods: {
    on_form_submit: function() {
      axios.post('/session/login', { secret: this.secret })
           .then(response => this.$router.push('/'))
           .catch(error => this.error = true, this.focus(), this.select());
    },
    on_secret_click: function() {
      this.select();
    },
    select: function() {
      this.$refs.secret.setSelectionRange(
        0, this.$refs.secret.value.length);
    },
    focus: function() {
      this.$refs.secret.focus();
    }
  }
}
</script>

<style scoped>
</style>

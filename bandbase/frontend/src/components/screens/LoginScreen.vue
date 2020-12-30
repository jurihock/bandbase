<template>
  <Screen>
    <template v-slot:content>
      <form class="card card-md" autocomplete="off" @submit.prevent="submit">
        <div class="card-body">
          <h2 class="card-title text-center mb-4">{{ title }}</h2>
          <div class="mb-2">
            <input required
                   class="form-control" :class="{ 'is-invalid': error }"
                   type="password" autocomplete="off" placeholder="Passwort"
                   ref="secret" v-model="secret"
                   @click="select">
          </div>
          <div class="form-footer">
            <button class="btn w-100" :class="[ error ? 'btn-danger' : 'btn-primary' ]" type="submit">Anmelden</button>
          </div>
        </div>
      </form>
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
      secret: '',
      error: false
    }
  },
  props: {},
  methods: {
    submit: function() {
      axios.post('/session/login', { secret: this.secret })
           .then(response => this.$router.push('/'))
           .catch(error => this.error = true, this.focus(), this.select());
    },
    focus: function() {
      this.$refs.secret.focus();
    },
    select: function() {
      this.$refs.secret.setSelectionRange(
        0, this.$refs.secret.value.length);
    }
  },
  created: function()
  {
    this.title = config.band.name;
  },
  mounted: function()
  {
    this.focus();
  }
}
</script>

<style scoped>
</style>

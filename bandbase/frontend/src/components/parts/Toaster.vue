<template>
  <div class="toast-container position-absolute top-0 end-0 p-2">
    <Toast v-for="(toast, id) in toasts"
           v-bind:key="id"
           v-bind:id="id"
           v-bind:subject="toast.subject"
           v-bind:message="toast.message"
           v-on:open="on_toast_open"
           v-on:pause="on_toast_pause"
           v-on:resume="on_toast_resume"
           v-on:close="on_toast_close"/>
  </div>
</template>

<script>
import Toast from '@/components/parts/Toast.vue';
import toaster from '@/toaster.js';
import { v4 as uuid } from 'uuid';

export default {
  name: 'Toaster',
  components: { Toast },
  data: function() {
    return {
      toasts: {}
    }
  },
  props: {},
  mounted: function() {
    toaster.on('toast',   (message) => this.on_toast_create('toast',   message));
    toaster.on('success', (message) => this.on_toast_create('success', message));
    toaster.on('warning', (message) => this.on_toast_create('warning', message));
    toaster.on('error',   (message) => this.on_toast_create('error',   message));
  },
  methods: {
    on_toast_create: function(subject, message) {
      const id = uuid();
      this.toasts[id] = {
        subject: subject,
        message: message,
        timeout: null
      };
    },
    on_toast_open: function(id) {
      if (!this.toasts.hasOwnProperty(id)) return;
      const close = () => this.on_toast_close(id);
      this.toasts[id].timeout = setTimeout(close, 5000);
    },
    on_toast_pause: function(id) {
      if (!this.toasts.hasOwnProperty(id)) return;
      clearTimeout(this.toasts[id].timeout);
    },
    on_toast_resume: function(id) {
      if (!this.toasts.hasOwnProperty(id)) return;
      const close = () => this.on_toast_close(id);
      this.toasts[id].timeout = setTimeout(close, 1500);
    },
    on_toast_close: function(id) {
      if (!this.toasts.hasOwnProperty(id)) return;
      delete this.toasts[id];
    }
  }
}
</script>

<style scoped>
</style>

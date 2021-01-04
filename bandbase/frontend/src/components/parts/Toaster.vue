<template>
  <div class="toast-container position-absolute top-0 end-0 p-2">
    <Toast v-for="toast in toasts"
           v-bind:id="toast.id"
           v-bind:subject="toast.subject"
           v-bind:message="toast.message"
           v-on:close="on_toast_closing"/>
  </div>
</template>

<script>
import Toast from '@/components/parts/Toast.vue';
import toaster from '@/toaster.js';
import _remove from 'lodash/remove';

export default {
  name: 'Toaster',
  components: { Toast },
  data: function() {
    return {
      toasts: []
    }
  },
  props: {},
  mounted: function() {
    toaster.on('toast',   (message) => this.on_toast_event('toast',   message));
    toaster.on('success', (message) => this.on_toast_event('success', message));
    toaster.on('warning', (message) => this.on_toast_event('warning', message));
    toaster.on('error',   (message) => this.on_toast_event('error',   message));
  },
  methods: {
    roll_the_dice: function() {
      return (Date.now() + Math.random()).toString();
    },
    on_toast_closing: function(id) {
      _remove(this.toasts, toast => toast.id === id);
    },
    on_toast_event: function(subject, message) {
      this.toasts.push({
        id: this.roll_the_dice(),
        subject: subject,
        message: message
      });
    }
  }
}
</script>

<style scoped>
</style>

<template>
  <div class="toast d-flex align-items-center show p-0 mb-2"
       ref="toast"
       v-bind:class="toast.class"
       v-bind:style="toast.background.current ? 'background-color:' + toast.background.current : ''"
       v-on:mouseenter="on_mouse_enter"
       v-on:mouseleave="on_mouse_leave"
       v-on:click="on_mouse_click">
    <div class="toast-body"
         v-html="toast.message"></div>
  </div>
</template>

<script>
export default {
  name: 'Toast',
  components: {},
  data: function() {
    return {
      timeout: null,
      toast: {
        message: null,
        class: null,
        background: {
          native: null,
          patched: null,
          current: null
        }
      }
    }
  },
  props: {
    id: String,
    subject: String,
    message: String
  },
  mounted: function() {
    this.timeout = setTimeout(this.close, 5000);
    this.toast.message = this.get_toast_message();
    this.toast.class = this.get_toast_class();
    this.toast.background = this.get_toast_background();
  },
  methods: {
    parse_rgba_color: function(value) {
      var rgba = value.split('(')[1].split(')')[0].split(',');
      if (rgba.length < 4) rgba.put('1');
      rgba[0] = parseInt(rgba[0]);
      rgba[1] = parseInt(rgba[1]);
      rgba[2] = parseInt(rgba[2]);
      rgba[3] = parseFloat(rgba[3]);
      return rgba;
    },
    build_rgba_color: function(rgba) {
      return 'rgba(' + rgba.map(_ => _.toString()).join(',') + ')';
    },
    get_toast_background: function() {
      var background = {
        native: null,
        patched: null,
        current: null
      };
      try {
        var native = this.parse_rgba_color(window
          .getComputedStyle(this.$refs.toast)
          .getPropertyValue('background-color'));
        var patched = [...native];
        patched[patched.length - 1] = 1;
        background.native = this.build_rgba_color(native);
        background.patched = this.build_rgba_color(patched);
        background.current = background.native;
      }
      catch (error) {
        background.native = null;
        background.patched = null;
        background.current = null;
        console.error('Unable to parse the native toast background color!', error);
      }
      return background;
    },
    get_toast_class: function() {
      if (this.subject == 'error')
        return 'alert alert-danger';
      if (this.subject == 'warning')
        return 'alert alert-warning';
      if (this.subject == 'success')
        return 'alert alert-success';
      return 'alert alert-info';
    },
    get_toast_message: function() {
      return this.message.replaceAll('<a ', '<a class="alert-link" ');
    },
    on_mouse_enter: function() {
      clearTimeout(this.timeout);
      this.toast.background.current = this.toast.background.patched;
    },
    on_mouse_leave: function() {
      this.timeout = setTimeout(this.close, 1500);
      this.toast.background.current = this.toast.background.native;
    },
    on_mouse_click: function() {
      this.close();
    },
    close: function() {
      this.$emit('close', this.id);
    }
  }
}
</script>

<style scoped>
.toast {
  cursor: pointer;
}
</style>

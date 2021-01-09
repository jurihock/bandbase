<template>
  <div class="toast d-flex align-items-center show p-0 mb-2"
       ref="toast"
       v-bind:style="background.current ? 'background-color:' + background.current : ''"
       v-bind:class="class"
       v-on:mouseenter="on_mouse_enter"
       v-on:mouseleave="on_mouse_leave"
       v-on:click="on_mouse_click">
    <div class="toast-body"
         v-html="html"></div>
  </div>
</template>

<script>
export default {
  name: 'Toast',
  components: {},
  data: function() {
    return {
      html: null,
      class: null,
      background: {
        transparent: null,
        opaque: null,
        current: null
      }
    }
  },
  props: {
    id: String,
    subject: String,
    message: String
  },
  created: function() {
    // the toast class needs to be set early,
    // to determine the proper background color
    // from computed style in the mount section
    this.class = this.get_toast_class();
  },
  mounted: function() {
    this.html = this.get_toast_html();
    this.background = this.get_toast_background();
    this.$emit('open', this.id);
  },
  methods: {
    parse_rgba_color: function(value) {
      var rgba = value.split('(')[1].split(')')[0].split(',');
      if (rgba.length < 4) rgba.push('1');
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
        transparent: null,
        opaque: null,
        current: null
      };
      try {
        var native = this.parse_rgba_color(window
          .getComputedStyle(this.$refs.toast)
          .getPropertyValue('background-color'));
        var transparent = [...native];
        var opaque = [...native];
        transparent[transparent.length - 1] = 0.85;
        opaque[opaque.length - 1] = 1;
        background.transparent = this.build_rgba_color(transparent);
        background.opaque = this.build_rgba_color(opaque);
        background.current = background.transparent;
      }
      catch (error) {
        background.transparent = null;
        background.opaque = null;
        background.current = null;
        console.error('Unable to identify the toast background color!', error);
      }
      return background;
    },
    get_toast_class: function() {
      if (this.subject == 'error')
        return 'alert alert-important alert-danger';
      if (this.subject == 'warning')
        return 'alert alert-important alert-warning';
      if (this.subject == 'success')
        return 'alert alert-important alert-success';
      return 'alert alert-important alert-info';
    },
    get_toast_html: function() {
      return this.message.replaceAll('<a ', '<a class="alert-link" ');
    },
    on_mouse_enter: function() {
      this.background.current = this.background.opaque;
      this.$emit('pause', this.id);
    },
    on_mouse_leave: function() {
      this.background.current = this.background.transparent;
      this.$emit('resume', this.id);
    },
    on_mouse_click: function() {
      this.$emit('close', this.id);
    }
  }
}
</script>

<style scoped>
.toast {
  cursor: pointer;
}
:deep() a.alert-link {
  color: #fff;
  font-weight: bold;
  text-decoration: underline;
}
</style>

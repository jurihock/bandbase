<template>
  <div v-bind:class="[offset, width]">
    <slot/>
  </div>
</template>

<script>
function LayoutData(value) {
  var values = value.split(',');
  console.assert(~[1, 2].indexOf(values.length));
  if (values.length < 2) values.unshift(0);
  this.offset = values[0] ? 'offset-sm-' + values[0] : '';
  this.width = values[1] ? 'col-sm-' + values[1] : '';
}

export default {
  name: 'FormFieldgap',
  components: {},
  data: function() {
    return new LayoutData(this.layout)
  },
  props: {
    layout: {
      type: String,
      required: false,
      default: '2,10'
    }
  },
  methods: {}
}
</script>

<style scoped>
</style>

<template>
  <input type="text"
         class="filter"
         ref="filter"
         v-model="value"
         v-on:click="on_filter_click"
         v-on:input="on_filter_input">
</template>

<script>
export default {
  name: 'DynamicTableFilter',
  components: {},
  data: function() {
    return {
      value: ''
    }
  },
  props: {
    name: String,
  },
  methods: {
    on_filter_click: function() {
      this.$refs.filter.setSelectionRange(
        0, this.$refs.filter.value.length);
    },
    on_filter_input: function() {
      this.$emit('trigger', this.name, this.value);
    }
  }
}
</script>

<style scoped>
input.filter {
  width: 100%;
}
</style>

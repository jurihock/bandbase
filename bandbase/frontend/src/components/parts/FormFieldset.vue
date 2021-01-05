<template>
  <fieldset>
    <legend v-if="legend" class="card-title">{{ legend }}</legend>
    <slot/>
  </fieldset>
</template>

<script>
export default {
  name: 'FormFieldset',
  components: {},
  data: function() {
    return {}
  },
  props: {
    legend: String
  },
  methods: {}
}
</script>

<style scoped>
</style>

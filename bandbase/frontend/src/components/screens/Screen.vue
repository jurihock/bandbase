<template>
  <div class="flex-fill d-flex flex-column justify-content-center py-4">
    <div class="container-tight py-6">
      <slot name="content"/>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Screen',
  components: {},
  data: function() {
    return {}
  },
  props: {},
  methods: {},
  mounted: function()
  {
    document.body.classList.add(
      'border-top-wide',
      'border-primary',
      'd-flex',
      'flex-column');
  },
  unmounted: function()
  {
    document.body.classList.remove(
      'border-top-wide',
      'border-primary',
      'd-flex',
      'flex-column');
  }
}
</script>

<style scoped>
</style>

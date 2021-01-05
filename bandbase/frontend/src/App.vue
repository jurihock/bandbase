<template>
  <router-view/>
</template>

<script>
export default {
  name: 'App',
  components: {},
  props: {}
}
</script>

<style>
/* fix flatpickr font size, which is a bit too large */
.flatpickr-current-month {
  font-size: 123%; /* instead of 135% */
}
</style>

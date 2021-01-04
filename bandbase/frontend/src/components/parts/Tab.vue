<template>
  <div v-show="selected" class="tab-pane active show">
    <slot/>
  </div>
</template>

<script>
export default {
  name: 'Tab',
  components: {},
  data: function() {
    return {
      selected: false
    }
  },
  props: {
    title: String
  },
  created: function() {
    this.$parent.tabs.push(this);
  },
  methods: {}
}
</script>

<style scoped>
</style>

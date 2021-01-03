<template>
  <span v-html="svg"></span>
</template>

<script>
import feather from 'feather-icons';

export default {
  name: 'Icon',
  components: {},
  data: function() {
    return {
      svg: feather.icons[this.name].toSvg()
    }
  },
  props: {
    name: String
  },
  created: function() {
  }
}
</script>

<style scoped>
</style>

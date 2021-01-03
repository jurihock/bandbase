<template>
  <Page>
    <template v-slot:title>
      About Bandbase
    </template>
    <template v-slot:content>
      ABOUT
    </template>
  </Page>
</template>

<script>
import Page from '@/components/parts/Page.vue';

export default {
  name: 'AboutPage',
  components: { Page },
  data: function() {
    return {}
  },
  props: {},
  methods: {}
}
</script>

<style scoped>
</style>

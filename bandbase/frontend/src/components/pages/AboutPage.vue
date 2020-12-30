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
import Page from '@/components/pages/Page.vue';

export default {
  name: 'AboutPage',
  components: { Page },
  props: {}
}
</script>

<style scoped>
</style>

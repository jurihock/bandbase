<template>
  <Page>
    <template v-slot:title>
      Dashboard
    </template>
    <template v-slot:content>
      DASH
    </template>
  </Page>
</template>

<script>
import Page from '@/components/pages/Page.vue';

export default {
  name: 'DashboardPage',
  components: { Page },
  props: {}
}
</script>

<style scoped>
</style>

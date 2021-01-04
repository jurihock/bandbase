<template>
  <Page>
    <template v-slot:title>
      Dashboard
    </template>
    <template v-slot:content>
      <Tabster>
        <Tab title="foo">FOO</Tab>
        <Tab title="bar">BAR</Tab>
      </Tabster>
    </template>
  </Page>
</template>

<script>
import Page from '@/components/parts/Page.vue';
import Tabster from '@/components/parts/Tabster.vue';
import Tab from '@/components/parts/Tab.vue';

export default {
  name: 'DashboardPage',
  components: { Page, Tabster, Tab },
  data: function() {
    return {}
  },
  props: {},
  methods: {}
}
</script>

<style scoped>
</style>

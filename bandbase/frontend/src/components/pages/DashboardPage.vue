<template>
  <Page>
    <template v-slot:title>
      Dashboard
    </template>
    <template v-slot:content>
      <Tabs>
        <Tab title="foo">FOO</Tab>
        <Tab title="bar">BAR</Tab>
      </Tabs>
    </template>
  </Page>
</template>

<script>
import Page from '@/components/parts/Page.vue';
import Tabs from '@/components/parts/Tabs.vue';
import Tab from '@/components/parts/Tab.vue';

export default {
  name: 'DashboardPage',
  components: { Page, Tabs, Tab },
  data: function() {
    return {}
  },
  props: {},
  methods: {}
}
</script>

<style scoped>
</style>

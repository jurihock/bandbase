<template>
  <Page>
    <template v-slot:title>
      Dashboard
    </template>
    <template v-slot:content>
      <DynamicTable source="contacts"
                    v-bind:columns="{
                      name:     { text: 'Name',      width: 5 },
                      category: { text: 'Kategorie', width: 3 },
                      comment:  { text: 'Kommentar', width: 3 }}"/>
    </template>
  </Page>
</template>

<script>
import Page from '@/components/parts/Page.vue';
import DynamicTable from '@/components/parts/DynamicTable.vue';

export default {
  name: 'DashboardPage',
  components: { Page, DynamicTable },
  data: function() {
    return {}
  },
  props: {},
  methods: {}
}
</script>

<style scoped>
</style>

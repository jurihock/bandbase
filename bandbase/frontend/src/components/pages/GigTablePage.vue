<template>
  <Page>
    <template v-slot:title>Gigs</template>
    <template v-slot:content>
      <DynamicTable source="gigs"
                    v-bind:columns="{
                      name:     { text: 'Name',      width: 5 },
                      date:     { text: 'Datum',     width: 1 },
                      location: { text: 'Ort',       width: 2 },
                      comment:  { text: 'Kommentar', width: 3 }}"/>
    </template>
  </Page>
</template>

<script>
import Page from '@/components/parts/Page.vue';
import DynamicTable from '@/components/parts/DynamicTable.vue';

export default {
  name: 'GigTablePage',
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

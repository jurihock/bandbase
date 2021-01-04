<template>
  <Page>
    <template v-slot:title>Gigs</template>
    <template v-slot:content>
      <DynamicTable source="gigs"
                    v-bind:columns="{
                      name:     { title: 'Name',      width: 5 },
                      date:     { title: 'Datum',     width: 1 },
                      location: { title: 'Ort',       width: 2 },
                      comment:  { title: 'Kommentar', width: 3 }}"/>
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

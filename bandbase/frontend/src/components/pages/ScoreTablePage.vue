<template>
  <Page>
    <template v-slot:title>Notenlager</template>
    <template v-slot:content>
      <DynamicTable source="scores"
                    v-bind:columns="{
                      name:    { title: 'Name',      width: 5 },
                      stockid: { title: 'LGR',       width: 1, tooltip: 'Lagerkennung: Buchstabe, Nummer, Zähler' },
                      edition: { title: 'AUS',       width: 1, tooltip: 'Ausgabe' },
                      gsm:     { title: 'GSM',       width: 2, tooltip: 'Genre, Stil, Metronomtext' },
                      comment: { title: 'Kommentar', width: 2 }}"/>
    </template>
  </Page>
</template>

<script>
import Page from '@/components/parts/Page.vue';
import DynamicTable from '@/components/parts/DynamicTable.vue';

export default {
  name: 'ScoreTablePage',
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

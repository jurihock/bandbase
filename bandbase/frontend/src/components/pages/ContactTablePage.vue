<template>
  <Page>
    <template v-slot:title>Kontakte</template>
    <template v-slot:floor>
      <div class="btn-list">
        <router-link v-bind:to="{ name: 'AddContactPage'}" class="btn btn-primary">Neuer Kontakt anlegen...</router-link>
        <router-link v-bind:to="{ name: 'AddContactPage'}" class="btn btn-primary">Bandmusiker</router-link>
      </div>
    </template>
    <template v-slot:content>
      <DynamicTable source="contacts"
                    v-bind:columns="{
                      name:     { title: 'Name',      width: 5 },
                      category: { title: 'Kategorie', width: 3 },
                      comment:  { title: 'Kommentar', width: 3 }}"/>
    </template>
  </Page>
</template>

<script>
import Page from '@/components/parts/Page.vue';
import DynamicTable from '@/components/parts/DynamicTable.vue';

export default {
  name: 'ContactTablePage',
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

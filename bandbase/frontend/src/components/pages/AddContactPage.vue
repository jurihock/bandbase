<template>
  <Page>
    <template v-slot:title>Neuer Kontakt anlegen</template>
    <template v-slot:content>
      <ContactForm actions="post"
                   v-on:post="create"
                   v-model:data="data"/>
    </template>
  </Page>
</template>

<script>
import ContactSetup from '@/components/forms/ContactSetup.js';
import ContactForm from '@/components/forms/ContactForm.vue';
import Page from '@/components/parts/Page.vue';

export default {
  name: 'AddContactPage',
  components: { Page, ContactForm },
  props: {},
  setup: ContactSetup,
  mounted: function() {
    this.data.category = '0';
  }
}
</script>

<style scoped>
</style>

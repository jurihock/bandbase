<template>
  <Page>
    <template v-slot:title>Kontakt bearbeiten</template>
    <template v-slot:content>
      <ContactForm actions="post,delete"
                   v-on:post="update"
                   v-on:delete="delet"
                   v-model:data="data"/>
    </template>
  </Page>
</template>

<script>
import ContactSetup from '@/components/forms/ContactSetup.js';
import ContactForm from '@/components/forms/ContactForm.vue';
import Page from '@/components/parts/Page.vue';

export default {
  name: 'EditContactPage',
  components: { Page, ContactForm },
  props: {},
  setup: ContactSetup,
  mounted: function() {
    this.read();
  }
}
</script>

<style scoped>
</style>

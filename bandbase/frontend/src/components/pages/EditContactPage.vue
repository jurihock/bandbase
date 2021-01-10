<template>
  <Page>
    <template v-slot:title>Kontakt bearbeiten</template>
    <template v-slot:floor>
      <div class="btn-list">
        <Download class="btn btn-white"
                  v-bind:files="[`contact/${id}.vcf`]">
          Dateien
        </Download>
      </div>
    </template>
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
import Download from '@/components/parts/Download.vue';
import Page from '@/components/parts/Page.vue';

export default {
  name: 'EditContactPage',
  components: { ContactForm, Download, Page },
  props: {},
  setup: ContactSetup,
  mounted: function() {
    this.read();
  }
}
</script>

<style scoped>
</style>

<template>
  <div class="page">
    <PageHeader/>
    <div class="content">
      <div class="container-xl">
        <div class="page-header">
          <div class="row align-items-center">
            <div class="col">
              <h2 class="page-title">
                <slot name="title"/>
              </h2>
            </div>
            <div class="col-auto ms-auto d-print-none">
              <slot name="floor"/>
            </div>
          </div>
        </div>
        <div class="row row-cards">
          <div class="col-12">
            <slot name="content"/>
          </div>
        </div>
      </div>
      <Toaster/>
      <PageFooter/>
    </div>
  </div>
</template>

<script>
import _get from 'lodash/get';

import toaster from '@/toaster.js';

import PageHeader from '@/components/parts/PageHeader.vue';
import PageFooter from '@/components/parts/PageFooter.vue';
import Toaster from '@/components/parts/Toaster.vue';

export default {
  name: 'Page',
  components: { PageHeader, PageFooter, Toaster },
  props: {},
  mounted: function() {
    if ('toasts' in this.$route.params) {
      const toasts = JSON.parse(this.$route.params.toasts);
      for (var i = 0; i < toasts.length; i++) {
        const toast = toasts[i];
        toaster.subject(toast.subject, toast.message);
      }
    }
  }
}
</script>

<style scoped>
</style>

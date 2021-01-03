<template>
  <div class="page">
    <Header/>

<!--  <div class="toast-container position-absolute top-0 end-0 p-3">
    <div class="toast d-flex align-items-center show" role="alert" aria-live="assertive" aria-atomic="true" data-autohide="false" data-bs-toggle="toast">
      <div class="toast-body">
        Hello, world! This is a toast message.
      </div>
      <button type="button" class="ms-2 btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
    </div>
    <div class="toast show" role="alert" aria-live="assertive" aria-atomic="true" data-autohide="false" data-bs-toggle="toast">
      <div class="toast-header">
        <span class="avatar avatar-xs me-2" style="background-image: url(...)"></span>
        <strong class="me-auto">Mallory Hulme</strong>
        <small>7 mins ago</small>
        <button type="button" class="ms-2 btn-close" data-bs-dismiss="toast" aria-label="Close"></button>
      </div>
      <div class="toast-body">
        This is another toast message.
      </div>
    </div>
  </div>-->

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
              <slot name="extra"/>
            </div>
          </div>
        </div>
        <div class="row row-cards">
          <div class="col-12">
            <slot name="content"/>
          </div>
        </div>
      </div>
      <Footer/>
    </div>
  </div>
</template>

<script>
import Header from '@/components/pages/Header.vue';
import Footer from '@/components/pages/Footer.vue';

export default {
  name: 'Page',
  components: { Header, Footer },
  props: {}
}
</script>

<style scoped>
</style>

<template>
  <form v-bind:autocomplete="autocomplete"
        v-on:submit.prevent="$emit('post')">
    <div class="card">
      <ul v-if="tabs.length" class="nav nav-tabs nav-tabs-alt">
        <li v-for="(tab, index) in tabs" class="nav-item">
          <a class="nav-link"
             v-bind:class="(index == selected) ? 'active' : ''"
             v-on:click="select(index)">
            {{ tab.title }}
          </a>
        </li>
      </ul>
      <div class="card-body">
        <div v-bind:class="tabs.length ? 'tab-content' : ''">
          <slot/>
        </div>
      </div>
      <div v-if="actions" class="card-footer text-end">
        <div class="d-flex">
          <button v-if="~actions.indexOf('delete')"
                  v-on:click="$emit('delete')"
                  class="btn btn-outline-danger"
                  type="button">Löschen...</button>
          <button v-if="~actions.indexOf('post')"
                  class="btn btn-primary ms-auto"
                  type="submit">Fertigstellen</button>
        </div>
      </div>
    </div>
  </form>
</template>

<script>
export default {
  name: 'Form',
  components: {},
  data: function() {
    return {
      tabs: [],
      selected: null
    }
  },
  props: {
    actions: {
      type: String,
      required: false,
      default: ''
    },
    autocomplete: {
      type: String,
      required: false,
      default: 'off'
    }
  },
  mounted: function() {
    this.select(0);
  },
  methods: {
    select: function(index) {
      const ok = (0 <= index && index < this.tabs.length);
      this.selected = ok ? index : null;
      for (var i = 0; i < this.tabs.length; i++) {
        this.tabs[i].selected = (i == index);
      }
    }
  }
}
</script>

<style scoped>
/* https://github.com/twbs/bootstrap/issues/20643 */
@media (min-width: 576px) {
  :deep() .col-form-label {
    text-align: right;
  }
}
:deep() .form-label.required:after,
:deep() .col-form-label.required:after {
  content: "*";
  margin-left: .25rem;
  color: #d63939;
}
:deep() .form-control.required {
  /* border-color: #d63939; */
}
</style>

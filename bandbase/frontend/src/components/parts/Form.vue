<template>
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
      <form>
        <div v-bind:class="tabs.length ? 'tab-content' : ''">
          <slot/>
        </div>
      </form>
    </div>
  </div>
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
/deep/ .form-label.required:after,
/deep/ .col-form-label.required:after {
  content: "*";
  margin-left: .25rem;
  color: #d63939;
}
/deep/ .form-control.required {
  border-color: #d63939;
}
</style>

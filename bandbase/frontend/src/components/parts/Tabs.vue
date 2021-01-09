<template>
  <div class="card">
    <ul class="nav nav-tabs nav-tabs-alt">
      <li v-for="(tab, index) in tabs" class="nav-item">
        <a class="nav-link"
           v-bind:class="(index == selected) ? 'active' : ''"
           v-on:click="select(index)">
          {{ tab.title }}
        </a>
      </li>
    </ul>
    <div class="card-body">
      <div class="tab-content">
        <slot/>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Tabs',
  components: {},
  data: function() {
    return {
      tabs: [],
      selected: null
    }
  },
  props: {},
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
</style>

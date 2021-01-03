<template>
  <div class="d-flex flex-wrap">
    <nav class="flex-fill">
      <ul class="pagination justify-content-start m-0">
        <li class="page-item">
          <span class="page-link" style="cursor:default"
                title="Datensatzbereich" data-toggle="tooltip" data-placement="top"
                v-if="total > 0">
              <span v-html="roi.start"></span>&ndash;<span v-html="roi.end"></span>
              von
              <span v-html="total"></span>
          </span>
        </li>
      </ul>
    </nav>
    <nav class="flex-fill">
      <ul class="pagination justify-content-end m-0">
        <li class="page-item" v-bind:class="!can.first && 'disabled'">
          <button class="page-link chevron" type="button"
                  title="Erste Seite" data-toggle="tooltip" data-placement="top"
                  v-on:click="on_first_click">
            <!--<Icon name="chevrons-left"/>-->
            &laquo;
          </button>
        </li>
        <li class="page-item" v-bind:class="!can.prev && 'disabled'">
          <button class="page-link chevron" type="button"
                  title="Vorherige Seite" data-toggle="tooltip" data-placement="top"
                  v-on:click="on_prev_click">
            <!--<Icon name="chevron-left"/>-->
            &lsaquo;
          </button>
        </li>
        <li class="page-item" v-bind:class="total < 1 && 'disabled'">
          <input class="page-link text-center limit" type="text"
                 title="Max. pro Seite" data-toggle="tooltip" data-placement="top"
                 ref="limit"
                 v-bind:value="page.limit"
                 v-on:click="on_limit_click"
                 v-on:input="on_limit_input"/>
        </li>
        <li class="page-item" v-bind:class="!can.next && 'disabled'">
          <button class="page-link chevron" type="button"
                  title="Nächste Seite" data-toggle="tooltip" data-placement="top"
                  v-on:click="on_next_click">
            <!--<Icon name="chevron-right"/>-->
            &rsaquo;
          </button>
        </li>
        <li class="page-item" v-bind:class="!can.last && 'disabled'">
          <button class="page-link chevron" type="button"
                  title="Letzte Seite" data-toggle="tooltip" data-placement="top"
                  v-on:click="on_last_click">
            <!--<Icon name="chevrons-right"/>-->
            &raquo;
          </button>
        </li>
      </ul>
    </nav>
  </div>
</template>

<script>
import Icon from '@/components/parts/Icon.vue';

export default {
  name: 'DynamicTablePager',
  components: { Icon },
  data: function() {
    return {
      page: {
        limit: this.limit,
        offset: 0
      },
      roi: {
        start: 0,
        end: 0
      },
      can:
      {
        first: false,
        last: false,
        prev: false,
        next: false
      }
    }
  },
  props: {
    limit: Number,
    total: Number
  },
  watch: {
    'limit': function() {
      this.page.offset = 0;
      this.page.limit = this.limit;
      this.update();
    },
    'total': function() {
      this.page.offset = 0;
      this.update();
    }
  },
  created: function()
  {
    this.update();
  },
  methods: {
    on_limit_click: function() {
      this.$refs.limit.setSelectionRange(0, this.$refs.limit.value.length);
    },
    on_limit_input: function() {
      if (!/^[1-9]\d*$/.test(this.$refs.limit.value)) {
        this.$refs.limit.value = this.page.limit;
        this.$refs.limit.setSelectionRange(0, this.$refs.limit.value.length);
        return;
      }
      const limit = Math.max(this.$refs.limit.value, 1);
      const pages = Math.ceil(this.total / limit);
      const page0 = Math.ceil(this.page.offset / limit);
      const page1 = Math.min(Math.max(page0, 0), pages - 1);
      const offset = page1 * limit;
      this.page.limit = limit;
      this.page.offset = offset;
      this.update();
      this.trigger();
    },
    on_first_click: function() {
      const offset0 = this.page.offset;
      const offset1 = 0;
      this.page.offset = offset1;
      this.update();
      if (offset0 != offset1) {
        this.trigger();
      }
    },
    on_last_click: function() {
      const pages = Math.ceil(this.total / this.page.limit);
      const page = Math.max(pages - 1, 0);
      const offset0 = this.page.offset;
      const offset1 = page * this.page.limit;
      this.page.offset = offset1;
      this.update();
      if (offset0 != offset1) {
        this.trigger();
      }
    },
    on_prev_click: function() {
      const pages = Math.ceil(this.total / this.page.limit);
      const page0 = Math.ceil(this.page.offset / this.page.limit);
      const page1 = Math.min(Math.max(page0 - 1, 0), pages - 1);
      const offset0 = this.page.offset;
      const offset1 = page1 * this.page.limit;
      this.page.offset = offset1;
      this.update();
      if (offset0 != offset1) {
        this.trigger();
      }
    },
    on_next_click: function() {
      const pages = Math.ceil(this.total / this.page.limit);
      const page0 = Math.ceil(this.page.offset / this.page.limit);
      const page1 = Math.min(Math.max(page0 + 1, 0), pages - 1);
      const offset0 = this.page.offset;
      const offset1 = page1 * this.page.limit;
      this.page.offset = offset1;
      this.update();
      if (offset0 != offset1) {
        this.trigger();
      }
    },
    update: function() {
      this.roi.start = this.page.offset + 1;
      this.roi.end = Math.min(this.page.offset + this.page.limit, this.total);
      this.can.first = this.can.prev = this.page.offset > 0;
      this.can.last = this.can.next = (this.total - this.page.offset) > this.page.limit;
    },
    trigger: function() {
      this.$emit('trigger', this.page.limit, this.page.offset);
    }
  }
}
</script>

<style scoped>
input.limit {
  cursor: text;
  width: 5em;
}
button.chevron {
}
</style>

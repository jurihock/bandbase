<template>
  <div class="card">
    <div class="table-responsive my-0">
      <table class="table table-hover table-vcenter not-table-sm card-table">
        <colgroup>
          <col v-for="column in table.columns"
               v-bind:width="get_column_width_percent(columns[column.name].width)"/>
          <col v-bind:width="get_column_width_percent(1)"/>
        </colgroup>
        <thead>
          <tr>
            <th v-for="column in table.columns"
                v-bind:title="columns[column.name].tooltip">
              {{ columns[column.name].title }}
            </th>
            <th>&nbsp;</th>
          </tr>
          <tr>
            <th v-for="column in table.columns">
              <DynamicTableFilter v-bind:name="column.name" v-on:trigger="on_filter_trigger"/>
            </th>
            <th>&nbsp;</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="row in table.rows">
            <td v-for="column in table.columns">
              <span v-if="(row.badge != null) && (row.badge.column == column.name)"
                    class="badge me-1"
                    v-bind:style="row.badge.style"
                    v-bind:title="row.badge.tooltip">
                {{ row.badge.text }}
              </span>
              {{ row.values[column.name] }}
            </td>
            <td>...</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div class="card-footer py-1">
      <DynamicTablePager ref="pager"
                         v-bind:limit="query.limit"
                         v-bind:total="table.total"
                         v-on:trigger="on_pager_trigger"/>
    </div>
  </div>
</template>

<script>
import DynamicTableFilter from '@/components/parts/DynamicTableFilter.vue';
import DynamicTablePager from '@/components/parts/DynamicTablePager.vue';
import config from '@/config.js';
import axios from 'axios';
import _debounce from 'lodash/debounce';

export default {
  name: 'DynamicTable',
  components: { DynamicTableFilter, DynamicTablePager },
  data: function() {
    return {
      url: config.backend + '/table/' + this.source,
      query: {
        filter: {},
        sort: {},
        limit: 0,
        offset: 0
      },
      table: {
        columns: [],
        rows: [],
        total: 0
      }
    }
  },
  props: {
    source: String,
    columns: {
      type: Object,
      required: true
    }
  },
  created: function()
  {
    this.probe();
  },
  methods: {
    get_column_width_percent: function(width) {
      const total = Object.entries(this.columns).reduce(
                    (sum, col) => sum + col[1].width, 1);
      console.assert(total == 12);
      return 100 * width / total + '%';
    },
    on_filter_trigger: function(column, value) {
      this.query.filter[column] = value;
      this.query.offset = 0;
      this.update();
    },
    on_pager_trigger: function(limit, offset) {
      this.query.limit = limit;
      this.query.offset = offset;
      this.update();
    },
    on_probe_callback: function(response) {
      this.table.columns = response.data.columns;
      this.query.sort = response.data.query.sort;
      this.query.limit = response.data.query.limit;
    },
    on_probe_error: function(error) {
      this.table.rows = [];
      this.table.total = 0;
      console.log(error);
    },
    on_update_callback: function(response) {
      this.table.rows = response.data.rows;
      this.table.total = response.data.total;
    },
    on_update_error: function(error) {
      this.table.rows = [];
      this.table.total = 0;
      console.log(error);
    },
    probe: function() {
      axios.post(this.url, {probe: true})
           .then(this.on_probe_callback)
           .then(() => {
             axios.post(this.url, this.query)
                  .then(this.on_update_callback)
                  .catch(this.on_update_error);
           })
           .catch(this.on_probe_error);
    },
    update: _debounce(function() {
      axios.post(this.url, this.query)
           .then(this.on_update_callback)
           .catch(this.on_update_error);
    }, 500)
  }
}
</script>

<style scoped>
</style>

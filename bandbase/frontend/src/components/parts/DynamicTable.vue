<template>
  <div v-show="error" class="alert alert-important alert-danger" role="alert">
    <p>Die Tabelle konnte leider nicht geladen werden!</p>
    <p><var>{{ error }}</var></p>
  </div>
  <div v-show="!pending && !error" class="card">
    <div class="table-responsive my-0">
      <table class="table table-sm table-hover table-vcenter card-table">
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
            <td>
              <div class="d-grid">
                <router-link class="btn btn-white"
                             v-if="source == 'contacts'"
                             v-bind:title="'Kontakt „' + row.values.name + '“ bearbeiten'"
                             v-bind:to="{ name: 'EditContactPage', params: {id: row.id}}">...</router-link>
                <!-- TODO ISSUE #4 -->
                <!-- TODO ISSUE #9 -->
              </div>
            </td>
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
import axios from 'axios';
import _debounce from 'lodash/debounce';
import _get from 'lodash/get';

import config from '@/config.js';

import DynamicTableFilter from '@/components/parts/DynamicTableFilter.vue';
import DynamicTablePager from '@/components/parts/DynamicTablePager.vue';

export default {
  name: 'DynamicTable',
  components: { DynamicTableFilter, DynamicTablePager },
  data: function() {
    return {
      pending: true,
      error: null,
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
      this.error = null;
    },
    on_probe_error: function(error) {
      this.table.rows = [];
      this.table.total = 0;
      this.error = _get(error, 'response.data.detail', error.message);
      console.error(error);
    },
    on_update_callback: function(response) {
      this.table.rows = response.data.rows;
      this.table.total = response.data.total;
      this.error = null;
    },
    on_update_error: function(error) {
      this.table.rows = [];
      this.table.total = 0;
      this.error = _get(error, 'response.data.detail', error.message);
      console.error(error);
    },
    probe: function() {
      axios.post(this.url, {probe: true})
           .then(this.on_probe_callback)
           .then(() => {
             axios.post(this.url, this.query)
                  .then(this.on_update_callback)
                  .then(() => { this.pending = false })
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

<template>
  <label class="col-form-label"
         v-bind:class="[ widths[0], required ? 'required' : '' ]"
         v-bind:for="id">
    {{ label }}
  </label>
  <div v-bind:class="widths[1]">
    <select class="form-select"
            v-bind:autocomplete="autocomplete"
            v-bind:class="required ? 'required' : ''"
            v-bind:disabled="pending || error"
            v-bind:id="id"
            v-bind:required="required"
            v-model="value">
      <option v-for="item in list.items"
              v-bind:value="item.id">
        {{ item.name }}
      </option>
    </select>
    <div v-if="help && !error" v-html="help" class="form-text"></div>
    <div v-if="error" class="form-text alert alert-important alert-danger" role="alert">
      <p>Die Liste konnte leider nicht geladen werden!</p>
      <p><var>{{ error }}</var></p>
    </div>
  </div>
</template>

<script>
import config from '@/config.js';
import axios from 'axios';
import { v4 as uuid } from 'uuid';

export default {
  name: 'FormList',
  components: {},
  data: function() {
    return {
      pending: true,
      error: null,
      url: config.backend + '/list/' + this.source,
      id: 'uuid:' + uuid(),
      widths: this.layout.split(',').map(width => 'col-sm-' + width),
      list: {
        items: [],
        default: null,
        nullable: null
      }
    }
  },
  props: {
    autocomplete: {
      type: String,
      required: false,
      default: 'off'
    },
    help: {
      type: String,
      required: false,
      default: null
    },
    label: {
      type: String,
      required: false,
      default: null
    },
    layout: {
      type: String,
      required: false,
      default: '2,10'
    },
    required: {
      type: Boolean,
      required: false,
      default: false
    },
    source: {
      type: String,
      required: true
    },
    value: {
      type: String,
      required: false,
      default: null
    }
  },
  created: function () {
    this.update();
  },
  methods: {
    on_update_callback: function(response) {
      const dummy = {id: null, name: '&mdash;', pinned: true};
      const nullable = response.data.nullable;
      const default_ = response.data.default;
      const items = nullable ? response.data.items : response.data.items;
      this.list.nullable = nullable;
      this.list.default = default_;
      this.list.items = items;
      this.error = null;
    },
    on_update_error: function(error) {
      this.list.items = [];
      this.list.default = null;
      this.list.nullable = null;
      this.error = error.toString();
      console.error(error);
    },
    update: function () {
       axios.post(this.url)
            .then(this.on_update_callback)
            .then(() => { this.pending = false })
            .catch(this.on_update_error);
    }
  }
}
</script>

<style scoped>
</style>

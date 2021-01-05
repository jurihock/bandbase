<template>
  <label class="col-form-label"
         v-bind:class="[ widths[0], required ? 'required' : '' ]"
         v-bind:for="id + ':latitude'">
    {{ label }}
  </label>
  <div v-bind:class="widths[1]">
    <div class="input-group">
      <label class="input-group-text"
             v-bind:for="id + ':latitude'">
        <span title="Breitengrad">B</span>
      </label>
      <input class="form-control"
             v-bind:autocomplete="autocomplete"
             v-bind:class="required ? 'required' : ''"
             v-bind:id="id + ':latitude'"
             v-bind:placeholder="placeholder"
             v-bind:required="required"
             v-bind:type="type"
             v-model="value.latitude">
      <label class="input-group-text"
             v-bind:for="id + ':longitude'">
        <span title="Längengrad">L</span>
      </label>
      <input class="form-control"
             v-bind:autocomplete="autocomplete"
             v-bind:class="required ? 'required' : ''"
             v-bind:id="id + ':longitude'"
             v-bind:placeholder="placeholder"
             v-bind:required="required"
             v-bind:type="type"
             v-model="value.longitude">
    </div>
    <div v-if="help" v-html="help" class="form-text"></div>
  </div>
</template>

<script>
import { v4 as uuid } from 'uuid';

export default {
  name: 'FormGeopoint',
  components: {},
  data: function() {
    return {
      id: 'uuid:' + uuid(),
      widths: this.layout.split(',').map(width => 'col-sm-' + width)
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
    placeholder: {
      type: String,
      required: false,
      default: null
    },
    required: {
      type: Boolean,
      required: false,
      default: false
    },
    type: {
      type: String,
      required: false,
      default: 'text'
    },
    value: {
      type: Object,
      required: false,
      default: {
        latitude: null,
        longitude: null
      }
    }
  },
  methods: {}
}
</script>

<style scoped>
</style>

<template>
  <label v-if="widths[0]" class="col-form-label"
         v-bind:class="[ widths[0], required ? 'required' : '' ]"
         v-bind:for="id">
    {{ label }}
  </label>
  <div v-bind:class="widths[1]">
    <textarea class="form-control"
              v-bind:autocomplete="autocomplete"
              v-bind:class="[ required ? 'required' : '', wrap ? 'wrap-soft' : 'wrap-off']"
              v-bind:id="id"
              v-bind:placeholder="placeholder"
              v-bind:required="required"
              v-bind:rows="rows"
              v-bind:style="color ? 'background-color:' + color : ''"
              v-bind:wrap="wrap ? 'soft' : 'off'"
              v-model="value"></textarea>
    <div v-if="help" v-html="help" class="form-text"></div>
  </div>
</template>

<script>
import { v4 as uuid } from 'uuid';

export default {
  name: 'FormTextArea',
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
    color: {
      type: String,
      required: false,
      default: null
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
    rows: {
      type: String,
      required: false,
      default: '1'
    },
    value: {
      type: String,
      required: false,
      default: null
    },
    wrap: {
      type: Boolean,
      required: false,
      default: false
    },
  },
  methods: {}
}
</script>

<style scoped>
textarea.wrap-soft {
  resize: vertical;
  white-space: normal;
}
textarea.wrap-off {
  resize: vertical;
  white-space: pre;
}
</style>

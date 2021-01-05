<template>
  <label class="col-form-label"
         v-bind:class="[ widths[0], isrequired ? 'required' : '' ]"
         v-bind:for="id">
    {{ label }}
  </label>
  <div v-bind:class="widths[1]">
    <input class="form-control flatpickr-input"
           ref="input"
           v-bind:autocomplete="autocomplete"
           v-bind:class="isrequired ? 'required' : ''"
           v-bind:id="id"
           v-bind:placeholder="placeholder"
           v-bind:required="isrequired"
           v-bind:type="type"
           v-model="value">
    <div v-if="help" v-html="help" class="form-text"></div>
  </div>
</template>

<script>
import flatpickr from 'flatpickr';
import { German } from 'flatpickr/dist/l10n/de.js';
import { v4 as uuid } from 'uuid';

export default {
  name: 'FormTime',
  components: {},
  data: function() {
    return {
      id: 'uuid:' + uuid(),
      isrequired: this.required === 'true',
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
      default: 'HH:MM'
    },
    required: {
      type: String,
      required: false,
      default: 'false'
    },
    type: {
      type: String,
      required: false,
      default: 'text'
    },
    value: {
      type: String,
      required: false,
      default: null
    }
  },
  mounted: function() {
    flatpickr(this.$refs.input, {
      dateFormat: 'H:i',
      locale: German,
      enableTime: true,
      noCalendar: true,
      time_24hr: true
    });
  },
  methods: {}
}
</script>

<style scoped>
/* see also additional style fix in App.vue */
</style>

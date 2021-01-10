<template>

  <a v-bind:class="class"
     v-on:click="open">
    <slot/>
  </a>

  <div class="modal-backdrop fade"
       v-bind:class="idle ? 'hide' : 'show'">
  </div>

  <div class="modal modal-blur fade"
       v-bind:class="idle ? 'hide' : 'show'"
       v-on:click.self="close">
    <div class="modal-dialog modal-sm modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-body">

          <div class="modal-title">
            <slot/>
          </div>

          <div v-if="pending" class="progress">
            <div class="progress-bar progress-bar-indeterminate"></div>
          </div>

          <div v-if="!pending && !error" class="list-group">
            <a v-for="file in downloads"
               class="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
               v-bind:href="file.data"
               v-bind:download="file.name">
              {{ file.name }}
              <span v-if="file.size" class="badge bg-secondary rounded-pill">
                {{ file.size }}
              </span>
            </a>
          </div>

          <div v-if="error" class="form-text alert alert-important alert-danger m-0" role="alert">
            <p>Der Download ist leider fehlgeschlagen!</p>
            <p><var>{{ error }}</var></p>
          </div>

        </div>
        <div class="modal-footer">
          <button v-if="pending"
                  class="btn btn-primary"
                  type="button"
                  v-on:click="close">
            Abbrechen
          </button>
          <button v-if="!pending"
                  class="btn btn-primary"
                  type="button"
                  v-on:click="close">
            Schließen
          </button>
        </div>
      </div>
    </div>
  </div>

</template>

<script>
import axios from 'axios';
import { ref } from 'vue';

import config from '@/config.js';

function setup(props) {

  const files = props.files;

  const idle = ref(true);
  const pending = ref(false);
  const error = ref('');
  const downloads = ref([]);

  var cancel = axios.CancelToken.source();

  function dispose() {
    for (var i = 0; i < downloads.value.length; i++) {
      window.URL.revokeObjectURL(downloads.value[i].data);
    }
    downloads.value = [];
  }

  function parse(responses) {
    for (var i = 0; i < responses.length; i++) {
      const response = responses[i];

      var filename = files[i];
      try {
        const header = response.headers['content-disposition'];
        const regex = /filename="(?<filename>.*)"/;
        filename = regex.exec(header).groups.filename;
      }
      catch (e) {
        console.error('Unable to parse file name!', e);
      }

      var filesize = '';
      try {
        const KB = 1024;
        const MB = 1024 * 1024;
        if (response.data.size >= MB) {
          filesize = Math.round(response.data.size / MB) + ' MB';
        }
        else if (response.data.size >= KB) {
          filesize = Math.round(response.data.size / KB) + ' KB';
        }
        else {
          filesize = response.data.size + ' B';
        }
      }
      catch (e) {
        console.error('Unable to parse file size!', e);
      }

      const filedata = window.URL.createObjectURL(response.data);

      downloads.value.push({name: filename, size: filesize, data: filedata});
    }
  }

  function open() {
    cancel.cancel();
    dispose();
    idle.value = false;
    pending.value = true;

    cancel = axios.CancelToken.source();

    const requests = [];

    for (var i = 0; i < files.length; i++) {
      const url = `${config.backend}/file/${files[i]}`;
      const request = axios({
        url: url,
        method: 'get',
        responseType: 'blob',
        timeout: 10 * 1000,
        cancelToken: cancel.token
      });
      requests.push(request);
    }

    Promise.all(requests)
           .then(responses => {
             pending.value = false;
             error.value = '';
             parse(responses);
           })
           .catch(e => {
             pending.value = false;
             error.value = !axios.isCancel(e) ? e.toString() : '';
           });
  }

  function close() {
    cancel.cancel();
    dispose();
    idle.value = true;
  }

  return {
    idle,
    pending,
    error,
    downloads,
    open,
    close
  }
}

export default {
  name: 'Download',
  components: {},
  props: {
    class: {
      type: String,
      required: false,
      default: ''
    },
    files: {
      type: Array,
      required: true
    }
  },
  setup: setup
}
</script>

<style scoped>
.modal.hide,
.modal-backdrop.hide {
  display: none;
}
.modal.show,
.modal-backdrop.show {
  display: block;
}
</style>

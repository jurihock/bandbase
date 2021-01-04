import mitt from 'mitt';

const events = mitt();

const toaster = {
  toast: function(message) {
    events.emit('toast', message);
  },
  success: function(message) {
    events.emit('success', message);
  },
  warning: function(message) {
    events.emit('warning', message);
  },
  error: function(message) {
    events.emit('error', message);
  },
  on: function(event, callback) {
    events.on(event, callback);
  }
};

export default toaster;

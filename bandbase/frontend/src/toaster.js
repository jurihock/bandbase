import mitt from 'mitt';
import _toString from 'lodash/toString';

const events = mitt();

const toaster = {
  popup: function() {
    window.scrollTo(0, 0);
    return this;
  },
  subject: function(subject, message) {
    events.emit(_toString(subject), _toString(message));
    return this;
  },
  toast: function(message) {
    events.emit(_toString(message));
    return this;
  },
  success: function(message) {
    events.emit('success', _toString(message));
    return this;
  },
  warning: function(message) {
    events.emit('warning', _toString(message));
    return this;
  },
  error: function(message) {
    events.emit('error', _toString(message));
    return this;
  },
  on: function(event, callback) {
    events.on(event, callback);
  }
};

export default toaster;

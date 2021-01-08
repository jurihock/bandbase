import _replace from 'lodash/replace';
import _thru from 'lodash/thru';
import _trim from 'lodash/trim';

function string(value) {
  return _thru(_trim(value),
               result => result ? result : null);
}

function integer(value) {
  return _thru(parseInt(_trim(value)),
               result => !isNaN(result) ? result.toString() : null);
}

function float(value) {
  return _thru(parseFloat(_replace(_trim(value), ',', '.')),
               result => !isNaN(result) ? result.toString() : null);
}

function date(value) {
  return _thru(_trim(value),
               result => result ? result : null);
}

function time(value) {
  return _thru(_trim(value),
               result => result ? result : null);
}

export default {
  string,
  integer,
  float,
  date,
  time
};

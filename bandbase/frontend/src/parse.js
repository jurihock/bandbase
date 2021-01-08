import _replace from 'lodash/replace';
import _thru from 'lodash/thru';
import _trim from 'lodash/trim';

function string(value) {
  return _trim(value);
}

function integer(value) {
  return _thru(parseInt(_trim(value)),
               result => !isNaN(result) ? result.toString() : '');
}

function float(value) {
  return _thru(parseFloat(_replace(_trim(value), ',', '.')),
               result => !isNaN(result) ? result.toString() : '');
}

function date(value) {
  return _trim(value);
}

function time(value) {
  return _trim(value);
}

export default {
  string,
  integer,
  float,
  date,
  time
};

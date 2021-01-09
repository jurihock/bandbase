import axios from 'axios';
import { reactive } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import _get from 'lodash/get';

import config from '@/config.js';
import parse from '@/parse.js';
import toaster from '@/toaster.js';

import ContactData from '@/components/forms/ContactData.js';

function setup() {

  const route = useRoute();
  const router = useRouter();

  const id = _get(route, 'params.id', null);
  const data = reactive(ContactData());

  function copy(src, dst) {
    dst.name.first = parse.string(src.name.first);
    dst.name.last = parse.string(src.name.last);
    dst.name.full = parse.string(src.name.full);
    dst.address.street = parse.string(src.address.street);
    dst.address.house = parse.string(src.address.house);
    dst.address.city = parse.string(src.address.city);
    dst.address.zip = parse.string(src.address.zip);
    dst.address.country = parse.string(src.address.country);
    dst.details.phone.landline = parse.string(src.details.phone.landline);
    dst.details.phone.mobile = parse.string(src.details.phone.mobile);
    dst.details.fax = parse.string(src.details.fax);
    dst.details.email = parse.string(src.details.email);
    dst.details.website = parse.string(src.details.website);
    dst.geopoint.latitude = parse.float(src.geopoint.latitude);
    dst.geopoint.longitude = parse.float(src.geopoint.longitude);
    dst.birthdate = parse.date(src.birthdate);
    dst.category = parse.integer(src.category);
    dst.comment = parse.string(src.comment);
  }

  function create() {
    console.assert(!id);
    const url = config.backend + '/form/contact/create';
    copy(data, data);
    axios.post(url, data)
         .then(response => {
           const id = response.data.id;
           const name = response.data.name;
           const message = `Neuer Kontakt <a href="/contact/${id}">${name}</a> wurde angelegt.`;
           const toasts = JSON.stringify([{subject: 'success', message: message}]);
           router.push({name: 'ContactTablePage', params: {toasts: toasts}});
         })
         .catch(error => {
           const message = _get(error, 'response.data.detail', error.message);
           toaster.popup().error(message);
         });
  }

  function read() {
    console.assert(id);
    const url = config.backend + '/form/contact/read/' + id;
    axios.post(url)
         .then(response => {
           copy(response.data, data);
         })
         .catch(error => {
           const message = _get(error, 'response.data.detail', error.message);
           const toasts = JSON.stringify([{subject: 'error', message: message}]);
           router.push({name: 'ContactTablePage', params: {toasts: toasts}});
         });
  }

  function update() {
    console.assert(id);
    const url = config.backend + '/form/contact/update/' + id;
    copy(data, data);
    axios.post(url, data)
         .then(response => {
           const id = response.data.id;
           const name = response.data.name;
           const message = `Kontakt <a href="/contact/${id}">${name}</a> wurde gespeichert.`;
           const toasts = JSON.stringify([{subject: 'success', message: message}]);
           router.push({name: 'ContactTablePage', params: {toasts: toasts}});
         })
         .catch(error => {
           const message = _get(error, 'response.data.detail', error.message);
           toaster.popup().error(message);
         });
  }

  function delet() {
    if (!confirm('Soll dieser Datensatz unwiderruflich gelöscht werden?')) {
      return;
    }
    console.assert(id);
    const url = config.backend + '/form/contact/delete/' + id;
    axios.post(url)
         .then(response => {
           const name = response.data.name;
           const message = `Kontakt „${name}“ wurde gelöscht.`;
           const toasts = JSON.stringify([{subject: 'success', message: message}]);
           router.push({name: 'ContactTablePage', params: {toasts: toasts}});
         })
         .catch(error => {
           const message = _get(error, 'response.data.detail', error.message);
           toaster.popup().error(message);
         });
  }

  return {
    data,
    create,
    read,
    update,
    delet
  };
}

export default setup;

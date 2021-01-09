export default function ContactData() {
  return {
    name: {
      first: null,
      last: null,
      full: null
    },
    address: {
      street: null,
      house: null,
      city: null,
      zip: null,
      country: null
    },
    details: {
      phone: {
        landline: null,
        mobile: null
      },
      fax: null,
      email: null,
      website: null
    },
    geopoint: {
      latitude: null,
      longitude: null
    },
    birthdate: null,
    category: null,
    comment: null
  }
}

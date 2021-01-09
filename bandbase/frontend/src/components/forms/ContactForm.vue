<template>
  <Form v-bind:actions="actions">
    <FormFieldset legend="Name und Kategorie">
      <FormFieldrow>
        <FormText label="Kurzer Nachname"
                  help="(ohne Namenszusätze, z.B. Beethoven oder Smith)"
                  layout="2,4"
                  v-bind:required="true"
                  v-model:value="data.name.last"/>
        <FormText label="Vorname"
                  help="(nur bei Personen relevant)"
                  layout="2,4"
                  v-model:value="data.name.first"/>
      </FormFieldrow>
      <FormFieldrow>
        <FormText label="Langer Nachname"
                  help="(mit Namenszusätzen, z.B. van Beethoven oder Smith, Jr.)"
                  layout="2,4"
                  v-model:value="data.name.full"/>
        <FormDate label="Geburtsdatum"
                  help="(nur bei Personen relevant)"
                  layout="2,4"
                  v-model:value="data.birthdate"/>
      </FormFieldrow>
      <FormFieldrow>
        <FormList label="Kategorie"
                  source="contact/category"
                  layout="2,4"
                  v-bind:required="true"
                  v-model:value="data.category"/>
      </FormFieldrow>
    </FormFieldset>
    <FormFieldset legend="Anschrift">
      <FormFieldrow>
        <FormText label="Straße"
                  layout="2,4"
                  v-model:value="data.address.street"/>
        <FormText label="Haus"
                  layout="1,2"
                  v-model:value="data.address.house"/>
      </FormFieldrow>
      <FormFieldrow>
        <FormText label="Ort"
                  layout="2,4"
                  v-model:value="data.address.city"/>
        <FormText label="PLZ"
                  layout="1,2"
                  v-model:value="data.address.zip"/>
      </FormFieldrow>
      <FormFieldrow>
        <FormText label="Land"
                  help="(das Land, falls nicht Deutschland, jedoch kein Bundesland)"
                  layout="2,4"
                  v-model:value="data.address.country"/>
      </FormFieldrow>
      <FormFieldrow>
        <FormGeopoint label="Standort"
                      layout="2,7"
                      v-model:value="data.geopoint"/>
      </FormFieldrow>
    </FormFieldset>
    <FormFieldset legend="Kontaktdaten">
      <FormFieldrow>
        <FormText label="Festnetztelefon"
                  layout="2,4"
                  v-model:value="data.details.phone.landline"/>
        <FormText label="E-Mail"
                  layout="2,4"
                  v-model:value="data.details.email"/>
      </FormFieldrow>
      <FormFieldrow>
        <FormText label="Mobiltelefon"
                  layout="2,4"
                  v-model:value="data.details.phone.mobile"/>
        <FormText label="Webseite"
                  layout="2,4"
                  v-model:value="data.details.website"/>
      </FormFieldrow>
      <FormFieldrow>
        <FormText label="Fax"
                  layout="2,4"
                  v-model:value="data.details.fax"/>
      </FormFieldrow>
    </FormFieldset>
    <FormFieldset legend="Kommentar">
      <FormFieldrow>
        <FormTextArea layout="0,12"
                      color="#FFFF9933"
                      rows="5"
                      v-bind:wrap="true"
                      v-model:value="data.comment"/>
      </FormFieldrow>
    </FormFieldset>
  </Form>
</template>

<script>
import Forms from '@/components/parts/Forms.vue';

export default {
  name: 'ContactForm',
  components: { ...Forms },
  props: {
    actions: String,
    data: Object
  }
}
</script>

<style scoped>
</style>

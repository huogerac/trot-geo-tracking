<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <v-form>
        <v-text-field v-model="percurso" label="Novo percurso" required></v-text-field>

        <v-btn variant="flat" color="secondary" block @click="obterMinhaPosicao"> INICIAR </v-btn>
      </v-form>
      <p>latitude: {{ latitude }}</p>
      <p>longitude: {{ longitude }}</p>
    </v-responsive>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      percurso: "",
      latitude: null,
      longitude: null,
      date: null,
    }
  },
  methods: {
    geoSuccess(position) {
      this.latitude = position.coords.latitude
      this.longitude = position.coords.longitude
      this.date = new Date().getTime()
    },
    geoError(error) {
      console.log("Vish, deu ruim!", error)
    },
    obterMinhaPosicao() {
      navigator.geolocation.getCurrentPosition(this.geoSuccess, this.geoError)
    },
  },
}
</script>

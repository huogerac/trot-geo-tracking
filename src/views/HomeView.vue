<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <v-form>
        <v-text-field v-model="percurso" label="Novo percurso" required></v-text-field>

        <v-btn variant="flat" color="secondary" block @click="obterMinhaPosicao"> INICIAR </v-btn>
      </v-form>
      <p>latitude: {{ latitude }}</p>
      <p>longitude: {{ longitude }}</p>
      <p>Acurácia: {{ latLongAccuracy?.toFixed(2) }} m</p>
      <p>Altitude: {{ altitude }} m</p>
      <p>Acurácia da Altitude: {{ altitudeAccuracy }} m</p>
      <p>Heading: {{ heading }} °</p>
      <p>Velocidade: {{ speed }} m / s</p>
      <p>Timestamp: {{ timestamp }}</p>
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
      latLongAccuracy: null,
      heading: null,
      speed: null,
      altitude: null,
      altitudeAccuracy: null,
      timestamp: null,
      date: null,
    }
  },
  methods: {
    geoSuccess(position) {
      this.latitude = position.coords.latitude
      this.longitude = position.coords.longitude
      this.latLongAccuracy =  position.coords.accuracy

      this.heading =  position.coords.heading
      this.speed =  position.coords.speed

      this.altitude =  position.coords.altitude
      this.altitudeAccuracy =  position.coords.altitudeAccuracy

      this.timestamp = position.timestamp
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

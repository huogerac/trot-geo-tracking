<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <v-form>
        <v-text-field v-model="percurso" label="Novo percurso" required></v-text-field>

        <v-btn v-if="id == 0" variant="flat" color="secondary" block @click="iniciar">
          INICIAR
        </v-btn>
        <v-btn v-else variant="flat" color="secondary" block @click="parar"> PARAR </v-btn>
      </v-form>

      <h2>Posições: {{ positions.length }}</h2>
      <ul>
        <li v-for="(position, idx) in positions" :key="idx">
          ({{ position.latitude }}, {{ position.longitude }})
        </li>
      </ul>
    </v-responsive>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      id: 0,
      positions: [],
      percurso: "",
    }
  },
  methods: {
    geoSuccess(position) {
      const newPosition = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        latLongAccuracy: position.coords.accuracy,
        heading: position.coords.heading,
        speed: position.coords.speed,
        altitude: position.coords.altitude,
        altitudeAccuracy: position.coords.altitudeAccuracy,
        date: new Date().getTime(),
      }
      this.positions.push(newPosition)
    },
    geoError(error) {
      console.log("Vish, deu ruim!", error)
    },
    iniciar() {
      //navigator.geolocation.getCurrentPosition(this.geoSuccess, this.geoError)
      this.id = navigator.geolocation.watchPosition(this.geoSuccess, this.geoError)
    },
    parar() {
      navigator.geolocation.clearWatch(this.id)
      this.id = 0
    },
  },
}
</script>

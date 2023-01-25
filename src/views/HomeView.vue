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

      <p v-if="lastPosition">
        <span>latitude:</span><span>{{ lastPosition.latitude }}</span> <span>longitude:</span
        ><span>{{ lastPosition.longitude }}</span> <span>heading:</span
        ><span>{{ lastPosition.heading }}</span> <span>speed:</span
        ><span>{{ lastPosition.speed }}</span> <span>altitude:</span
        ><span>{{ lastPosition.altitude }}</span>
      </p>

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
import axios from "axios"
export default {
  data() {
    return {
      id: 0,
      lastPosition: {},
      positions: [],
      percurso: "",
    }
  },
  methods: {
    geoSuccess(position) {
      if (
        position.coords.latitude == this.lastPosition.latitude &&
        position.coords.longitude == this.lastPosition.longitude
      ) {
        return
      }
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
      this.lastPosition = newPosition
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
    async addGeolocation(lat, long) {
      const res = await axios.post(`http://localhost:3001/api/geolocation`, {
        latitude: lat,
        longitude: long,
      })
      this.geolocation.push(res.data)
    },
    eraseDb() {
      axios
        .get(`http://localhost:3001/api/geolocation`)
        .then((geolocation) => {
          geolocation.data.forEach((item) => {
            axios.delete(`http://localhost:3001/api/geolocation/${item.id}`)
          })
        })
        .finally((this.geolocation = []))
    },
  },
}
</script>

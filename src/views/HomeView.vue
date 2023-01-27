<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <v-form>
        <v-text-field v-model="trackName" label="Novo trackName" required></v-text-field>

        <v-btn v-if="geoId == 0" variant="flat" color="secondary" block @click="iniciar">
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
import TracksApi from "@/api/tracks.api"
import PositionsApi from "@/api/positions.api"

export default {
  data() {
    return {
      geoId: 0,
      trackId: 0,
      lastPosition: {},
      positions: [],
      trackName: "",
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
      const coords = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        latLongAccuracy: position.coords.accuracy,
        heading: position.coords.heading,
        speed: position.coords.speed,
        altitude: position.coords.altitude,
        altitudeAccuracy: position.coords.altitudeAccuracy,
        date: new Date().getTime(),
      }
      this.positions.push(coords)
      this.lastPosition = coords
      PositionsApi.addPosition(this.trackId, coords)
    },
    geoError(error) {
      console.log("Vish, deu ruim!", error)
    },
    iniciar() {
      TracksApi.addTrack(this.trackName || "novo trackName").then((newTrack) => {
        this.trackId = newTrack.id
        this.geoId = navigator.geolocation.watchPosition(this.geoSuccess, this.geoError)
      })
    },
    parar() {
      navigator.geolocation.clearWatch(this.geoId)
      this.geoId = 0
    },
  },
}
</script>

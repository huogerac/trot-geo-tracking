<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <h6>v2024-06-20-07:15</h6>
      <v-form>
        <v-text-field v-model="description" label="Nome da corrida" required></v-text-field>

        <p>selected circuit: {{ circuit_selected }}</p>
        <p>track_id: {{ track_id }}</p>
        <p>counter: {{ counter }}</p>

        <v-combobox
          v-model="circuit_selected"
          label="Circuito"
          :items="circuits"
          item-title="name"
          item-value="id"></v-combobox>

        <v-btn v-if="!track_id" variant="flat" color="secondary" block @click="iniciar">
          INICIAR
        </v-btn>
        <v-btn v-else variant="flat" color="secondary" block @click="parar"> PARAR </v-btn>
      </v-form>

      <v-btn color="primary" variant="flat" :to="{ name: 'PercursoDetalheView' }" class="my-4">
        Ver percurso
      </v-btn>

      <h2>Posições salvas: {{ lastSavedPositions.length }} / {{ tentativas }}</h2>

      <h3 v-if="lastSavedPositions">Map point viewer ({{ lastSavedPositions.length }})</h3>
      <open-layer-map-point-viewer
        v-if="lastSavedPositions"
        :positions-list="latLon"
        :center="center">
      </open-layer-map-point-viewer>

      <h2>Última posição <span v-if="lastPosition">OK</span></h2>
      <div v-if="lastPosition">
        <p>
          latitude:<em>{{ lastPosition.latitude }}</em>
        </p>
        <p>
          longitude:<em>{{ lastPosition.longitude }}</em>
        </p>
        <p>
          latLongAccuracy:<em>{{ lastPosition.latLongAccuracy }}</em>
        </p>
        <p>
          quality:<em>{{ lastPosition.quality }}</em>
        </p>
        <p>lastSavedPositions: {{ lastSavedPositions }}</p>
        <p>center: {{ center }}</p>
      </div>
    </v-responsive>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
//import { useLocationStore } from "@/store/locationStore"
import { useTrackStore } from "@/store/trackStore"
import OpenLayerMapPointViewer from "@/components/OpenLayerMapPointViewer.vue"

export default {
  components: {
    OpenLayerMapPointViewer,
  },
  setup() {
    // const locationStore = useLocationStore()
    const trackStore = useTrackStore()

    return {
      trackStore,
    }
  },
  data() {
    return {
      watch_id: null,
      circuit_selected: null,
      description: "",
      tentativas: 0,
      counter: 0,
      //percurso: "",
      //timer: null,
      //timerInterval_2min: 2 * 60 * 1000,
    }
  },
  computed: {
    //...mapState(useLocationStore, ["latLon", "lastPosition"]),
    ...mapState(useTrackStore, [
      "circuits",
      "track_id",
      "positionsSaved",
      "positionsIgnored",
      "lastPosition",
      "lastSavedPositions",
      "latLon",
    ]),
    center() {
      if (this.lastPosition) {
        return [this.lastPosition.longitude, this.lastPosition.latitude]
      }
      //this?.lastSavedPositions?.slice(-1)[0]
      return []
    },
  },
  mounted() {
    this.getCircuitos()
  },
  methods: {
    async getCircuitos() {
      console.log("obtendo circuitos", this.circuits)
      this.trackStore.getCircuitos()
      console.log("obtendo circuitos 2", this.circuits)
    },
    geoSuccess(position) {
      this.tentativas += 1
      this.counter = this.counter + 1
      const newPosition = {
        latitude: position.coords.latitude,
        longitude: position.coords.longitude,
        latLongAccuracy: position.coords.accuracy,
        heading: position.coords.heading,
        speed: position.coords.speed,
        altitude: position.coords.altitude,
        altitudeAccuracy: position.coords.altitudeAccuracy,
        dateTime: new Date().toISOString(),
      }
      // this.locationStore.savePositions(newPosition)
      // console.log(newPosition)
      this.trackStore.salvarPosicoes(newPosition)
    },
    geoError(error) {
      // TODO: console log eh ma pratica
      console.log("Vish, deu ruim!", error)
    },
    iniciar() {
      this.trackStore.iniciarTracking(this.description, this.circuit_selected.id)
      const options = {
        enableHighAccuracy: true,
        maximumAge: 0,
      }
      this.watch_id = navigator.geolocation.watchPosition(this.geoSuccess, this.geoError, options)
      // this.timer = setInterval(() => {
      //   navigator.geolocation.getCurrentPosition(this.geoSuccess, this.geoError, options)
      //
      // }, this.timerInterval_2min)
    },
    parar() {
      navigator.geolocation.clearWatch(this.watch_id)
      //clearInterval(this.timer)
      //this.timer = null
      //this.tentativas = 0
      this.trackStore.pararTracking()
    },
  },
}
</script>

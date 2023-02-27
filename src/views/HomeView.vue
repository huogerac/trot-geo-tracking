<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <v-form>
        <v-text-field v-model="percurso" label="Novo percurso" required></v-text-field>

        <v-btn v-if="id == 0" variant="flat" color="secondary" block @click="iniciar">
          INICIAR
        </v-btn>
        <v-btn v-else variant="flat" color="secondary" block @click="parar"> PARAR </v-btn>
        <p>
          Descartar pontos com acurácia pior que:
          <v-chip class="ma-2" color="pink" label text-color="white">
            <v-icon start icon="mdi-trash-can-outline"></v-icon>
            {{ positionsUnused }}
          </v-chip>
        </p>
        <v-slider
          v-model="accuracyThreshold"
          :min="6"
          :max="40"
          :step="2"
          thumb-label="always"></v-slider>
      </v-form>

      <div v-if="lastPosition.latitude">
        <h2>Última posição</h2>
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
        <p>
          <v-btn color="success" variant="flat" @click="marcarPontoComoBom"> BOM </v-btn>
          <v-btn color="error" variant="flat" @click="marcarPontoComoRuim"> RUIM </v-btn>
        </p>
        <p>latLon: {{ latLon }}</p>
        <p>center: {{ center }}</p>
      </div>

      <v-btn color="primary" variant="flat" :to="{ name: 'PercursoDetalheView' }" class="my-4">
        Ver percurso
      </v-btn>

      <open-layer-map-point-viewer v-if="latLon" :positions-list="latLon" :center="center">
      </open-layer-map-point-viewer>
    </v-responsive>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useLocationStore } from "@/store/location"
import { OpenLayerMapPointViewer } from "@/components/OpenLayerMapPointViewer"

export default {
  components: {
    OpenLayerMapPointViewer,
  },
  setup() {
    const locationStore = useLocationStore()

    return {
      locationStore,
    }
  },
  data() {
    return {
      id: 0,
      lastPosition: {},
      accuracyThreshold: 26,
      positionsUnused: 0,
      positions: [],
      percurso: "",
    }
  },
  computed: {
    ...mapState(useLocationStore, ["latLon"]),
    center() {
      return this?.latLon?.slice(-1)[0]
    },
  },
  methods: {
    geoSuccess(position) {
      if (
        position.coords.latitude == this.lastPosition.latitude &&
        position.coords.longitude == this.lastPosition.longitude
      ) {
        return
      }
      if (position.coords.accuracy > this.accuracyThreshold) {
        this.positionsUnused += 1
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
      this.locationStore.savePositions(newPosition)
      // this.positions.push(newPosition)
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
    marcarPontoComoRuim() {
      console.log("ruim")
      this.locationStore.badPosition()
    },
    marcarPontoComoBom() {
      console.log("bom")
      this.locationStore.goodPosition()
    },
  },
}
</script>

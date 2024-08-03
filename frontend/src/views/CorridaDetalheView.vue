<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <v-btn outlined class="ma-4" @click="corridas">Voltar</v-btn>
      <v-btn density="compact" icon="mdi-arrow-left" @click="turn_prior"></v-btn>
      <v-btn density="compact" icon="mdi-arrow-right" @click="turn_next"></v-btn>
      <h1>Corrida: {{ track_id }}</h1>
      <h2>Total Points: {{ trackPoints.length }}</h2>
      <h2>Points Turn {{ current_turn }}: {{ trackPointsLatLon.length }}</h2>

      <!--
      <open-layer-map-viewer
        v-if="trackPointsLatLon"
        :positions-list="trackPointsLatLon"
        :center="center"></open-layer-map-viewer>
      -->
      <h2>Pontos</h2>
      <open-layer-map-point-viewer
        v-if="trackPointsLatLon"
        :positions-list="trackPointsLatLon"
        :center="center">
      </open-layer-map-point-viewer>
    </v-responsive>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useTrackStore } from "@/store/trackStore"
//import OpenLayerMapViewer from "@/components/OpenLayerMapViewer.vue"
import OpenLayerMapPointViewer from "@/components/OpenLayerMapPointViewer.vue"

export default {
  components: {
    //OpenLayerMapViewer,
    OpenLayerMapPointViewer,
  },
  setup() {
    const trackStore = useTrackStore()
    return {
      trackStore,
    }
  },
  data() {
    return {
      show: false,
      projection: "EPSG:4326",
      zoom: 17,
      rotation: 0,
      radius: 40,
      strokeWidth: 10,
      strokeColor: "red",
      track_id: 0,
      current_turn: 1,
    }
  },
  computed: {
    ...mapState(useTrackStore, ["trackPoints"]),
    trackPointsTurn() {
      return this?.trackPoints.filter((item) => item.turn == this.current_turn)
    },
    trackPointsLatLon() {
      return this?.trackPointsTurn.map((obj) => [obj.longitude, obj.latitude])
    },
    center() {
      return this?.trackPointsLatLon[0]
    },
  },
  mounted() {
    this.track_id = this.$route.params.id
    this.getPoints()
  },
  methods: {
    async getPoints() {
      this.trackStore.getPoints(this.track_id)
    },
    turn_prior() {
      if (this.current_turn == 1) {
        return
      }
      this.current_turn = this.current_turn - 1
    },
    turn_next() {
      this.current_turn = this.current_turn + 1
    },
    corridas() {
      this.$router.push({ name: "ListarCorridasView" })
    },
  },
}
</script>

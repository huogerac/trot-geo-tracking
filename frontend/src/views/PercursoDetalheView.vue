<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <h1>Tela de Visualização</h1>

      <h2>Linhas</h2>
      <open-layer-map-viewer :positions-list="latLon" :center="center"></open-layer-map-viewer>

      <h2>Pontos</h2>
      <open-layer-map-point-viewer :positions-list="latLon" :center="center">
      </open-layer-map-point-viewer>
      <h2>Positions:</h2>
      <ul>
        <li v-for="(position, idx) in positions" :key="idx">
          <p>{{ position }}</p>
        </li>
      </ul>
    </v-responsive>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useLocationStore } from "@/store/locationStore"
import OpenLayerMapViewer from "@/components/OpenLayerMapViewer.vue"
import OpenLayerMapPointViewer from "@/components/OpenLayerMapPointViewer.vue"

export default {
  components: {
    OpenLayerMapViewer,
    OpenLayerMapPointViewer,
  },
  data() {
    return {
      projection: "EPSG:4326",
      zoom: 17,
      rotation: 0,
      radius: 40,
      strokeWidth: 10,
      strokeColor: "red",
    }
  },
  computed: {
    ...mapState(useLocationStore, ["positions", "latLon"]),
    center() {
      return this?.latLon[0]
    },
  },
  methods: {},
}
</script>

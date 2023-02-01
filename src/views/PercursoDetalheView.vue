<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <h1>Tela de Visualização</h1>

      <ol-map :load-tiles-while-animating="true" :load-tiles-while-interacting="true" style="height:400px">

    <ol-view ref="view" :center="center" :rotation="rotation" :zoom="zoom" :projection="projection" />

    <ol-tile-layer>
        <ol-source-osm />
    </ol-tile-layer>

    <ol-vector-layer>
        <ol-source-vector>
            <ol-feature>
                <ol-geom-line-string :coordinates="latLon"></ol-geom-line-string>
                <ol-style>
                        <ol-style-stroke :color="strokeColor" :width="strokeWidth"></ol-style-stroke>          
                </ol-style>
            </ol-feature>

        </ol-source-vector>

    </ol-vector-layer>

</ol-map>

    </v-responsive>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useLocationStore } from "@/store/location"

export default {
  data() {
    return {
        projection: 'EPSG:4326',
        zoom: 17,
        rotation: 0,
        radius: 40,
        strokeWidth: 10,
        strokeColor: 'red',
    }
  },
  computed: {
    ...mapState(useLocationStore, ["positions", "latLon"]),
    center () {
      return this?.latLon[0]
    }
  },
  methods: {
   
  },
}
</script>

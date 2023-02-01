<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <h1>Tela de Visualização</h1>
      <ol-map :loadTilesWhileAnimating="true" :loadTilesWhileInteracting="true" style="height:400px">

    <ol-view ref="view" :center="center" :rotation="rotation" :zoom="zoom" :projection="projection" />

    <ol-tile-layer>
        <ol-source-osm />
    </ol-tile-layer>

    <ol-vector-layer>
        <ol-source-vector>
            <ol-feature>
                <ol-geom-line-string :coordinates="posicoes"></ol-geom-line-string>
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
export default {
  data() {
    return {
        posicoes: [[-45.9105859,-23.2393818]],
        center: [-45.9105859,-23.2393818] ,
        projection: 'EPSG:4326',
        zoom: 17,
        rotation: 0,
        radius: 40,
        strokeWidth: 10,
        strokeColor: 'red',
    }
  },
  methods: {
   
  },
}
</script>

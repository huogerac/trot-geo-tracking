<template>
  <ol-map
    :load-tiles-while-animating="true"
    :load-tiles-while-interacting="true"
    style="height: 400px">
    <ol-view
      ref="view"
      :center="center"
      :rotation="rotation"
      :zoom="zoom"
      :projection="projection" />

    <ol-tile-layer>
      <ol-source-osm />
    </ol-tile-layer>

    <ol-vector-layer>
      <ol-source-vector>
        <ol-feature>
          <ol-geom-line-string :coordinates="positionsList"></ol-geom-line-string>
          <ol-style>
            <ol-style-stroke :color="strokeColor" :width="strokeWidth"></ol-style-stroke>
          </ol-style>
        </ol-feature>
      </ol-source-vector>
    </ol-vector-layer>
  </ol-map>
</template>

<script>
export default {
  props: {
    positionsList: {
      type: Array,
      default: null,
    },
    center: {
      type: Array,
      default: null,
    },
  },
  data: () => ({
    projection: "EPSG:4326",
    zoom: 17,
    rotation: 0,
    radius: 40,
    strokeWidth: 10,
    strokeColor: "blue",
  }),
}
</script>

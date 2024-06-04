<template>
  <ol-map
    :load-tiles-while-animating="true"
    :load-tiles-while-interacting="true"
    style="height: 600px">
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
          <ol-geom-multi-point :coordinates="positionsList"> </ol-geom-multi-point>
          <ol-style>
            <ol-style-circle :radius="radius">
              <ol-style-fill :color="fillColor"></ol-style-fill>
              <ol-style-stroke :color="strokeColor" :width="strokeWidth"></ol-style-stroke>
            </ol-style-circle>
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
    radius: 5,
    strokeWidth: 1,
    strokeColor: "blue",
    fillColor: "white",
  }),
}
</script>

import { defineStore } from "pinia"

export const useLocationStore = defineStore("location", {
  state: () => ({
    positions: [],
    lastPosition: {},
    accuracyMin: 26,
    accuracyThreshold: 26,
  }),
  actions: {
    savePositions(position) {
      if (
        this.positions.length > 0 &&
        position.latLongAccuracy > this.accuracyThreshold &&
        position.latLongAccuracy > this.accuracyMin
      ) {
        return
      }
      if (
        position.latitude == this.lastPosition?.latitude &&
        position.longitude == this.lastPosition?.longitude
      ) {
        return
      }
      this.positions.push(position)
      this.lastPosition = position

      const accuracySum = this.positions.reduce((a, b) => a + b.latLongAccuracy, 0)
      const accuracyAvg = accuracySum / this.positions.length
      this.accuracyThreshold = accuracyAvg * 1.3
    },
  },
  getters: {
    latLon: (state) => state.positions.map((obj) => [obj.longitude, obj.latitude]),
  },
})

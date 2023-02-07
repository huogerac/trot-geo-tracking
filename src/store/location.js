import { defineStore } from "pinia"

export const useLocationStore = defineStore("location", {
  state: () => ({
    positions: [],
  }),
  actions: {
    savePositions(position) {
      this.positions.push(position)
    },
    badPosition() {
      let lastPosition = this.positions[this.positions.length - 1]
      lastPosition.quality = "bad"
    },
    goodPosition() {
      let lastPosition = this.positions[this.positions.length - 1]
      lastPosition.quality = "good"
    },
  },
  getters: {
    latLon: (state) => state.positions.map((obj) => [obj.longitude, obj.latitude]),
  },
})

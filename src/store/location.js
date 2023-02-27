import { defineStore } from "pinia"

export const useLocationStore = defineStore("location", {
  state: () => ({
    positions: [],
  }),
  actions: {
    savePositions(position) {
      this.positions.push(position)
    },
  },
  getters: {
    latLon: (state) => state.positions.map((obj) => [obj.longitude, obj.latitude]),
  },
})

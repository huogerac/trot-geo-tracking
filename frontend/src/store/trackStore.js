import { defineStore } from "pinia"
import TrackApi from "@/api/tracks.api.js"

export const useTrackStore = defineStore("TrackStore", {
  state: () => ({
    circuitsLoading: false,
    circuits: [],
    track_id: null,
    positions: [],
    positionsSaved: 0,
    positionsIgnored: 0,
    lastPosition: null,
    lastSavedPositions: [],
  }),
  actions: {
    async getCircuitos() {
      this.circuitsLoading = true
      const response = await TrackApi.getCircuits()
      this.circuits = response.circuits
      console.log("store:circuits:", this.circuits)
      this.circuitsLoading = false
    },
    async iniciarTracking(description, circuit_id) {
      this.circuitsLoading = true
      const response = await TrackApi.startTrack(description, circuit_id)
      this.track_id = response.id
      console.log("start:", response)
      this.circuitsLoading = false
    },
    async salvarPosicoes(position) {
      this.circuitsLoading = true
      this.positions.push(position)
      this.lastPosition = position
      this.lastSavedPositions.push(position)
      if (this.positions.length >= 100) {
        const response = await TrackApi.savePoints(this.track_id, this.positions)
        console.log(response)
        this.positions = []
        if (response.points_saved) {
          this.positionsSaved = this.positionsSaved + response.points_saved
          this.positionsIgnored = this.positionsIgnored + response.points_ignored
        }
        if (this.lastSavedPositions.length > 1000) {
          this.lastSavedPositions.splice(0, this.lastSavedPositions.length - 1000)
        }
      }
    },
    async pararTracking() {
      this.circuitsLoading = true
      const response = await TrackApi.stopTrack(this.track_id)
      console.log(response)

      this.track_id = null
      this.track_id = null
      this.positions = []
      this.positionsSaved = 0
      this.positionsIgnored = 0
      this.lastPosition = null
      this.lastSavedPositions = []
    },
  },
})

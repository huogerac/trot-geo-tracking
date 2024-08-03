import { defineStore } from "pinia"
import TrackApi from "@/api/tracks.api.js"

export const useTrackStore = defineStore("TrackStore", {
  state: () => ({
    trackStatus: "waiting",
    circuitsLoading: false,
    circuits: [],
    track_id: null,
    positions: [],
    positionsSaved: 0,
    positionsIgnored: 0,
    lastPosition: null,
    lastSavedPositions: [],
    tracks: [],
    trackPoints: [],
  }),
  actions: {
    async getCircuitos() {
      this.circuitsLoading = true
      const response = await TrackApi.getCircuits()
      this.circuits = response.circuits
      this.circuitsLoading = false
    },
    async getTracks() {
      const response = await TrackApi.getTracks()
      this.tracks = response.tracks
    },
    async getPoints(track_id) {
      const response = await TrackApi.getPoints(track_id)
      this.trackPoints = response.points
    },
    async iniciarTracking(description, circuit_id) {
      this.circuitsLoading = true
      const response = await TrackApi.startTrack(description, circuit_id)
      this.track_id = response.id
      console.log("start:", response)
      this.trackStatus = `Track started: ${response.id}`
      this.circuitsLoading = false
      this.positions = []
      this.lastSavedPositions = []
      this.lastPosition = null
      this.positionsSaved = 0
      this.positionsIgnored = 0
    },
    async salvarPosicoes(position) {
      this.circuitsLoading = true
      this.positions.push(position)
      this.lastPosition = position
      this.lastSavedPositions.push(position)
      if (this.positions.length >= 40) {
        this.trackStatus = `Saving points`
        const response = await TrackApi.savePoints(this.track_id, this.positions)
        console.log(response)
        this.positions = []
        this.trackStatus = `Saved: ${response?.result?.points_saved}; Ignored: ${response?.result?.points_ignored}; Turn: ${response?.result?.current_turn}`
        if (response?.result?.points_saved) {
          this.positionsSaved = this.positionsSaved + response.result.points_saved
          this.positionsIgnored = this.positionsIgnored + response.result.points_ignored
        }
        if (this.lastSavedPositions.length > 1000) {
          this.lastSavedPositions.splice(0, this.lastSavedPositions.length - 1000)
        }
      }
    },
    async pararTracking() {
      this.circuitsLoading = true
      let response = await TrackApi.savePoints(this.track_id, this.positions)
      console.log(response)
      this.positions = []

      response = await TrackApi.stopTrack(this.track_id)
      console.log(response)
      this.track_id = null
      this.positionsSaved = 0
      this.circuitsLoading = false
    },
  },
  getters: {
    latLon: (state) => state.lastSavedPositions.map((obj) => [obj.longitude, obj.latitude]),
  },
})

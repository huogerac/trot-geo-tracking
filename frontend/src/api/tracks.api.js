import api from "./config.js"

export default {
  getCircuits: async () => {
    const response = await api.get("/api/core/circuits")
    return response.data
  },
  startTrack: async (description, circuit_id) => {
    const json = { description, circuit_id }
    const response = await api.post("/api/core/tracks/start", json)
    return response.data
  },
  savePoints: async (track_id, points) => {
    const json = { points }
    const response = await api.post(`/api/core/tracks/${track_id}/points/save`, json)
    return response.data
  },
  stopTrack: async (track_id) => {
    const response = await api.post(`/api/core/tracks/${track_id}/stop`)
    return response.data
  },
}

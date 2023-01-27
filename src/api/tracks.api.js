import api from "./config.js"
import apiHelpers from "./helpers.js"

export default {
  getTracks: () => {
    return new Promise((resolve, reject) => {
      api
        .get("/api/tracks/")
        .then((response) => {
          return resolve(response.data)
        })
        .catch((error) => {
          return reject(error)
        })
    })
  },
  addTrack: (name) => {
    return new Promise((resolve, reject) => {
      api
        .post("/api/tracks/add", apiHelpers.dataToForm({ name }))
        .then((response) => {
          return resolve(response.data)
        })
        .catch((error) => {
          return reject(error)
        })
    })
  },
}

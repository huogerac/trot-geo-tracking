import api from "./config.js"
//import apiHelpers from "./helpers.js"

export default {
  addPosition: (trackId, coords) => {
    return new Promise((resolve, reject) => {
      api
        .post(`/api/positions/tracks/${trackId}/add`, { coords })
        .then((response) => {
          return resolve(response.data)
        })
        .catch((error) => {
          return reject(error)
        })
    })
  },
}

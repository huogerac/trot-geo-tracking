const utils = require("../utils")

module.exports = {
  tracks: utils.parseJson("./data/tracks.json"),
  positions: utils.parseJson("./data/positions.json"),
}

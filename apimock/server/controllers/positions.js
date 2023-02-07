const data = require("../data")

function getMaxId(items) {
  return Math.max(...items.map((item) => item.id))
}

module.exports = {
  find: (req, res) => {
    const { id } = req.params
    if (id == undefined) {
      res.status(404).end()
      return
    }

    const positions = data.positions.filter((p) => p.track_id == id)
    if (positions.length == 0) {
      res.status(404).end()
      return
    }
    res.send(positions)
    return
  },
  add: (req, res) => {
    const { trackId } = req.params
    const { coords } = req.body
    const id = getMaxId(data.positions) + 1
    const newPosition = {
      id,
      track_id: trackId,
      coords,
    }
    data.positions.push(newPosition)
    console.log("📍 nova posição adicionada no trajeto:", trackId)
    res.send(newPosition)
  },
}

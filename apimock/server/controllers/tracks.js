const data = require("../data")

function getMaxId(items) {
  return Math.max(...items.map((item) => item.id))
}

module.exports = {
  find: (req, res) => {
    const { id } = req.params
    if (id != undefined) {
      const track = data.tracks.find((t) => t.id == id)
      if (!track) {
        res.status(404).end()
        return
      }
      res.send(track)
      return
    }
    const response = {
      tracks: data.tracks,
    }
    res.send(response)
  },
  add: (req, res) => {
    const { name } = req.body
    const id = getMaxId(data.tracks) + 1
    const newTrack = {
      id,
      name,
    }
    data.tracks.push(newTrack)
    res.send(newTrack)
  },
}

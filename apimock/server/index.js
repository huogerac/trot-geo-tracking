const express = require("express")
const cors = require("cors")
const bodyParser = require("body-parser")
const multer = require("multer")
const cookieParser = require("cookie-parser")

const tracks = require("./controllers/tracks")
const positions = require("./controllers/positions")

const YELLOW = "\x1b[33m%s\x1b[0m"
const WHITE = "\x1b[37m"

const app = express()

app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))
app.use(multer().array())
app.use(cookieParser())

//CONFIG
const PORT = process.env.APIMOCK_PORT || 8000
const ORIGIN_URL = process.env.ORIGIN_URL || "http://localhost:3000"

app.use(cors({ credentials: true, origin: ORIGIN_URL }))

// TRACKS
app.get("/api/tracks/", tracks.find)
app.get("/api/tracks/:id", tracks.find)
app.post("/api/tracks/add", tracks.add)

// POSITIONS
app.get("/api/positions/tracks/:id", positions.find)
app.post("/api/positions/tracks/:trackId/add", positions.add)

app.listen(PORT, () => {
  console.log(YELLOW, "🆙 API MOCK using express is running on port: " + PORT, WHITE)
})

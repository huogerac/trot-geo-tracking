<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <v-form>
        <v-text-field v-model="percurso" label="Novo percurso" required></v-text-field>

        <v-btn variant="flat" color="secondary" block @click="obterMinhaPosicao"> INICIAR </v-btn>
        <v-btn variant="flat" color="secondary" block @click="eraseDb"> RESET DB </v-btn>
      </v-form>
      <p>latitude: {{ latitude }}</p>
      <p>longitude: {{ longitude }}</p>
      <div v-if="geolocation.length != 0" style="margin-top: 10px">
        Saved Geolocation:
        <div v-for="location in geolocation" :key="location.id">
          <li>
            id: {{ location.id }} = latitude: {{ location.latitude }} / longitude:
            {{ location.longitude }}
          </li>
        </div>
      </div>
    </v-responsive>
  </v-container>
</template>

<script>
import axios from "axios"
export default {
  data() {
    return {
      percurso: "",
      latitude: null,
      longitude: null,
      date: null,
      geolocation: [],
    }
  },
  async created() {
    try {
      const res = await axios.get(`http://localhost:3001/api/geolocation`)
      this.geolocation = res.data
    } catch (error) {
      console.log(error)
    }
  },
  methods: {
    geoSuccess(position) {
      this.latitude = position.coords.latitude
      this.longitude = position.coords.longitude
      this.date = new Date().getTime()
      this.addGeolocation(this.latitude, this.longitude)
    },
    geoError(error) {
      console.log("Vish, deu ruim!", error)
    },
    obterMinhaPosicao() {
      navigator.geolocation.getCurrentPosition(this.geoSuccess, this.geoError)
    },
    async addGeolocation(lat, long) {
      const res = await axios.post(`http://localhost:3001/api/geolocation`, {
        latitude: lat,
        longitude: long,
      })
      this.geolocation.push(res.data)
    },
    eraseDb() {
      axios
        .get(`http://localhost:3001/api/geolocation`)
        .then((geolocation) => {
          geolocation.data.forEach((item) => {
            axios.delete(`http://localhost:3001/api/geolocation/${item.id}`)
          })
        })
        .finally((this.geolocation = []))
    },
  },
}
</script>

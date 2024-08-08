<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <v-btn outlined class="ma-4" @click="home">Home</v-btn>
      <h1>Corridas</h1>
      <v-table>
        <thead>
          <tr>
            <th class="text-left">ID</th>
            <th class="text-left">Corrida</th>
            <th></th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in tracks" :key="item.id">
            <td>{{ item.id }}</td>
            <td>{{ item.description }}</td>
            <td>
              <v-btn density="compact" icon="mdi-map" @click="detalhe(item.id)"></v-btn>
              <v-btn
                density="compact"
                icon="mdi-download"
                :loading="downloading"
                @click="download(item.id)"></v-btn>
            </td>
          </tr>
        </tbody>
      </v-table>
    </v-responsive>
  </v-container>
</template>

<script>
import { mapState } from "pinia"
import { useTrackStore } from "@/store/trackStore"
import TrackApi from "@/api/tracks.api.js"
import { saveAs } from "file-saver"

export default {
  setup() {
    const trackStore = useTrackStore()
    return {
      trackStore,
    }
  },
  data() {
    return {
      corridas: [],
      downloading: false,
    }
  },
  computed: {
    ...mapState(useTrackStore, ["tracks"]),
  },
  mounted() {
    this.getTracks()
  },
  methods: {
    home() {
      this.$router.push({ name: "Home" })
    },
    detalhe(corridaId) {
      this.$router.push({ name: "CorridaDetalheView", params: { id: corridaId } })
    },
    async download(corridaId) {
      this.downloading = true
      const response = await TrackApi.getDownloadPoints(corridaId)
      this.downloading = false
      saveAs(response.data, `track_${corridaId}_data.xlsx`)
    },
    async getTracks() {
      this.trackStore.getTracks()
    },
  },
}
</script>

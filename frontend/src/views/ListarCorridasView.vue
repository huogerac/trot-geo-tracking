<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <v-btn outlined class="ma-4" @click="home">Home</v-btn>
      <h1>Corridas</h1>
      <p v-for="track in tracks" :key="track.id">{{ track.id }} - {{ track.description }}</p>

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
    async getTracks() {
      this.trackStore.getTracks()
    },
  },
}
</script>

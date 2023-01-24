<template>
  <v-container class="fill-height">
    <v-responsive class="d-flex align-center text-center fill-height">
      <v-form>
        <v-text-field v-model="percurso" label="Novo percurso" required></v-text-field>

        <v-btn variant="flat" color="secondary" block> INICIAR </v-btn>
      </v-form>
    </v-responsive>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      percurso: "",
    }
  },
}
</script>

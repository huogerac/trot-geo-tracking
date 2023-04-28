<template>
  <router-view />
</template>

<script setup>
// TODO: mover app.vue para src/app, e manter a logica de app centralizada
// TODO: implementar a troca dinâmica de layouts no projeto, usando um "layout-handler"
// TODO: no projeto a gente ta usando PascalCase para nomear os componentes, e kebab-case para referencia-los em outros componentes, tem que melhorar isso
// TODO: quebrar o router em modulos, ter uma pagina de constantes para guardar page name e layout name (facilita a navegacao e troca de nome de paginas no longo prazo)
// TODO: utilizar pages ao invés de views
// TODO: preferir named exports ao invés do export default para manter uma consistência no projeto
// TODO: quando a lógica do app estiver bem definida, utilizar testes e2e em playwright
// TODO: usar o maximo possivel do workbox para cachear deps no service worker
// https://github.com/vite-pwa/vite-plugin-pwa/tree/main/examples/vue-router
// https://web.dev/offline-cookbook/
// https://web.dev/learn/pwa/
// https://vite-pwa-org.netlify.app/guide/
</script>

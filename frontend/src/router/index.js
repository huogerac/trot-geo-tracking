// Composables
import { createRouter, createWebHistory } from "vue-router"
import HomeView from "@/views/HomeView.vue"
import PercursoDetalheView from "@/views/PercursoDetalheView.vue"
import ListarCorridasView from "@/views/ListarCorridasView.vue"
import CorridaDetalheView from "@/views/CorridaDetalheView.vue"

const routes = [
  {
    path: "/",
    component: () => import("@/layouts/default/Default.vue"),
    children: [
      {
        path: "",
        name: "Home",
        component: HomeView,
      },
      {
        path: "Detalhe",
        name: "PercursoDetalheView",
        component: PercursoDetalheView,
      },
      {
        path: "corridas",
        name: "ListarCorridasView",
        component: ListarCorridasView,
      },
      {
        path: "corridas/:id",
        name: "CorridaDetalheView",
        component: CorridaDetalheView,
      },
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router

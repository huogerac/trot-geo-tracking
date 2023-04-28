// Composables
import { createRouter, createWebHistory } from "vue-router"
import HomeView from "@/views/HomeView.vue"
import PercursoDetalheView from "@/views/PercursoDetalheView.vue"

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
    ],
  },
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
})

export default router

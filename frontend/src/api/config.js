import axios from "axios"

import router from "../router"

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  xsrfHeaderName: "X-CSRFToken",
  xsrfCookieName: "csrftoken",
  withCredentials: true,
  headers: {
    "Content-Type": "application/json",
  },
})

export function responseSuccess(response) {
  return response
}

export function responseError(error) {
  // Redireciona falha na comunicação com o BACKEND para página 500
  //const baseStore = useBaseStore()
  if (!error.response && error.message === "Network Error") {
    //baseStore.setShowErrorMessage(error.message)
    console.log("-------->", error.message)
  }

  // Redireciona erro de autênticação para página de login
  if (error.response && error.response.status === 401) {
    //baseStore.showSnackbar("Usuário sem autênticação. Efetue o login!", "warning")
    console.log("-------->", "Usuário sem autênticação. Efetue o login!")
    router.push({
      name: "accounts-login",
    })
    return
  }
  return Promise.reject(error)
}

api.interceptors.response.use(responseSuccess, responseError)

export default api

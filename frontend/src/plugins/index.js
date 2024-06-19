/**
 * plugins/index.js
 *
 * Automatically included in `./src/main.js`
 */

// Plugins
import { loadFonts } from "./webfontloader"
import vuetify from "./vuetify"
import OpenLayersMap from "./openlayers"
import { createPinia } from "pinia"
import router from "../router"

export function registerPlugins(app) {
  loadFonts()
  app.use(vuetify).use(OpenLayersMap).use(createPinia()).use(router)
}

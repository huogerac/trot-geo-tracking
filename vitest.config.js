import { mergeConfig } from "vite"
import { defineConfig } from "vitest/config"

import { fileURLToPath, URL } from "node:url"
import viteConfig from "./vite.config"

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: "jsdom",
      src: "src/",
    },
    resolve: {
      alias: {
        "@": fileURLToPath(new URL("./src", import.meta.url)),
      },
    },
  })
)

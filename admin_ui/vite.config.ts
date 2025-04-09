import { fileURLToPath, URL } from "node:url"

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"
import vueDevTools from "vite-plugin-vue-devtools"

// https://vite.dev/config/
export default defineConfig({
    plugins: [vue(), vueDevTools()],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url))
        }
    },
    base: "./",
    build: {
        outDir: "../piccolo_admin/dist",
        emptyOutDir: true
    },
    server: {
        host: "127.0.0.1",
        port: 3000,
        proxy: {
            "^/api": {
                target: "http://127.0.0.1:8000"
            },
            "^/public": {
                target: "http://127.0.0.1:8000"
            }
        }
    }
})

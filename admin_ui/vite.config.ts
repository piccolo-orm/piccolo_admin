import { fileURLToPath, URL } from "url"

import { defineConfig } from "vite"
import vue from "@vitejs/plugin-vue"

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
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
        host: "0.0.0.0",
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

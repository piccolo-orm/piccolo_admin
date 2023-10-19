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

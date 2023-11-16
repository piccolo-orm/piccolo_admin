import { createApp } from "vue"

import App from "./App.vue"
import router from "./router"
import store from "./store"
import { setupFonts } from "./fontawesome"
import i18n from "./translations"

/*****************************************************************************/

import axios from "axios"
import JSONBig from "json-bigint"
import Cookies from "js-cookie"

// Add the CSRF token
axios.interceptors.request.use(function (config) {
    if (
        config.method &&
        ["POST", "PUT", "DELETE", "PATCH"].indexOf(
            config.method.toUpperCase()
        ) != -1
    ) {
        const csrfToken = Cookies.get("csrftoken")
        config.headers["X-CSRFToken"] = csrfToken
    }
    return config
})

// Handle BigInt values
axios.defaults.transformResponse = [
    function (data) {
        if (typeof data === "string") {
            try {
                data = JSONBig.parse(data)
            } catch (e) {}
        }
        return data
    }
]

/*****************************************************************************/
// Create app

const app = createApp(App)

/*****************************************************************************/
// Localisation

app.use(i18n)

app.provide("i18n", i18n)

/*****************************************************************************/
// Fonts

setupFonts(app)

/*****************************************************************************/
// Router

app.use(router)

/*****************************************************************************/
// Store

app.use(store)

/*****************************************************************************/
// Mount app

app.mount("#app")

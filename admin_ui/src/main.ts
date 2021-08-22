import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import FontAwesomeIcon from './fontawesome'

/*****************************************************************************/

import axios from 'axios'
import JSONBig from 'json-bigint'
import Cookies from 'js-cookie'

// Add the CSRF token
axios.interceptors.request.use(function (config) {
    if (
        ['POST', 'PUT', 'DELETE', 'PATCH'].indexOf(
            config.method.toUpperCase()
        ) != -1
    ) {
        const csrfToken = Cookies.get('csrftoken')
        config.headers['X-CSRFToken'] = csrfToken
    }
    return config
})

// Handle BigInt values
axios.defaults.transformResponse = [function (data) {
    if (typeof data === 'string') {
        try {
            data = JSONBig.parse(data);
        } catch (e) {
        }
    }
    return data;
}]

/*****************************************************************************/

createApp(App as any)
    .use(router)
    .use(store)
    .component("font-awesome-icon", FontAwesomeIcon)
    .mount("#app");


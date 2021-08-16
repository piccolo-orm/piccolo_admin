import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import { FontAwesomeIcon } from "@fortawesome/vue-fontawesome"
import { library } from '@fortawesome/fontawesome-svg-core'
import {
    faAngleDown,
    faAngleLeft,
    faAngleRight,
    faAngleUp,
    faBars,
    faCheck,
    faEdit,
    faEllipsisV,
    faExternalLinkAlt,
    faFileCsv,
    faFilter,
    faHome,
    faInfoCircle,
    faLevelUpAlt,
    faMoon,
    faPlus,
    faQuestionCircle,
    faSignOutAlt,
    faSort,
    faSun,
    faTable,
    faTimes,
    faTools,
    faTrashAlt,
    faUser,
} from '@fortawesome/free-solid-svg-icons'

library.add(
    faAngleDown,
    faAngleLeft,
    faAngleRight,
    faAngleUp,
    faBars,
    faCheck,
    faEdit,
    faEllipsisV,
    faExternalLinkAlt,
    faFileCsv,
    faFilter,
    faHome,
    faInfoCircle,
    faLevelUpAlt,
    faMoon,
    faPlus,
    faQuestionCircle,
    faSignOutAlt,
    faSort,
    faSun,
    faTable,
    faTimes,
    faTools,
    faTrashAlt,
    faUser,
)

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

// Vue.filter('readable', function (value) {
//     return value.split('_').join(' ')
// })

/*****************************************************************************/

const app = createApp(App as any)
    .use(router)
    .use(store)
    .component("font-awesome-icon", FontAwesomeIcon)
    .mount("#app");


import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'

/******************************************************************************
 Font Awesome */

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
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
    faKey,
    faLevelUpAlt,
    faMoon,
    faPlus,
    faQuestionCircle,
    faSignOutAlt,
    faSort,
    faStar,
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
    faKey,
    faLevelUpAlt,
    faMoon,
    faPlus,
    faQuestionCircle,
    faSignOutAlt,
    faSort,
    faStar,
    faSun,
    faTable,
    faTimes,
    faTools,
    faTrashAlt,
    faUser,
)
Vue.component('font-awesome-icon', FontAwesomeIcon)

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

Vue.filter('readable', function (value) {
    return value.split('_').join(' ')
})

/*****************************************************************************/

Vue.config.productionTip = false

new Vue({
    router,
    store,
    render: h => h(App)
}).$mount('#app')

import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import './fontawesome'

/*****************************************************************************/

import axios from 'axios'
import JSONBig from 'json-bigint'
import Cookies from 'js-cookie'
import VueI18n from 'vue-i18n'
import english from "../locales/english.json"
import welsh from "../locales/welsh.json"
import croatian from "../locales/croatian.json"


const messages = {
    english,
    welsh,
    croatian,
}

Vue.use(VueI18n)
const i18n = new VueI18n({
    locale: "english",
    messages,
    silentTranslationWarn: process.env.NODE_ENV === 'production'
})


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
    i18n,
    router,
    store,
    render: h => h(App)
}).$mount('#app')

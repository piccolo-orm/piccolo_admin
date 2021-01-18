import axios from 'axios'

const BASE_URL = process.env.VUE_APP_BASE_URI

export default {
    state: {
        siteName: 'Piccolo Admin',
        piccoloAdminVersion: 'Unknown'
    },
    mutations: {
        updateSiteName(state, value: Object) {
            state.siteName = value
        },
        updatePiccoloAdminVersion(state, value: Object) {
            state.piccoloAdminVersion = value
        },
    },
    actions: {
        async fetchMeta(context) {
            const response = await axios.get(`${BASE_URL}meta/`)
            this.commit('updateSiteName', response.data.site_name)
            this.commit('updatePiccoloAdminVersion', response.data.piccolo_admin_version)
        }
    }
}

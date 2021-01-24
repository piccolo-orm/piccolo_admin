import axios from 'axios'

const BASE_URL = process.env.VUE_APP_BASE_URI

export default {
    state: {
        siteName: 'Piccolo Admin',
        piccoloAdminVersion: 'Unknown'
    },
    mutations: {
        updateSiteName(state, value: string) {
            state.siteName = value
        },
        updatePiccoloAdminVersion(state, value: string) {
            state.piccoloAdminVersion = value
        },
    },
    actions: {
        async fetchMeta(context) {
            const response = await axios.get(`${BASE_URL}meta/`)
            context.commit('updateSiteName', response.data.site_name)
            context.commit('updatePiccoloAdminVersion', response.data.piccolo_admin_version)
        }
    }
}

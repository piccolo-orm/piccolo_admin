import axios from 'axios'

export default {
    state: {
        siteName: 'Piccolo Admin',
        piccoloAdminVersion: 'Unknown',
        defaultLanguage: "english",
    },
    mutations: {
        updateSiteName(state, value: string) {
            state.siteName = value
        },
        updatePiccoloAdminVersion(state, value: string) {
            state.piccoloAdminVersion = value
        },
        updateDefaultLanguage(state, value) {
            state.defaultLanguage = value
        }
    },
    actions: {
        async fetchMeta(context) {
            const response = await axios.get(`./meta/`)
            context.commit('updateSiteName', response.data.site_name)
            context.commit('updatePiccoloAdminVersion', response.data.piccolo_admin_version)
            context.commit('updateDefaultLanguage', response.data.default_language)
        }
    }
}

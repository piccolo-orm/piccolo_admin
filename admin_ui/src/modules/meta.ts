import axios from 'axios'

export default {
    state: {
        siteName: 'Piccolo Admin',
        piccoloAdminVersion: 'Unknown',
        defaultLanguage: "english",
        languages: undefined,
    },
    mutations: {
        updateSiteName(state, value: string) {
            state.siteName = value
        },
        updatePiccoloAdminVersion(state, value: string) {
            state.piccoloAdminVersion = value
        },
        updateDefaultLanguage(state, value: string) {
            state.defaultLanguage = value
        },
        updateLanguages(state, value: object) {
            state.languages = value
            localStorage.setItem("languages", JSON.stringify(value))
        }
    },
    actions: {
        async fetchMeta(context) {
            const response = await axios.get(`./meta/`)
            context.commit('updateSiteName', response.data.site_name)
            context.commit('updatePiccoloAdminVersion', response.data.piccolo_admin_version)
            context.commit('updateDefaultLanguage', response.data.default_language)
            context.commit('updateLanguages', response.data.languages)
        }
    }
}

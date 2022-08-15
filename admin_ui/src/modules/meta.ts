import axios from "axios"

export default {
    state: {
        siteName: "Piccolo Admin",
        piccoloAdminVersion: "Unknown",
        logoPath: "icons/logo.jpg",
        faviconPath: "icons/favicon.ico",
    },
    mutations: {
        updateSiteName(state, value: string) {
            state.siteName = value
        },
        updateLogoPath(state, value: string) {
            state.logoPath = value
        },
        updateFaviconPath(state, value: string) {
            state.faviconPath = value
        },
        updatePiccoloAdminVersion(state, value: string) {
            state.piccoloAdminVersion = value
        }
    },
    actions: {
        async fetchMeta(context) {
            const response = await axios.get(`./public/meta/`)
            context.commit("updateSiteName", response.data.site_name)
            context.commit("updateLogoPath", response.data.logo_path)
            context.commit("updateFaviconPath", response.data.favicon_path)
            context.commit(
                "updatePiccoloAdminVersion",
                response.data.piccolo_admin_version
            )
        }
    }
}

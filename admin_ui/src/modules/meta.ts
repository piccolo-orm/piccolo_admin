import axios from "axios"

export default {
    state: {
        siteName: "Piccolo Admin",
        piccoloAdminVersion: "Unknown",
        logoImage: "logo.jpg",
    },
    mutations: {
        updateSiteName(state, value: string) {
            state.siteName = value
        },
        updateLogoImage(state, value: string) {
            state.logoImage = value
        },
        updatePiccoloAdminVersion(state, value: string) {
            state.piccoloAdminVersion = value
        }
    },
    actions: {
        async fetchMeta(context) {
            const response = await axios.get(`./public/meta/`)
            context.commit("updateSiteName", response.data.site_name)
            context.commit("updateLogoImage", response.data.logo_image)
            context.commit(
                "updatePiccoloAdminVersion",
                response.data.piccolo_admin_version
            )
        }
    }
}

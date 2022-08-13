import axios from "axios"

export default {
    state: {
        siteName: "Piccolo Admin",
        piccoloAdminVersion: "Unknown",
        logoImage: "logo.jpg",
        logoWidth: 40,
        logoHeight: 30,
    },
    mutations: {
        updateSiteName(state, value: string) {
            state.siteName = value
        },
        updateLogoImage(state, value: string) {
            state.logoImage = value
        },
        updateLogoWidth(state, value: number) {
            state.logoWidth = value
        },
        updateLogoHeight(state, value: number) {
            state.logoHeight = value
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
            context.commit("updateLogoWidth", response.data.logo_width)
            context.commit("updateLogoHeight", response.data.logo_height)
            context.commit(
                "updatePiccoloAdminVersion",
                response.data.piccolo_admin_version
            )
        }
    }
}

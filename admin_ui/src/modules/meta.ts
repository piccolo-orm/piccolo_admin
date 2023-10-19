import axios from "axios"

import type { Context } from "./interfaces"

interface State {
    siteName: string
    piccoloAdminVersion: string
}

export default {
    state: {
        siteName: "Piccolo Admin",
        piccoloAdminVersion: "Unknown"
    } as State,
    mutations: {
        updateSiteName(state: State, value: string) {
            state.siteName = value
        },
        updatePiccoloAdminVersion(state: State, value: string) {
            state.piccoloAdminVersion = value
        }
    },
    actions: {
        async fetchMeta(context: Context) {
            const response = await axios.get(`./public/meta/`)
            context.commit("updateSiteName", response.data.site_name)
            context.commit(
                "updatePiccoloAdminVersion",
                response.data.piccolo_admin_version
            )
        }
    }
}

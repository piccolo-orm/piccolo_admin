import axios from 'axios'

const BASE_URL = process.env.VUE_APP_BASE_URI

export default {
    state: {
        showAboutModal: false,
        meta: {}
    },
    mutations: {
        updateShowAboutModal(state, value: boolean) {
            state.showAboutModal = value
        },
        updateMeta(state, value: Object) {
            state.meta = value
        }
    },
    actions: {
        async fetchMeta(context) {
            const response = await axios.get(`${BASE_URL}meta/`)
            this.commit('updateMeta', response.data)
        }
    }
}

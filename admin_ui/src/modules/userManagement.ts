import axios from 'axios'

const BASE_URL = process.env.VUE_APP_BASE_URI


interface UserResponse {
    id: Number
}


export default {
    namespaced: true,
    state: {
        userList: [],
    },
    mutations: {
        updateUserList(state, value: any[]) {
            state.userList = value
        },
    },
    actions: {
        async fetchUserList(context) {
            const response = await axios.get(`${BASE_URL}user-management/`)
            context.commit('updateUserList', response.data)
        }
    }
}

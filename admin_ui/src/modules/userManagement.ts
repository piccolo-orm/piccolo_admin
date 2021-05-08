import axios from 'axios'
import { User } from '../interfaces'

const BASE_URL = process.env.VUE_APP_BASE_URI


export default {
    namespaced: true,
    state: {
        userList: [] as User[],
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

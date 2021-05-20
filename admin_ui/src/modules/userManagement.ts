import axios from 'axios'
import { User } from '../interfaces'

const BASE_URL = process.env.VUE_APP_BASE_URI


export default {
    namespaced: true,
    state: {
        userList: [] as User[],
        userSchema: null
    },
    mutations: {
        updateUserList(state, value: any[]) {
            state.userList = value
        },
        updateUserSchema(state, value: any) {
            state.userSchema = value
        }
    },
    actions: {
        async fetchUserList(context) {
            const response = await axios.get(`${BASE_URL}user-management/`)
            context.commit('updateUserList', response.data.rows)
        },
        async fetchUserSchema(context) {
            const response = await axios.get(`${BASE_URL}user-management/schema/`)
            context.commit('updateUserSchema', response.data)
        }
    }
}

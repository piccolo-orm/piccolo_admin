<template>
    <Modal v-on:close="$emit('close')">
        <h1><font-awesome-icon icon="lock" />Change password</h1>

        <form v-on:submit.prevent="updatePassword">
            <label>Username</label>
            <input type="text" v-bind:value="username" disabled />

            <label>New Password</label>
            <input v-model="password" type="password" placeholder="Password" />
            <input
                v-model="confirmedPassword"
                type="password"
                placeholder="Confirm password"
            />
            <button>Submit</button>
        </form>
    </Modal>
</template>

<script lang="ts">
import axios from "axios"

import Modal from "./Modal.vue"
import { APIResponseMessage } from "../interfaces"

const BASE_URL = process.env.VUE_APP_BASE_URI

export default {
    props: {
        username: {
            type: String,
            default: undefined,
        },
    },
    data() {
        return { password: "", confirmedPassword: "" }
    },
    components: {
        Modal,
    },
    methods: {
        async updatePassword() {
            if (this.password != this.confirmedPassword) {
                alert("The passwords don't match!")
                return
            }

            if (this.password.length < 8) {
                alert("The password must be at least 8 characters long!")
                return
            }

            await axios.post(`${BASE_URL}change-password/`, {
                username: this.username,
                password: this.password,
            })

            const message: APIResponseMessage = {
                contents: "Successfully updated password.",
                type: "success",
            }
            this.$store.commit("updateApiResponseMessage", message)
            this.$emit("close")
        },
    },
}
</script>

<style>
</style>

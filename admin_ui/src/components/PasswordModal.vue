<template>
    <Modal v-on:close="$emit('close')">
        <h1>Change password</h1>

        <form v-on:submit.prevent="updatePassword">
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

export default {
    props: {
        userId: {
            type: Number,
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

            await axios.post(`./change-password/`, {
                userID: this.userID,
                password: this.password,
            })

            this.$emit("close")
        },
    },
}
</script>

<style>
</style>

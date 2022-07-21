<template>
    <div id="change_password">
        <div class="inner">
            <BackButton />
            <h1>{{ $t("Change password") }}</h1>
            <form v-on:submit.prevent="changePassword">
                <label>{{ $t("Current password") }}</label>
                <input
                    name="current_password"
                    type="password"
                    v-model="currentPassword"
                />

                <label>{{ $t("New password") }}</label>
                <input
                    name="new_password"
                    type="password"
                    v-model="newPassword"
                />

                <label>{{ $t("New password confirmation") }}</label>
                <input
                    name="confirm_new_password"
                    type="password"
                    v-model="confirmNewPassword"
                />

                <button>{{ $t("Change password") }}</button>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import axios from "axios"
import BackButton from "../components/BackButton.vue"

export default {
    data() {
        return {
            currentPassword: "",
            newPassword: "",
            confirmNewPassword: ""
        }
    },
    components: {
        BackButton
    },
    methods: {
        async changePassword() {
            console.log("Changing password")
            const payload = {
                current_password: this.currentPassword,
                new_password: this.newPassword,
                confirm_new_password: this.confirmNewPassword
            }
            try {
                await axios.post(`./api/change-password/`, payload)
                this.$store.commit("updateApiResponseMessage", {
                    contents: `Changed password successfully. You will be redirected
                        to the login page to log in with your new credentials.`,
                    type: "success"
                })
                setTimeout(() => {
                    this.$router.push({ name: "home" })
                }, 3000)
            } catch (error) {
                console.log("Request failed")
                console.log(error.response)
                this.$store.commit("updateApiResponseMessage", {
                    contents: `Error - ${error.response.data.detail}`,
                    type: "error"
                })
            }
        }
    }
}
</script>

<style lang="less">
div#change_password {
    div.inner {
        margin: 0 auto;
        max-width: 30rem;
        padding: 2rem 2rem;

        h1 {
            margin-top: 0;
            padding-top: 0.5rem;
            text-align: center;
        }
    }
}
</style>

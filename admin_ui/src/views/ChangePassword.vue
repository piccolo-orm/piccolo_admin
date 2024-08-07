<template>
    <div id="change_password">
        <div class="inner">
            <BackButton />
            <div class="heading">
                <h1>{{ $t("Change Password") }}</h1>
            </div>
            <form v-on:submit.prevent="changePassword">
                <label>{{ $t("Current password") }}</label>
                <PasswordInput
                    :value="currentPassword"
                    @input="currentPassword = $event"
                />
                <label>{{ $t("New password") }}</label>
                <PasswordInput
                    :value="newPassword"
                    @input="newPassword = $event"
                />
                <label>{{ $t("New password confirmation") }}</label>
                <PasswordInput
                    :value="confirmNewPassword"
                    @input="confirmNewPassword = $event"
                />
                <button>{{ $t("Change Password") }}</button>
            </form>
        </div>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue"

import axios from "axios"
import BackButton from "../components/BackButton.vue"
import PasswordInput from "../components/PasswordInput.vue"

export default defineComponent({
    data() {
        return {
            currentPassword: "",
            newPassword: "",
            confirmNewPassword: ""
        }
    },
    components: {
        BackButton,
        PasswordInput
    },
    methods: {
        async changePassword() {
            const payload = {
                current_password: this.currentPassword,
                new_password: this.newPassword,
                confirm_new_password: this.confirmNewPassword
            }
            try {
                await axios.post(`./api/change-password/`, payload)
                this.$store.commit("updateApiResponseMessage", {
                    contents: `Changed password successfully. You will be redirected
                        to log in with your new credentials.`,
                    type: "success"
                })
                setTimeout(() => {
                    this.$router.push({ name: "home" })
                }, 3000)
            } catch (error) {
                console.log("Request failed")
                if (axios.isAxiosError(error) && error.response) {
                    console.log(error.response)
                    this.$store.commit("updateApiResponseMessage", {
                        contents: `Error - ${error.response.data.detail}`,
                        type: "error"
                    })
                }
            }
        }
    }
})
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
